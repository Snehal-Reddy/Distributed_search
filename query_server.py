from concurrent import futures
import time
import math
import logging

import grpc

import route_guide_pb2
import route_guide_pb2_grpc


class DistributedSearchServicer(route_guide_pb2_grpc.DistributedSearchServicer):

	def AskQuery(self,request,context):

		query_string = request.query
		print("Received query string : ",query_string)
		arr = list(range(10))
		titles = "abcdefghij"
		for i in arr:
			yield route_guide_pb2.Result(docid=i,title=titles[i])


def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	route_guide_pb2_grpc.add_DistributedSearchServicer_to_server(
	DistributedSearchServicer(), server)
	server.add_insecure_port('[::]:8099')
	server.start()
	server.wait_for_termination()


serve()