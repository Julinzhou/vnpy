# -*- coding: utf-8 -*-

from tornado.ioloop import IOLoop

from program_top.utilities.process_and_main_function.my_engine import my_engine

def main_function(running_class_def=None):
	'''主函数，传入开始执行的主函数，然后以指定的类作为起始工作实例，为单实例机器的程序入口'''
	a=my_engine(running_class_def)
	#b=my_engine(running_class_def)
	
	IOLoop.current().start()
	pass