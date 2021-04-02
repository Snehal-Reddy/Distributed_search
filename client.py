import grpc

import route_guide_pb2
import route_guide_pb2_grpc

master_server_ip = "localhost:50051"
backup_server_ip = "localhost:50052"
ip_list = [master_server_ip]  #add all ip ports here


def handle_search():
	query = input("Enter your search query : ")
	answered = False
	for address in ip_list:
		channel = grpc.insecure_channel(address)
		stub = route_guide_pb2_grpc.QueryNodeStub(channel)
		request = route_guide_pb2.Query(query=query.strip())
		print("Trying %s",address)
		try:
			responses = stub.AskQuery(request)
			print("Query Answered!")
			answered = True
			for response in responses:
				print("ID %d Title %s : "%(response.docid,response.title))
			break
		except Exception as e: 		# To-DO : See kind of exceptions and handle them separately and correctly
			print("Error with query server: ",e)

	if answered == False:
		print("Try with all query servers failed!")
		exit() 		# To-DO : Instead of exiting, set a number of times to retry?


def handle_write():

	docs = []
	doc_count = input("How many documents to add?")
	try:
		doc_count = int(doc_count)
		if doc_count<=0:
			1/0
	except:
		print("Invalid input, it must be >0")
		exit()

	for i in range(doc_count):
		docid = input("Enter docid : ")
		title = input("Enter title : ")
		content = input("Enter content : ")
		docid = int(docid) # To-DO : Check for errors here
		docs.append(route_guide_pb2.Document(docid=docid,title=title,content=content))

	answered = False
	for address in ip_list:
		channel = grpc.insecure_channel(address)
		stub = route_guide_pb2_grpc.QueryNodeStub(channel)
		print("Trying %s",address)
		try:
			response = stub.AddDocuments(iter(docs)).content
			print("Write response : ",response)
			if response=="OK":
				print("Query Completed!")
				answered = True
				break
		except Exception as e: 		# To-DO : See kind of exceptions and handle them separately and correctly
			print("Error with query server: ",e)

	if answered == False:
		print("Try with all query servers failed!")
		exit() 		# To-DO : Instead of exiting, set a number of times to retry?

def handle_delete():
	query = input("Enter the DocID: ")
	answered = False
	for address in ip_list:
		channel = grpc.insecure_channel(address)
		stub = route_guide_pb2_grpc.QueryNodeStub(channel)
		request = route_guide_pb2.DocumentId(docid=query)
		print("Trying %s",address)
		try:
			response = stub.DeleteDocuments(request)
			if response.content=='OK':
				answered = True
				print('Delete success!')
				break
			if response.content=='DNE':
				answered = True
				print('Document with given id doesn\'t exist!')
				break
		except Exception as e: 		# To-DO : See kind of exceptions and handle them separately and correctly
			print("Error with query server: ",e)

	if answered == False:
		print("Delete failed or document doesn't exist!")
		exit() 		# To-DO : Instead of exiting, set a number of times to retry?

def handle_fetch():
	query = input("Enter the DocID: ")
	answered = False
	for address in ip_list:
		channel = grpc.insecure_channel(address)
		stub = route_guide_pb2_grpc.QueryNodeStub(channel)
		request = route_guide_pb2.DocumentId(docid=query)
		print("Trying %s",address)
		try:
			response = stub.FetchDocuments(request)
			print("Document Fetched!")
			answered = True
			print("ID %d Title :%s \nContent: %s"%(response.docid,response.title,response.content))
			break
		except Exception as e: 		# To-DO : See kind of exceptions and handle them separately and correctly
			print("Error with query server: ",e)

	if answered == False:
		print("Fetch failed or document doesn't exist!")
		exit() 		# To-DO : Instead of exiting, set a number of times to retry?

while True:
	query_type = input("What kind of query?\n1. Search \n2. Add Documents \n3. Delete Documents \n4. Fetch by DocID:")
	try:
		query_type = int(query_type)
		if query_type not in [1,2,3,4]:
			1/0
	except Exception as e:
		print("Received invalid query")
		continue

	if query_type==1:
		handle_search()

	elif query_type==2:
		handle_write()

	elif query_type==3:
		handle_delete()

	elif query_type==4:
		handle_fetch()