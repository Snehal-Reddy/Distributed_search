import grpc

import route_guide_pb2
import route_guide_pb2_grpc

master_server_ip = "localhost:8099"

while True:
	query = input("Enter your query :")
	channel = grpc.insecure_channel(master_server_ip)
	stub = route_guide_pb2_grpc.DistributedSearchStub(channel)
	request = route_guide_pb2.Query(query=query.strip())
	try:
		responses = stub.AskQuery(request)
		for response in responses:
			print("ID %d Title %s : "%(response.docid,response.title))
	except Exception as e:
		print("ERRORR : ",e)
		exit()
	print("LOOP")
