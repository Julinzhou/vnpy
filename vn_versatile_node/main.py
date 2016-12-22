# -*- coding: utf-8 -*-

from program_top.utilities.environment_and_platform import get_current_environment_pack
from program_top.utilities.my_dir import make_ever_dir
from tornado.ioloop import IOLoop

if __name__ == '__main__':
	environment_pack=get_current_environment_pack()
	make_ever_dir(environment_pack['runtime_paths']['config_file_dir'])
	
	
	
	IOLoop.current().start()
	pass