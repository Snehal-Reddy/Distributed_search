from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
import time
import math
import logging
import json
import _thread
import grpc
import route_guide_pb2
import route_guide_pb2_grpc
from google.protobuf import empty_pb2
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
		self.isMasterAlive = True
		if(self.kind=='backup'):
			try:
				_thread.start_new_thread(self.sendHeartBeatMessage, ("localhost:50051",))
			except Exception as e:
				print("[LOG]"+str(e))


		

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
			tried = 0
			while tried<len(partition):
				channel = grpc.insecure_channel(partition[i])
				stub = route_guide_pb2_grpc.DataNodeStub(channel)
				request = route_guide_pb2.Query(query=query_string)
				try:
					responses = stub.AskQuery(request)
					for response in responses:
						print("[LOG]ID: %d Title: %s Score: %f"%(response.docid, response.title, response.score))
						all_responses.append(response)
					answered = True
					self.partition_last_index[partition_no] = i 
					break
				except Exception as e:		
					print("Error with partition number %d DataNodeIP %s Exception::::%s "%(partition_no, partition[i], e))
				i = (i+1)%len(partition)
				tried += 1
			
			if answered == False:
				print("No response from partition %d!"%(partition_no))
		final_result = aggregate_results(all_responses)
		for res in final_result:
			yield res

	def DeleteDocument(self,request,content):
		docid = int(request.docid)
		print('Deleting doc with id: ',docid)
		 
		partition_no = docid%self.no_of_partitions
		print("Parittion Number : ",partition_no)

		commit = True

		for data_node_ip in self.partitions[partition_no]:
			channel = grpc.insecure_channel(data_node_ip)
			stub = route_guide_pb2_grpc.DataNodeStub(channel) 
			try:
				commit_request_response = stub.DeleteRequest(request)
				if commit_request_response.content=='ABORT':
					commit = False
					print("Query server received ABORT from data node -> %s",data_node_ip)
				else:
					print("Received %s from %s"%(commit_request_response,data_node_ip))
			except grpc.RpcError as e:		
				print("Error with data node",partition_no,data_node_ip, e.code().name)
				commit = False

		commit_message = None
		if commit==True:
			self.commit_logs.append("commit")
			commit_message = "COMMIT"
		else:
			self.commit_logs.append("abort")
			commit_message = "ABORT"
		print("COORDINATOR TO COHORT FOR 2 phase commit: ",commit_message)

		for ip in self.partitions[partition_no]:
			channel = grpc.insecure_channel(ip)
			stub = route_guide_pb2_grpc.DataNodeStub(channel)
			for abc in range(10):
				try:
					ack = stub.DeleteReply(route_guide_pb2.Status(content=commit_message))
					break
				except Exception as e:
					print("Exception : ",e)
					time.sleep(1)

		self.commit_logs.append("complete")
		ret_message = "OK"
		if commit_message=="ABORT":
			ret_message = "NOTOK"
		print("Return obj")
		obj = route_guide_pb2.Status(content=ret_message)
		return obj


	def FetchDocuments(self,request,context):
		docid = int(request.docid)
		partition_no = (docid)%self.no_of_partitions
		print('fetching %d'%(request.docid))
		limit = self.partition_last_index[partition_no]
		partition = self.partitions[partition_no]
		i = (limit+1)%len(partition)
		print(i)
		while i!=limit:
			channel = grpc.insecure_channel(partition[i])
			stub = route_guide_pb2_grpc.DataNodeStub(channel) 
			try:
				responses = stub.FetchDocuments(request)
				if responses.content!='Fail':
					self.partition_last_index[partition_no] = i
					return responses
			except Exception as e:		## To-Do => Try with different data nodes of same partition
				print("Error with data node",partition_no,data_node,e)
				exit()
			i = (i+1)%len(partition)

		return route_guide_pb2.Document(docid=1,title='name',content='Fail')

	# def add_dummy_partition_details(self):  # Dummy function, for local testing
	# 	self.data_partitions = 1
	# 	self.data_node_details = {0:[{"ip":"localhost:8087","pending_requests":0}]}
	# 	self.partition_sizes = {0:1}
	# 	self.docid_partition = {1:0}

	# def select_min_partition(self):
	# 	# To-DO : select the min partition
	# 	return 0


	def AddDocuments(self,request,context):
		"""
		To - Do : 
		Write the logs with enough details so that they can be completed after recovery from crash
		"""
		## Determine the correct partition to add to
		partition_no = self.last_doc_id%self.no_of_partitions
		print("PNO : ",partition_no)
		request.docid = self.last_doc_id
		self.last_doc_id += 1
		# Initiate 2 phase commit with all these docs
		all_accepted = True
		for data_node_ip in self.partitions[partition_no]:
			channel = grpc.insecure_channel(data_node_ip)
			stub = route_guide_pb2_grpc.DataNodeStub(channel)
			try:
				commit_request_response = stub.WriteRequest(request).content
				if commit_request_response=="ABORT":
					print("Query server received ABORT from data node -> %s",data_node_ip)
					all_accepted = False
				else:
					print("Received %s from %s"%(commit_request_response,data_node_ip))
			except Exception as e:
				## What to do here?
				all_accepted = False
				print("Error in COMMIT_REQUEST with data node %s, exception message : %s"%(data_node_ip,e))
		
		send_message = None
		if all_accepted==True:
			self.commit_logs.append("commit")
			send_message = "COMMIT"
		else:
			self.commit_logs.append("abort")
			send_message = "ABORT"
		print("COORDINATOR TO COHORT FOR 2 phase commit: ",send_message)
		# send messages to all data nodes and wait for their replies [use threads]
		# def send_commit_reply(details):
		# 	ip = details[0]
		# 	message = details[1]
		# 	channel = grpc.insecure_channel(ip)
		# 	stub = route_guide_pb2_grpc.DataNodeStub(channel)
		# 	while True:
		# 		try:
		# 			ack = stub.WriteReply(route_guide_pb2.Status(content=message))
		# 			return
		# 		except Exception as e:
		# 			pass

		# reply_list = [(ip,send_message) for ip in self.partitions[partition_no]]
		# with ThreadPoolExecutor(4) as executor:
		#     results = executor.map(send_commit_reply, reply_list)

		for ip in self.partitions[partition_no]:
			channel = grpc.insecure_channel(ip)
			stub = route_guide_pb2_grpc.DataNodeStub(channel)

			for abc in range(10):
				try:
					ack = stub.WriteReply(route_guide_pb2.Status(content=send_message))
					break
				except Exception as e:
					print("Exception : ",e)
					time.sleep(1)


		print('We are here now')
		self.commit_logs.append("complete")
		ret_message = "OK"
		if send_message=="ABORT":
			ret_message = "NOTOK"
		print("Return obj")
		obj = route_guide_pb2.Status(content=ret_message)
		return obj

	def getMaxID(self):
		mid = -1
		for partition_no, partition in enumerate(self.partitions):
			print("[LOG]for partition no %d:"%(partition_no))
			for i in range(0, len(partition)):
				channel = grpc.insecure_channel(partition[i])
				stub = route_guide_pb2_grpc.DataNodeStub(channel)
				try:
					response = stub.getMID(empty_pb2.Empty())
					mid = max(mid, response.docid)	
					print("docid - ", mid)
				except Exception as e:		
					print("Error with partition number %d DataNodeIP %s Exception::::%s "%(partition_no, partition[i], e))

		return mid


	def sendHeartBeatMessage(self, m_ip):
		while 1:
			time.sleep(15)
			channel = grpc.insecure_channel(m_ip) #localhost:50051
			stub = route_guide_pb2_grpc.HealthCheckStub(channel)
			request = route_guide_pb2.HealthCheckRequest(healthCheck = 'is_working?')
			print("req")
			try:
				response = stub.Check(request, timeout = 10)
				print("Resp - ",response)
				self.isMasterAlive = True
			except Exception as e:
				print("Err - ",e)
				MID = self.getMaxID()
				self.last_doc_id = MID
				# self.kind = "master"
				self.isMasterAlive = False
				return

	# def Check(self, request, context):
	# 	# self._HEALTH_CHECK_TIME += 1
	# 	print("received")
	# 	return route_guide_pb2.HealthCheckResponse(status = "STATUS: Master server up!")

class HealthCheck(route_guide_pb2_grpc.HealthCheckServicer):
	def __init__(self ):
		super(HealthCheck,self).__init__()
		self._HEALTH_CHECK_TIME = 0

	def Check(self, request, context):
		self._HEALTH_CHECK_TIME += 1
		print("received")
		return route_guide_pb2.HealthCheckResponse(status = "STATUS: Master server up!")



def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	query_node = QueryNode(args.kind)
	health_check = HealthCheck()
	route_guide_pb2_grpc.add_QueryNodeServicer_to_server(query_node, server)
	
	if args.kind=="master":
		route_guide_pb2_grpc.add_HealthCheckServicer_to_server(health_check, server)
		server.add_insecure_port('[::]:50051')
		print("Starting master")
	else:
		server.add_insecure_port('[::]:50052')
		print("Starting backup")		

	server.start()

	try:
		while True:
			time.sleep(60 * 60 * 24)
	except KeyboardInterrupt:
		print("Stopping server ...")
		server.stop(0)

validate_arguments()
serve()