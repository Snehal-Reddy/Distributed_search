from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
import time
import math
import logging
import json

import grpc
import route_guide_pb2
import route_guide_pb2_grpc

from argparse import ArgumentParser
import argparse

from search_functions import aggregate_results

parser = argparse.ArgumentParser(description='Query Node')
parser.add_argument('--kind', type=str, default="master",
                   help='choose between ["backup","master"]')
args = parser.parse_args()

def validate_arguments():
	if args.kind not in ['backup','master']:
		print("Wrong argument given for kind, exiting")
		exit()


class QueryNode(route_guide_pb2_grpc.QueryNodeServicer):

	def __init__(self,kind):
		super(QueryNode,self).__init__()
		self.kind = kind
		fp = open("metadata.json", 'r')
		self.partitions = json.load(fp)
		fp.close()
		self.no_of_partitions = len(self.partitions)
		self.commit_logs = []
		self.partition_last_index = [0]*self.no_of_partitions 
		self.last_doc_id = 0
		

	def AskQuery(self, request, context):
		query_string = request.query
		print("Received query string : ", query_string)
		## Now send to all data nodes
		all_responses = []
		for partition_no, partition in enumerate(self.partitions):
			print("[LOG]For partition no %d:"%(partition_no))		
			answered = False
			limit = self.partition_last_index[partition_no]
			i = (limit+1)%len(partition)
			while i!=limit:
				channel = grpc.insecure_channel(partition[i])
				stub = route_guide_pb2_grpc.DataNodeStub(channel)
				request = route_guide_pb2.Query(query=query_string)
				try:
					responses = stub.AskQuery(request)
					for response in responses:
						print("[LOG]ID: %d Title: %s Score: %f"%(response.docid, response.title, response.score))
						all_responses.append(response)
					answered = True
					break
				except grpc.RpcError as e:		
					print("Error with partition number %d DataNodeIP %s Exception::::%s "%(partition_no, partition[i], e.code().name))
				i = (i+1)%len(partition)
			
			if answered == False:
				print("No response from partition %d!"%(partition_no))
		final_result = aggregate_results(all_responses)
		for res in final_result:
			yield res

	def DeleteDocuments(self,request,context):
		docid = int(request.docid)
		print('Deleting doc with id: ',docid)
		partition_no = -1
		for pno, partition in enumerate(self.partitions):
			if docid in partition['doc_list']:
				partition_no = pno
		if partition_no == -1:
			print('Invalid docid')
			yield  route_guide_pb2.Status(content='DNE')
			return

		commit = True

		for data_node in self.data_node_details[partition_no]:
			channel = grpc.insecure_channel(data_node["ip"])
			stub = route_guide_pb2_grpc.DataNodeStub(channel) 
			try:
				commit_request_response = stub.DeleteRequest(request)
				if commit_request_response.content=='ABORT':
					commit = False
					print("Query server received ABORT from data node -> %s",data_node["ip"])
			except grpc.RpcError as e:		
				print("Error with data node",partition_no,data_node["ip"], e.code().name)
				commit = False

		commit_message = None
		if commit==True:
			self.commit_logs.append("commit")
			commit_message = "COMMIT"
		else:
			self.commit_logs.append("abort")
			commit_message = "ABORT"

		print("COMMIT MESSAGE : ",commit_message)
		def send_commit_reply(details):
			ip = details["ip"]
			message = details["message"]
			channel = grpc.insecure_channel(data_node["ip"])
			stub = route_guide_pb2_grpc.DataNodeStub(channel)
			while True:
				try:
					ack = stub.DeleteReply(route_guide_pb2.Status(content=message,timeout=5))
					return
				except Exception as e:
					pass

		reply_list = [(i["ip"],commit_message) for i in self.data_node_details[partition_no]]
		with ThreadPoolExecutor(4) as executor:
		    results = executor.map(send_commit_reply, reply_list)

		self.commit_logs.append("complete")
		ret_message = "OK"
		if commit_message=="ABORT":
			ret_message=='Fail'
		return route_guide_pb2.Status(content=ret_message)		

	def FetchDocuments(self,request,content):
		docid = int(request.docid)
		print('fetching %d'%(request.docid))
		if docid not in self.docid_partition:
			print('Invalid fetch')
			return route_guide_pb2.Document(docid=1,title='name',content='Document doesn\'t exist')
		partition_no = self.docid_partition[docid]

		for data_node in self.data_node_details[partition_no]:
			channel = grpc.insecure_channel(data_node["ip"])
			stub = route_guide_pb2_grpc.DataNodeStub(channel) 
			try:
				responses = stub.FetchDocuments(request)
				if responses.content!='Fail':
					return responses
			except Exception as e:		## To-Do => Try with different data nodes of same partition
				print("Error with data node",partition_no,data_nodes[i]["ip"],e)
				exit()
		
		return route_guide_pb2.Document(docid=1,title='name',content='Fail')

	def add_dummy_partition_details(self):  # Dummy function, for local testing
		self.data_partitions = 1
		self.data_node_details = {0:[{"ip":"localhost:8087","pending_requests":0}]}
		self.partition_sizes = {0:1}
		self.docid_partition = {1:0}

	def select_min_partition(self):
		# To-DO : select the min partition
		return 0


	def AddDocuments(self,request,context):
		"""
		To - Do : 
		Write the logs with enough details so that they can be completed after recovery from crash
		"""
		## Determine the correct partition to add to
		partition_no = self.last_doc_id%self.no_of_partitions
		# Initiate 2 phase commit with all these docs
		all_accepted = True
		for data_node_ip in self.partitions[partition_no]:
			channel = grpc.insecure_channel(data_node_ip)
			stub = route_guide_pb2_grpc.DataNodeStub(channel)
			try:
				commit_request_response = stub.WriteRequest(request).content
				if commit_request_response=="ABORT":
					print("Query server received ABORT from data node -> %s",data_node["ip"])
					all_accepted = False
			except Exception as e:
				## What to do here?
				all_accepted = False
				print("Error in COMMIT_REQUEST with data node %s, exception message : %s"%(data_node["ip"],e))
		
		send_message = None
		if all_accepted==True:
			self.commit_logs.append("commit")
			send_message = "COMMIT"
		else:
			self.commit_logs.append("abort")
			send_message = "ABORT"
		print("SEND MESSAGE : ",send_message)
		# send messages to all data nodes and wait for their replies [use threads]
		def send_commit_reply(details):
			ip = details["ip"]
			message = details["message"]
			channel = grpc.insecure_channel(data_node["ip"])
			stub = route_guide_pb2_grpc.DataNodeStub(channel)
			while True:
				try:
					ack = stub.WriteReply(route_guide_pb2.Status(content=message,timeout=5))
					return
				except Exception as e:
					pass

		reply_list = [(i["ip"],send_message) for i in self.data_node_details[min_partition]]
		with ThreadPoolExecutor(4) as executor:
		    results = executor.map(send_commit_reply, reply_list)

		self.commit_logs.append("complete")
		ret_message = "OK"
		if send_message=="ABORT":
			ret_message = "NOTOK"
		return route_guide_pb2.Status(content=ret_message)

	def Check(self, request, context):

		if(self.db == 'master'):
			self.logger.debug("Received heartbeat query from backup")
			self._HEALTH_CHECK_TIME += 1
			return search_pb2.HealthCheckResponse(status = "STATUS: Master server up!")

		# else it is a replica getting health check message from master
		self.logger.debug("Received heartbeat query from master")

		###
		#incomplete process
		###

		return search_pb2.HealthCheckResponse(status = "Replica " + self.ip + " up!", data = indices_to_remove)




def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	query_node = QueryNode(args.kind)
	route_guide_pb2_grpc.add_QueryNodeServicer_to_server(query_node, server)
	route_guide_pb2_grpc.add_HealthCheckServicer_to_server(query_node, server)
	if args.kind=="master":
		server.add_insecure_port('[::]:50051')
	else:
		server.add_insecure_port('[::]:50052')		

	server.start()

	try:
		while True:
			time.sleep(60 * 60 * 24)
	except KeyboardInterrupt:
		print("Stopping server ...")
		server.stop(0)

validate_arguments()
serve()