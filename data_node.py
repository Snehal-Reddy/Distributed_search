from concurrent import futures
import time
import math
import logging
import grpc
import json

import route_guide_pb2
import route_guide_pb2_grpc

from search_functions import perform_search, add_documents

from argparse import ArgumentParser
import argparse

parser = argparse.ArgumentParser(description='Query Node')
parser.add_argument('--port', type=str, default="8081",
                   help='port for the data node')
args = parser.parse_args()
port = args.port



class DataNode(route_guide_pb2_grpc.DataNodeServicer):
	
	def loadData(self):
		fp = open("data.json", 'r')
		self.data = json.load(fp)
		fp.close()


	def __init__(self,query_master,query_backup):
		super(DataNode,self).__init__()
		self.query_master = grpc.insecure_channel(query_master)
		self.query_backup = grpc.insecure_channel(query_backup)
		self.data = self.loadData()
		self.commit_logs = []

	def AskQuery(self, request, context):
		results = perform_search(request,self.data)
		for res in results:
			yield res

	def WriteRequest(self,request,context):
		status = add_documents(self.commit_logs,request,self.data)
		if status == True:
			return route_guide_pb2.Status(content="AGREED")
		else:
			route_guide_pb2.Status(content="ABORT")

	def WriteReply(self,request,context):
		if request.content == "ABORT":
			## undo using logs 
			pass
		return route_guide_pb2.Status(content="ACK")

	def DeleteRequest(self, request, context):
		print(request.docid)
		return route_guide_pb2.Status(content="AGREED")
	
	def DeleteReply(self, request, context):
		print(request.docid)
		return route_guide_pb2.Status(content="ACK")

	def FetchDocuments(self,request,content):
		print('recvd')
		return 	route_guide_pb2.Document(docid=1,title='title',content="Jello world")

# master_ip = input("Enter Master IP : ")
# backup_ip = input("Enter Backup IP : ")
master_ip = "localhost:50051"
backup_ip = "localhost:50052"
def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	data_node = DataNode(master_ip,backup_ip)
	route_guide_pb2_grpc.add_DataNodeServicer_to_server(data_node, server)
	server.add_insecure_port('[::]:%s'%(port))
	server.start()
	server.wait_for_termination()

serve()
