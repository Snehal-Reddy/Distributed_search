import json
import os
import subprocess
import threading

with open("metadata.json","r") as r:
	dc = json.loads(r.read())

def run_data_node(port,pno,nno):
	os.system("python data_node.py --port %s > %d_%d.txt"%(port,pno,nno))

t_list = []
for pno,partition in enumerate(dc):
	for nno,node in enumerate(partition):
		port = node.split(":")[1]
		print("port : ",port)
		t = threading.Thread(target=run_data_node,args=(port,pno,nno,))	
		t_list.append(t)
		t.start()
		# with open("%d_%d.txt"%(pno,nno),"w") as w:
		# 	subprocess.Popen(["python","data_node.py","--port","%s"%(port)],stdout=w,stderr=w)

for i in t_list:
	i.join()
