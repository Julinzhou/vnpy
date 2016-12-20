# -*- coding: utf-8 -*-

import datetime, os

from program_top.utilities.my_datetime import my_date_time_microsec_format

class my_logger(object):
	'''
	记录日志的实例
	'''
	
	def __init__(self, log_writting_instance):
		'''如果哪个类想要写入日志，可以把自己传入日志类的构造函数'''
		
		self.__logged_id=id(log_writting_instance)#被记录类实例的id
		self.__logged_class=log_writting_instance.__class__.__name__#被记录实例的类名称
		
		self.logger_name="%s,%d"%(self.__logged_class, self.__logged_id)#logger_name
		log_path=log_writting_instance._environment_pack['runtime_paths']['output_dir']
		self.__log_file_encoding=log_writting_instance._environment_pack['current_platform_info'][
			'current_system_encoding']#读取当前运行操作系统的内码，输出日志文件时使用
		log_filename=log_path+self.logger_name+'.txt'
		self.__log_filename=log_filename
		
		pass
	
	def write_log(self, log_message):
		time_now=datetime.datetime.now().strftime(my_date_time_microsec_format)
		join_message=','.join([time_now, log_message])
		join_message.decode('utf-8').encode(self.__log_file_encoding)
		
		print join_message
		
		with open(self.__log_filename, mode='a') as file_struct:
			file_struct.write(log_message+os.linesep)
			file_struct.close()
			pass
		
		pass
	
	pass
