#-*-coding:utf-8-*-

import os,json,cPickle
from pandas import DataFrame
from program_top.utilities.my_dir import make_ever_dir
from program_top.utilities.data_container_operations import nested_dict_apply
from program_top.utilities.string_and_unicode import to_string_if_unicode

def read_csv_into_paterns(absolute_csv_filename,pattern):
	if os.path.isfile(absolute_csv_filename):
		target_frame=DataFrame.from_csv(absolute_csv_filename)
		target_list=target_frame.to_dict(pattern)
		return target_list

	else:
		target_string=','.join([absolute_csv_filename,''])

		utilities.write_log(target_string)

		return[]
	pass

def pickle_load(pickle_filename):
	loaded_content=None
	
	try:
		with open(pickle_filename,'r') as file_struct:
			loaded_content=cPickle.load(file_struct)
			pass
	except Exception, current_error:
		error_msg=current_error.strerror
		print '读取pickle文件失败，信息',error_msg
		pass
	
	return loaded_content

def pickle_save(raw_object_to_save, pickle_filename):
	try:
		with open(pickle_filename,'w') as file_struct:
			cPickle.dump(raw_object_to_save,file_struct)
			pass
	except Exception, current_error:
		error_msg=current_error.strerror
		print '写入pickle文件失败，信息',error_msg
		pass
	pass

def temperarily_load_a_local_json(json_filename,as_set=False):
	loaded_content=None
	try:
		with open(json_filename,'r')as file_struct:
			loaded_content=json.loads(file_struct.read())
			pass

	except Exception,current_error:
		print'%s文件读取失败,错误信息%s'%(json_filename,current_error.__repr__())
		pass
	
	return nested_dict_apply(loaded_content,to_string_if_unicode,set_or_list=as_set)

def temperarily_save_a_local_json(raw_object_to_save,json_filename):
	'''
	临时存入一个文件
	'''
	
	target_object_to_save=nested_dict_apply(raw_object_to_save)#过滤其中的set

	try:
		with open(json_filename,'w')as file_struct:
			json_serialised=json.dumps(target_object_to_save)
			file_struct.write(json_serialised)
			file_struct.close()
			pass

	except Exception,current_exception:
		print'%s文件写入失败,错误信息%s'%(json_filename, current_exception.__repr__())

	pass

class cacheable_data(object):
	'''
	带缓存的变量
	'''
	def __init__(self,data_name,default_type,dictionary_buffering_path):
		self.data_name=data_name
		self.relative_filename=data_name+'.json'
		self.absolute_filename=dictionary_buffering_path+self.relative_filename
		self.path=dictionary_buffering_path
		self.load_from_json(default_type)
		pass

	def save_to_json(self,path_to_save=None):

		if path_to_save:
			absolute_save_name=path_to_save+self.relative_filename
			make_ever_dir(path_to_save)

		else:

			if self.absolute_filename:
				absolute_save_name=self.absolute_filename
			else:
				print'请指定存入的绝对路径'
				return None
			pass

		temperarily_save_a_local_json(self.data_content,absolute_save_name)
		pass

	def load_from_json(self,default_type=None):
		loaded=temperarily_load_a_local_json(self.absolute_filename)

		if loaded:
			self.data_content=default_type(loaded)
		else:
			self.data_content=default_type()
		pass
	pass

class cacheable_set(cacheable_data):
	def __init__(self,data_name,buffer_path):
		super(cacheable_set,self).__init__(data_name=data_name,default_type=set,dictionary_buffering_path=buffer_path)
		pass

	def __getattr__(self,item):
		'''
		如果没有item成员函数，则调用data_content的item成员函数
		'''

		if hasattr(self.data_content,item):
			def wrapper(parameter=None):
				target_function=getattr(self.data_content,item)
				if parameter:
					result=target_function(parameter)
				else:
					result=target_function()
				self.save_to_json()
				return result
			return wrapper
		raise AttributeError(item)
		pass
	pass
