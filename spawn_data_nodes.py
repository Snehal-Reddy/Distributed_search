import json
import os
import subprocess

with open("metadata.json","r") as r:
	dc = json.loads(r.read())

for pno,partition in enumerate(dc):
	for nno,node in enumerate(partition):
		port = node.split(":")[1]
		print("port : ",port)
		# os.system("python data_node.py --port %s > %d_%d.txt"%(port,pno,nno))
		with open("%d_%d.txt"%(pno,nno),"w") as w:
			subprocess.Popen(["python","data_node.py","--port","%s"%(port)],stdout=w,stderr=w)
