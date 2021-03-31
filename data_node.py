from concurrent import futures
import time
import math
import logging
import grpc

import route_guide_pb2
import route_guide_pb2_grpc

from search_functions import perform_search, add_documents

class DataNode(route_guide_pb2_grpc.DataNodeServicer):
	def __init__(self,query_master,query_backup):
		super(DataNode,self).__init__()
		self.query_master = grpc.insecure_channel(query_master)
		self.query_backup = grpc.insecure_channel(query_backup)
		self.data = None
		self.commit_logs = []

	def AskQuery(self, request, context):
		results = perform_search(request,self.data)
		for res in results:
			yield res

	def WriteRequest(self,request_iterator,context):
		try:
			add_documents(request_iterator)
			self.commit_logs.append("success") 		# To-DO : Make the logs message such that it is revertible
			return route_guide_pb2.Status(content="AGREED")
		except Exception as e:
			print("Exception in local transaction, %s",e)
			return route_guide_pb2.Status(content="ABORT")

	def WriteReply(self,request,context):
		if request.content == "ABORT":
			## undo using logs 		# To-DO : Revert based on log content
			pass
		return route_guide_pb2.Status(content="ACK")

# master_ip = input("Enter Master IP : ")
# backup_ip = input("Enter Backup IP : ")
master_ip = "localhost:8099"
backup_ip = "localhost:8098"
def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	data_node = DataNode(master_ip,backup_ip)
	route_guide_pb2_grpc.add_DataNodeServicer_to_server(data_node, server)
	server.add_insecure_port('[::]:8087')
	server.start()
	server.wait_for_termination()

serve()
