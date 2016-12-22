# -*- coding: utf-8 -*-
from program_top.utilities.ip_and_socket import tcp_gateway
from utilities.environment_and_platform import get_current_environment_pack
from utilities.ip_and_socket import scan_available_ports_then_return,address_string2address_tuple
from datetime import datetime
from utilities.csv_and_json_serialisation import temperarily_load_a_local_json

class vn_event_agent_node(object):
	'''
	事件代理节点，每个工作类产生的事件都往节点里面塞，它应该和工作类在同一个线程/进程中构造
	每一类事件作为集群中的一个订阅topic
	'''
	
	#----------------------------------------------------------------------
	
	def __execute_chain_actions(self, list_of_functions, interverl):
		'''链状以一个时间间隔先后执行列表中的若干函数，可以解决比如CTP查询持仓和资金要有间隔之类的问题，也可以把超时后的应对逻辑加进去'''
		
		pass
	
	def __initialise_cluster(self):
		
		pass
	
	def __seeding_cluster(self):
		'''启动以后要检查潜在的交易网络节点，如果有就加入之，如果3秒超时内没有就初始化本节点作为集群的第一个节点——所谓种子'''
		tuple_address=address_string2address_tuple(self.__config['known_cluster_node'])
		#till here
		
		print self
		
		pass
	
	def __try_timeout_catch(self, timeout_period, catch_action_function):
		'''
		执行某行为，如果超时达到timeout_period，则执行catch_action_function
		'''
		
		pass
	
	def __load_config_file(self, config_file):
		self.__config=temperarily_load_a_local_json(config_file)
		
		self._listening_port=self.__config['listening_port'] if self.__config else scan_available_ports_then_return(
			self._environment_pack['current_platform_info']['current_system_category'])
		pass
	
	def __init__(self, config_file=None):
		"""初始化事件引擎"""
		self._environment_pack=get_current_environment_pack()
		
		if not config_file:
			self._listening_port=scan_available_ports_then_return(
				self._environment_pack['current_platform_info']['current_system_category'])#搜索一个还没有被占用的端口，接下来开始监听
		else:
			self.__load_config_file(config_file)
			pass
		
		self._tcp_gateway=tcp_gateway(self._listening_port, self.__process)
		self.__handlers={}
		self.__topics={}#话题字典，相当于事件字典
		self.__seeding_cluster()
		self.__cluster_map={}#连接
		
		#self.__timer=tornado_timer(emit_interval=timedelta(seconds=3),emit_function=self.__test_emit)
		pass
	
	def __test_emit(self):
		target_port=31416 if self._listening_port==31418 else 31418
		target_string="%s,my port is %d"%(datetime.now().__repr__(), self._listening_port)
		self._tcp_gateway.__send_string("0.0.0.0", target_port, target_string)
		pass
	
	#----------------------------------------------------------------------
	def __run(self):
		"""引擎运行"""
		pass
	
	#----------------------------------------------------------------------
	def __process(self, event):
		'''
		事件入口
		'''
		print event
		pass
	
	#for handler in self.__handlers[event.type_]:
	#handler(event)
	
	#----------------------------------------------------------------------
	def start(self):
		"""引擎启动"""
		# 将引擎设为启动
		pass
	
	#----------------------------------------------------------------------
	def stop(self):
		"""停止引擎"""
		# 将引擎设为停止
		pass
	
	#----------------------------------------------------------------------
	def register(self, type_, handler):
		"""注册事件处理函数监听"""
		# 尝试获取该事件类型对应的处理函数列表，若无则创建
		try:
			handlerList=self.__handlers[type_]
		except KeyError:
			handlerList=[]
			self.__handlers[type_]=handlerList
		
		# 若要注册的处理器不在该事件的处理器列表中，则注册该事件
		if handler not in handlerList:
			handlerList.append(handler)
	
	#----------------------------------------------------------------------
	def unregister(self, type_, handler):
		"""注销事件处理函数监听"""
		# 尝试获取该事件类型对应的处理函数列表，若无则忽略该次注销请求
		try:
			handlerList=self.__handlers[type_]
			
			# 如果该函数存在于列表中，则移除
			if handler in handlerList:
				handlerList.remove(handler)
			
			# 如果函数列表为空，则从引擎中移除该事件类型
			if not handlerList:
				del self.__handlers[type_]
		except KeyError:
			pass
	
	#----------------------------------------------------------------------
	def put(self, event):
		pass
	
	pass