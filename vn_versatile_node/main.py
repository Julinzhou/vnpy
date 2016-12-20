# -*- coding: utf-8 -*-

if __name__ == '__main__':
	from tornado.ioloop import IOLoop
	from program_top.utilities.environment_and_platform import get_current_environment_pack
	environment_pack=get_current_environment_pack()
	
	IOLoop.current().start()
	pass