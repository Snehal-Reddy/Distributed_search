from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
import time
import math
import logging

import grpc

import route_guide_pb2
import route_guide_pb2_grpc

from argparse import ArgumentParser
import argparse

from search_functions import preprocess_query, aggregate_results

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
		self.data_partitions = 0
		self.data_node_details = {}
		self.partition_sizes = {} 	# to decide the minimum size partition to insert the documents to
		## Format : key = partition number, 
		## value = list of data nodes, each element is a dict having ip, pending_requests
		self.add_dummy_partition_details()
		self.commit_logs = []

	def AskQuery(self,request,context):
		"""
		To-DO : use threads to send all requests to data nodes in parallel
		"""
		query_string = request.query
		print("Received query string : ",query_string)
		preprocessed_query = preprocess_query(query_string)
		## Now send to all data nodes
		all_responses = []
		for partition_no in range(self.data_partitions):
			data_nodes = self.data_node_details[partition_no]
			min_load = 0
			for i,node in enumerate(data_nodes):
				if node["pending_requests"] < data_nodes[min_load]["pending_requests"]:
					min_load = data_nodes
			data_nodes[min_load]["pending_requests"] += 1
			channel = grpc.insecure_channel(data_nodes[min_load]["ip"])
			stub = route_guide_pb2_grpc.DataNodeStub(channel)
			request = route_guide_pb2.Query(query=preprocessed_query)
			try:
				responses = stub.AskQuery(request)
				print("For partition no %d : "%(partition_no))
				received_responses = []
				for response in responses:
					print("ID %d Title %s : "%(response.docid,response.title))
					received_responses.append(response)
			except Exception as e:		## To-Do => Try with different data nodes of same partition
				print("Error with partition number %d DataNodeIP %s Exception::::%s "%(partition_no,data_nodes[min_load]["ip"],e))
				exit()

			all_responses.append(received_responses)
			data_nodes[min_load]["pending_requests"] -= 1

		final_result = aggregate_results(all_responses)
		for res in final_result:
			yield res

	def add_dummy_partition_details(self):  # Dummy function, for local testing
		self.data_partitions = 1
		self.data_node_details = {0:[{"ip":"localhost:8087","pending_requests":0}]}
		self.partition_sizes = {0:1}

	def select_min_partition(self):
		# To-DO : select the min partition
		return 0


	def AddDocuments(self,request_iterator,context):
		"""
		To - Do : 
		Write the logs with enough details so that they can be completed after recovery from crash
		"""
		## Determine the correct partition to add to
		min_partition = self.select_min_partition()
		# Initiate 2 phase commit with all these docs
		all_accepted = True
		for data_node in self.data_node_details[min_partition]:
			channel = grpc.insecure_channel(data_node["ip"])
			stub = route_guide_pb2_grpc.DataNodeStub(channel)
			try:
				commit_request_response = stub.WriteRequest(request_iterator).content
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




def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	query_node = QueryNode(args.kind)
	route_guide_pb2_grpc.add_QueryNodeServicer_to_server(query_node, server)
	if args.kind=="master":
		server.add_insecure_port('[::]:8099')
	else:
		server.add_insecure_port('[::]:8098')		
	server.start()
	server.wait_for_termination()

validate_arguments()
serve()