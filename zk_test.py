#!/usr/bin/env python
import time
import sys

from sys import path
path.append("hydra/src/main/python")
from hydra.lib.runtestbase import HydraBase
from ConfigParser import ConfigParser
from hydra.lib.h_analyser import HAnalyser
tout_60s = 60000

class ZkPubAnalyser(HAnalyser):
	def __init__(self, server_ip, server_port, task_id):
		HAnalyser.__init__(self, server_ip, server_port, task_id)
        
class ZK(HydraBase):
	def __init__(self):	#pub_port in arguments before
		self.config = ConfigParser()
		HydraBase.__init__(self, test_name='ZKstress', options=None, app_dirs=['src', 'hydra'])
#		self.pub_port = pub_port
		self.zk_pub_app_id = self.format_appname("/zk-pub")
		self.zk_pub_task_ip = None
		self.zk_pub_cmd_port = None
		self.zkpa = None
		self.add_appid(self.zk_pub_app_id)
		
	def run_test(self):
		"""
		Function which actually runs
    	"""
    	# Get Mesos/Marathon client
    	self.start_init()
    	# Launch HelloWorld Pub
    	self.launch_zk_pub()

	def launch_zk_pub(self):
		"""
		Function to launch ZKStress pub app.
		"""
		print ("Launching the ZKStress pub app")
		self.create_binary_app(name=self.zk_pub_app_id, app_script='./src/zk_pub.py',
								cpus=0.01, mem=32,
								ports=[0])
                               
		ipm = self.get_app_ipport_map(self.zk_pub_app_id)
		
		assert (len(ipm) == 1)
		self.zk_pub_task_ip = ipm.values()[0][1]                               
		self.zk_pub_cmd_port = str(ipm.values()[0][0])                               
        
		print("[helloworldtest.zk_pub] ZKStress running at [%s:%s]" % (self.zk_pub_task_ip, self.zk_pub_cmd_port))
		self.zkpa = ZKPubAnalyser(self.zk_pub_task_ip, self.zk_pub_cmd_port, self.zk_pub_app_id)
        
        
class RunTest(object):
	def __init__(self, argv):
#        pub_port = argv[1]
        num_msgs = argv[1]
        
        z = ZK()		
        z.start_appserver()
        z.run_test()
        
        print ("Communicating create signal to pub")
#        z.zkpa.do_req('create', tout_60s, arg1=num_msgs)
        
        
		z.delete_all_launched_apps()
		z.stop_appserver()        
        
if __name__ == "__main__":
    RunTest(sys.argv)        
        
        
        
        
        
        
        
        
        
        
        
        
        
                               
                               
                               
