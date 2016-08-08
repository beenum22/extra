#!/usr/bin/env python
import zmq
import os
import logging
import sys
import time

from kazoo.client import KazooClient
from sys import path

path.append("hydra/src/main/python")
from hydra.lib import util
from hydra.lib.hdaemon import HDaemonRepSrv

l = util.createlogger('ZkPub', logging.INFO)

class HDZk(HDaemonRepSrv):
	#port here is the one that will be used by analyzer to send signals; one which which mesos assigns to it's app.
	def __init__(self, port):
		HDaemonRepSrv.__init__(self, port)
		self.register_fn('create', self.create_node)

	def create_node(self, arg1):
#		zk = KazooClient(hosts='10.10.0.73:2181')
#		zk.start()
		for i in range(int(arg1)):
			self.zk.create("/testhydra/data-", b"Muneeb", sequence=True)
		print "Done creating the znodes"
#		zk.stop()
		
def run(argv):
#	zk_ip_port = argv[1]

	zk = KazooClient(hosts='10.10.0.73:2181')
	zk.start()
	
	zkpub_an_port = os.environ.get('PORT0')
	print ("Starting Zk pub at port [%s]", zkpub_an_port)


			
	zks = HDHelloWorldPub(zkpub_an_port)
	zks.zk = zk
	zks.run()
	
	while True:
		time.sleep(1)
	zk.stop()
			 
if __name__ == "__main__":
    run(sys.argv)
