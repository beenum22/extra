#!/usr/bin/env python
import time
import sys

from sys import path
path.append("hydra/src/main/python")
from hydra.lib.runtestbase import HydraBase
from ConfigParser import ConfigParser
from hydra.lib.h_analyser import HAnalyser
tout_60s = 60000



class ZKPubAnalyser(HAnalyser):
	def __init__(self, server_ip, server_port, task_id):
		HAnalyser.__init__(self, server_ip, server_port, task_id)


class ZK(HydraBase):
	def __init__(self,client_count, num_msgs):
		self.config = ConfigParser()

		HydraBase.__init__(self, test_name='ZKstress', options=None, app_dirs=['src', 'hydra'])

		self.client_count = client_count
		self.num_msgs = num_msgs

		self.zk_pub_app_id = self.format_appname("/zk-pub")

		self.zk_pub_task_ip = None

		self.zk_pub_cmd_port = None

		self.zkpa = None  # Pub Analyzer

		self.add_appid(self.zk_pub_app_id)

	def run_test(self):
		"""
		Function which actually runs
		"""
        
		self.start_init()

		self.launch_zk_pub()

		self.post_run()
		
		
	def post_run():
		task_list = self.all_task_ids[self.zk_pub_app_id]
		print task_list
		for task_id in task_list:
			info = self.apps[self.zk_pub_app_id]['ip_port_map'][task_id]
			port = info[0]
			ip = info[1]

			self.zkpa = ZKPubAnalyser(ip, port, task_id)
			self.zkpa.do_req_resp('sendmsg', tout_60s, self.num_msgs)		
		
		
		

	def launch_zk_pub(self):
		"""
		Function to launch helloWorld pub app.
		"""
		print ("Launching the HelloWorld pub app")
		self.create_binary_app(name=self.zk_pub_app_id, app_script='./src/zk_stress.py',
                               cpus=0.01, mem=32,
                               ports=[0])


		self.scale_and_verify_app(self.zk_pub_app_id, self.client_count)

class RunTest(object):
	def __init__(self, argv):
		num_msgs = int(argv[1])
		client_count = int(argv[2])
 

		r = ZK(client_count,num_msgs)

		r.start_appserver()

		r.run_test()

		print ("Communicating sendmsg signal to pub")


        print ("About to sleep for 15")
#       time.sleep(15)
#        r.delete_all_launched_apps()
		r.stop_appserver()

if __name__ == "__main__":
	RunTest(sys.argv)
