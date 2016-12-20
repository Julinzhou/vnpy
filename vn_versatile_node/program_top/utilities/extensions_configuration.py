# -*- coding: utf-8 -*-


from os import sep, remove

try:
	from os import symlink
except:
	pass

from program_top.utilities.my_dir import browse_dir, get_relative_filename_from_absolute
from program_top.utilities.environment_and_platform import get_current_environment_pack

def load_shared_objects(search_parent_path=None):
	'''将扩展根目录中的共享链接库软链接到程序main所在的文件夹'''
	
	current_environment=get_current_environment_pack()
	
	project_path=current_environment['runtime_paths']['program_main_dir']
	
	if not search_parent_path:
		search_parent_path=project_path
		pass
	
	target_so_files=browse_dir(search_parent_path, '.so')
	
	for each_so in target_so_files:
		'''
		如果有什么扩展.so库，就把它创建符号链接到项目文件夹，供搜索
		'''
		relative_so_name=get_relative_filename_from_absolute(each_so)
		symlinked_lib_name=project_path+sep+relative_so_name
		
		try:#无论软链接是否存在，都先删除之
			remove(symlinked_lib_name)
		except:
			pass
		
		try:
			symlink(each_so, symlinked_lib_name)#这里使用绝对地址的目标做链接
		except:
			pass
		pass
	pass