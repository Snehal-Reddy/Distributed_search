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
				print("ERERE")
			print("Query Success!")
			answered = True
			break
		except Exception as e: 		# To-DO : See kind of exceptions and handle them separately and correctly
			print("Error with query server:", e)

	if answered == False:
		print("Try with all query servers failed!")


def handle_write():
	# docs = []
	# doc_count = input("How many documents to add? ")
	# try:
	# 	doc_count = int(doc_count)
	# 	if doc_count <= 0:
	# 		raise Exception("Invalid DocID")			# To-DO : Throw exception and handle that particular exception only
	# except:
	# 	print("Invalid input, it must be >0.")
	# 	return
	# try:
	# 	for _ in range(doc_count):
	# 		docid = input("Enter docid: ")
	# 		title = input("Enter title: ")
	# 		content = input("Enter content: ")
	# 		docid = int(docid) # To-DO : Check for errors here
	# 		docs.append(route_guide_pb2.Document(docid=docid,title=title,content=content))
	# except Exception as e:
	# 	print("Invalid input.")
	# 	return

	title = input("Enter title: ")
	content = input("Enter content: ")
	doc = route_guide_pb2.Document(title=title,content=content)


	answered = False
	for address in ip_list:
		channel = grpc.insecure_channel(address)
		stub = route_guide_pb2_grpc.QueryNodeStub(channel)
		print("Trying %s ..."%(address))
		try:
			response = stub.AddDocuments(doc)
			print("Response:", response.content)
			if response.content == "OK":
				print("Write Success!")
				answered = True
				break
			# To-DO : Check for other cases.
			elif response.content == "NOTOK":
				print("Write fail two phase commit decision abort")
		except Exception as e: 		# To-DO : See kind of exceptions and handle them separately and correctly, this is still not sufficient
			print("Error with query server:", e)

	if answered == False:
		print("Try with all query servers failed!")

def handle_delete():
	query = input("Enter the DocIDs: ")
	docIds = []
	try:
		for id in query.split():
			docIds.append(route_guide_pb2.DocumentId(docid=int(id))) 		# To-DO : Check whether query is correct or not
	except Exception as e: 												# To-DO : Check for particular class of Exception
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

def handle_fetch():

	query = input("Enter the DocID: ")
	try:								# To-DO : Handle this properly
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
			# To-DO : Check for other cases. [What other cases???]
		except grpc.RpcError as e: 		# To-DO : See kind of exceptions and handle them separately and correctly
			print("Error with query server:", e.code().name)

	if answered == False:
		print("Fetch failed or document doesn't exist!")


##################
while True:
	query_type = input("What kind of query?\n1. Search \n2. Add Documents \n3. Delete Documents \n4. Fetch by DocID \n5. Exit \n>> ")
	try:
		query_type = int(query_type)
		if query_type not in [1,2,3,4,5]:
			raise Exception("Invalid Query Type")
	except Exception as e:			
		print("Exception Message ",e) 			
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