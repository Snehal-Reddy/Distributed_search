from concurrent import futures
import time
import math
import logging
import grpc

import route_guide_pb2
import route_guide_pb2_grpc

from search_functions import perform_search

class DataNode(route_guide_pb2_grpc.DataNodeServicer):
	def __init__(self,query_master,query_backup):
		super(DataNode,self).__init__()
		self.query_master = grpc.insecure_channel(query_master)
		self.query_backup = grpc.insecure_channel(query_backup)
		self.data = None

	def AskQuery(self, request, context):
		results = perform_search(request,self.data)
		for res in results:
			yield res

master_ip = input("Enter Master IP : ")
backup_ip = input("Enter Backup IP : ")
def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	data_node = DataNode(master_ip,backup_ip)
	route_guide_pb2_grpc.add_DataNodeServicer_to_server(data_node, server)
	server.add_insecure_port('[::]:8087')
	server.start()
	server.wait_for_termination()

serve()
