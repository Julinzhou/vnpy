# -*- coding: utf-8 -*-

import sys

class TailRecurseException:
    """尾递归异常类"""
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

def tail_call_optimized(g):
    """
    This function decorates a function with tail call
    optimization. It does this by throwing an exception
    if it is it's own grandparent, and catching such
    exceptions to fake the tail call optimization.

    This function fails if the decorated
    function recurses in a non-tail context.
    """
    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back \
            and f.f_back.f_back.f_code == f.f_code:
            # 抛出异常
            raise TailRecurseException(args, kwargs)
        else:
            while 1:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException, e:
                    # 捕获异常，重新调用栈
                    args = e.args
                    kwargs = e.kwargs
    func.__doc__ = g.__doc__
    return func
	
def merge_dicts(list_of_dicts_to_merge):
	'''合并所有dict'''
	empty_dict={}
	
	for each_dict in list_of_dicts_to_merge:
		empty_dict.update(each_dict)
		pass
	return empty_dict
	pass

#@tail_call_optimized
def nested_dict_apply(target_data_for_json, operation_function=None, ignore_key=False,set_or_list=False):
	'''
	对层叠的dict结构逐层撸一遍函数，然后返回转化后的dict结构，遇到set要转化成list，方便以json字符串形式传递，如果没有应用函数，则只做set转化，递归执行，并且选择是否忽略其中字典的key，默认不忽略
	'''
	
	if isinstance(target_data_for_json, list) or (isinstance(target_data_for_json, set)):#如果是列表或者字典，则列表解析其中的每个成员，并根据参数返回列表或者集合
		target=[nested_dict_apply(item, operation_function) for item in target_data_for_json]
		return target if not set_or_list else set(target)
		
	if isinstance(target_data_for_json, dict):#如果忽略字典key，则字典key不做function操作，否则对字典key也做function操作，使用字典解析
		if ignore_key:
			return {nested_dict_apply(key, None,ignore_key): nested_dict_apply(value, operation_function,ignore_key) for key, value in target_data_for_json.iteritems()}
		else:
			return {nested_dict_apply(key, operation_function,False): nested_dict_apply(value, operation_function,False) for key, value in target_data_for_json.iteritems()}
			pass
	
	#如果既不是列表又不是字典还不是集合，则对数据执行操作并得到返回值
	if operation_function:#定义了操作则操作数据并返回
		return operation_function(target_data_for_json)
	else:#没有定义操作则直接返回
		return target_data_for_json
	pass