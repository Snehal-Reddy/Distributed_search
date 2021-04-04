import grpc

import route_guide_pb2
import route_guide_pb2_grpc

ip_list = ["localhost:50051", "localhost:50052"]

def handle_search():

	query = input("Enter your search query: ")

	answered = False

	for address in ip_list:
		channel = grpc.insecure_channel(address)
		stub = route_guide_pb2_grpc.QueryNodeStub(channel)
		request = route_guide_pb2.Query(query=query.strip())
		print("Trying %s ..."%(address))
		try:
			responses = stub.AskQuery(request)
			for response in responses:
				print("ID: %d :: Title: %s"%(response.docid,response.title))
			print("Query Success!")
			answered = True
			break
		except Exception as e: 		# To-DO : See kind of exceptions and handle them separately and correctly
			print("Error with query server:", e)

	if answered == False:
		print("Try with all query servers failed!")
	# To-DO : Instead of exiting, set a number of times to retry?


def handle_write():

	docs = []
	doc_count = input("How many documents to add? ")
	try:
		doc_count = int(doc_count)
		if doc_count <= 0:
			1/0
	except:
		print("Invalid input, it must be >0.")
		return
	try:
		for _ in range(doc_count):
			docid = input("Enter docid: ")
			title = input("Enter title: ")
			content = input("Enter content: ")
			docid = int(docid) # To-DO : Check for errors here
			docs.append(route_guide_pb2.Document(docid=docid,title=title,content=content))
	except Exception as e:
		print("Invalid input.")
		return

	answered = False
	for address in ip_list:
		channel = grpc.insecure_channel(address)
		stub = route_guide_pb2_grpc.QueryNodeStub(channel)
		print("Trying %s ..."%(address))
		try:
			response = stub.AddDocuments(iter(docs)).content
			print("Response:", response.content)
			if response.content == "OK":
				print("Write Success!")
				answered = True
				break
			# To-DO : Check for other cases.
		except grpc.RpcError as e: 		# To-DO : See kind of exceptions and handle them separately and correctly
			print("Error with query server:", e.code().name)

	if answered == False:
		print("Try with all query servers failed!")
	# To-DO : Instead of exiting, set a number of times to retry?

def handle_delete():

	query = input("Enter the DocIDs: ")
	docIds = []
	try:
		for id in query.split():
			docIds.append(route_guide_pb2.DocumentId(docid=int(id)))
	except Exception as e:
		print("Invalid input.")
		return

	answered = False
	for address in ip_list:
		channel = grpc.insecure_channel(address)
		stub = route_guide_pb2_grpc.QueryNodeStub(channel)
		print("Trying %s ..."%(address))
		try:
			response = stub.DeleteDocuments(iter(docIds)).content
			print("Response:", response.content)
			if response.content == "OK":
				print("Delete Success!")
				answered = True
				break
			if response.content == 'DNE':
				print('Documents with the given ids do not exist!')
				answered = True
				break
			# To-DO : Check for other cases.
		except grpc.RpcError as e: 		# To-DO : See kind of exceptions and handle them separately and correctly
			print("Error with query server:", e.code().name)

	if answered == False:
		print("Try with all query servers failed!")
	# To-DO : Instead of exiting, set a number of times to retry?

def handle_fetch():

	query = input("Enter the DocID: ")
	try:
		docId = int(query)
	except Exception as e:
		print("Invalid input.")
		return

	answered = False
	for address in ip_list:
		channel = grpc.insecure_channel(address)
		stub = route_guide_pb2_grpc.QueryNodeStub(channel)
		request = route_guide_pb2.DocumentId(docid=docId)
		print("Trying %s ..."%(address))
		try:
			response = stub.FetchDocuments(request)
			if response.docid >= 0:
				print("Document Fetched!")
				print("ID: %d Title: %s \nContent: %s"%(response.docid,response.title,response.content))
				answered = True
				break
			if response.docid == -1:
				print('Documents with the given id does not exist!')
				answered = True
				break
			# To-DO : Check for other cases.
		except grpc.RpcError as e: 		# To-DO : See kind of exceptions and handle them separately and correctly
			print("Error with query server:", e.code().name)

	if answered == False:
		print("Fetch failed or document doesn't exist!")
	# To-DO : Instead of exiting, set a number of times to retry?

while True:
	query_type = input("What kind of query?\n1. Search \n2. Add Documents \n3. Delete Documents \n4. Fetch by DocID \n5. Exit \n>> ")
	try:
		query_type = int(query_type)
		if query_type not in [1,2,3,4,5]:
			1/0
	except Exception as e:
		print("Received invalid query type.")
		continue

	if query_type==1:
		handle_search()

	elif query_type==2:
		handle_write()

	elif query_type==3:
		handle_delete()

	elif query_type==4:
		handle_fetch()

	elif query_type==5:
		exit()