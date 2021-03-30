from concurrent import futures
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
		## Format : key = partition number, 
		## value = list of data nodes, each element is a dict having ip, pending_requests
		self.add_dummy_partition_details()

	def AskQuery(self,request,context):
		"""
		One more To-DO : use threads to send all requests to data nodes in parallel
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
			except Exception as e:
				print("ERRORR : ",e)
				exit()

			all_responses.append(received_responses)
			data_nodes[min_load]["pending_requests"] -= 1

		final_result = aggregate_results(all_responses)
		for res in final_result:
			yield res

	def add_dummy_partition_details(self):
		self.data_partitions = 1
		self.data_node_details = {0:[{"ip":"localhost:8087","pending_requests":0}]}


def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	query_node = QueryNode(args.kind)
	route_guide_pb2_grpc.add_QueryNodeServicer_to_server(query_node, server)
	server.add_insecure_port('[::]:8099')
	server.start()
	server.wait_for_termination()

validate_arguments()
serve()