import route_guide_pb2
import route_guide_pb2_grpc

def preprocess_query(query):
	"""
	Input : query string as received from client
	O/p : preprocessed query string
	whatever preprocessing you do, change message formats accordingly
	"""
	return query.lower()

def aggregate_results(all_responses):
	return all_responses[:5]


def perform_search(query,data):
	res = []
	for docs in data:
		if docs["content"].startswith(query):
			res.append(route_guide_pb2.Result(docid=docs["docid"],title=docs["title"],score=0))
	
	return res


def add_documents(commit_logs,query,data):
	## Write steps in commit log, add data and return true/false 
	print("types : ",type(commit_logs),type(data),flush=True)
	commit_logs.append("inserting docid %d"%query.docid)
	return True

