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
	arr = list(range(10))
	titles = "abcdefghij"
	return [route_guide_pb2.Result(docid=i,title=titles[i]) for i in range(10)]


def add_documents(commit_logs,query,data):
	## Write steps in commit log, add data and return true/false 
	return True

