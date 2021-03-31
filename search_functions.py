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
	response_merge = []
	for responses in all_responses:
		response_merge += responses
	return response_merge


def perform_search(query,data):
	arr = list(range(10))
	titles = "abcdefghij"
	return [route_guide_pb2.Result(docid=i,title=titles[i]) for i in range(10)]

def add_documents(request_iterator):
	## Raise exception if errors
	return

