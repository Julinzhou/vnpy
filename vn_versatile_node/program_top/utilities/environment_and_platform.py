# -*- coding: utf-8 -*-
import os,platform,sys
from os import path
from os.path import abspath, sep
from program_top.utilities.my_dir import make_ever_dir

def confirm_platform_info():
	'''
	获取当前平台相关的信息，以字典形式返回出来
	'''
	current_platform_name=platform.platform()
	current_system_category='linux' if 'Linux' in current_platform_name else 'windows'#当前系统类别:windows还是linux
	system_encoding_dict={'linux': 'utf-8', 'windows': 'gb18030', 'osx': 'unicode'}
	current_system_encoding=system_encoding_dict[current_system_category]

	print 'current os:', current_platform_name, 'python版本', platform.python_version(), '操作系统内码:', current_system_encoding, os.linesep

	reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
	sys.setdefaultencoding('utf-8')
	new_encoding=sys.getdefaultencoding()

	platform_info_dict={
		'current_system_category':current_system_category,
		'current_system_encoding':current_system_encoding,
		'graphical_backend':'AGG'#使用的AGG后端
	}
	
	'''
	import matplotlib
	matplotlib.use(platform_info_dict['graphical_backend'])
	'''
	return platform_info_dict
	pass

def get_current_environment_pack():
	'''
	返回所有对应的路径变量，生成平台相关的信息
	'''
	from __main__ import __file__ as entry_file
	start_script_absolute_filename=abspath(entry_file)
	runtime_paths={}
	runtime_paths['start_script_absolute_filename']=start_script_absolute_filename
	start_working_directory_stem=path.split(start_script_absolute_filename)[0]#当前程序的文件夹绝对路径，不包含斜杠
	program_main_dir=start_working_directory_stem+sep
	runtime_paths['program_main_dir']=program_main_dir
	#以下为项目包含文件夹

	resource_dir=program_main_dir+'resource_dir'+sep#资源文件根目录，包括图标，图片
	runtime_paths['resource_dir']=resource_dir
	config_file_dir=program_main_dir+'config_dir'+sep#配置文件根目录
	runtime_paths['config_file_dir']=config_file_dir
	extension_dir=program_main_dir+'extensions'+sep#扩展工具根目录
	runtime_paths['extension_dir']=extension_dir

	#以下为输入输出文件夹
	input_dir=start_working_directory_stem+',input_dir'+sep#输入数据根目录
	runtime_paths['input_dir']=input_dir

	output_dir=start_working_directory_stem+',output_dir'+sep#输出数据根目录
	runtime_paths['output_dir']=output_dir

	buffer_dir=start_working_directory_stem+',buffer_dir'+sep#缓存根目录
	runtime_paths['buffer_dir']=buffer_dir

	current_platform_info=confirm_platform_info()

	return {'runtime_paths':runtime_paths,'current_platform_info':current_platform_info}
	pass

def environment_initialisation(self):
	'''
	单个类的环境初始化：1.创建环境变量包，然后根据环境变量的路径，创建配置文件文件夹(如果不存在)，读入配置文件。创建日志文件夹，创建日志文件
	'''
	
	self._environment_pack=get_current_environment_pack()
	instance_dict={
		'config_file_dir':self._environment_pack['runtime_paths']['config_file_dir']+self.__class__.__name__+os.sep,
		'buffer_dir': self._environment_pack['runtime_paths']['buffer_dir']+self.__class__.__name__+os.sep,
		'output_dir': self._environment_pack['runtime_paths']['output_dir']+self.__class__.__name__+os.sep
	}
	self._environment_pack['instance_path']=instance_dict
	
	for each_path in instance_dict.keys():
		make_ever_dir(instance_dict[each_path])
	pass