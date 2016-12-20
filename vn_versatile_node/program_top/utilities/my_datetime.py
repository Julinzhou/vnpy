# -*- coding: utf-8 -*-

from __future__ import division
import datetime,time
from math import floor

my_date_time_microsec_format='%Y-%m-%d-%H:%M:%S.%f'#yyyy-mm-dd-HH:MM:SS.microsecond
my_date_time_without_micro='%Y-%m-%d-%H:%M:%S'#yyyy-mm-dd-HH:MM:SS
my_quant_time_format='%Y-%m-%d %H:%M:%S'#掘金时间格式yyyy-mm-dd HH:MM:SS
my_quant_time_stamp_format='%Y-%m-%dT%H:%M:%S+08:00'#掘金时间戳格式yyyy-mm-ddTHH:MM:SS+08:00
data_buffer_time_format='%Y-%m-%d-%H-%M-%S.%f'#数据缓存文件时间格式yyyy-mm-dd-HH-MM-SS.μs
data_buffer_date_format='%Y-%m-%d'#数据缓存文件日期格式yyyy-mm-dd
date_contract_format='%Y%m'#期货合约年月格式,yyyymm，只能根据此输出，不能导入

vn_on_order_time='%H:%M:%S'#vn.py的订单回报HH:MM:SS

derby_elasticsearch_date_format='%Y%m%d'#elasticsearch日期格式yyyymmdd
derby_perflog_timestamp_format='%Y-%m-%d-%H:%M:%S.%f-%Z'#年月日时分秒-时区

def posix_timestamp2datetime(utc_float_time):
	'''输入utc_posix时间戳，返回本机所在时区的datetime时间'''
	int_utc_sec=int(utc_float_time)
	millisec_float=int(1000*(utc_float_time-int_utc_sec))
	time_t=time.localtime(int_utc_sec)
	final_datetime=datetime.datetime(time_t.tm_year,time_t.tm_mon,time_t.tm_mday,time_t.tm_hour,time_t.tm_min,time_t.tm_sec,millisec_float*1000)
	return final_datetime
	
def my_date_time_string2datetime(time_string):
	return datetime.datetime.strptime(time_string, my_date_time_without_micro)

#返回月首日期
def get_month_1st_date(target_date=datetime.datetime.today().date()):
	return datetime.date(target_date.year,target_date.month,1)

#返回n年后的同一天
def get_same_day_in_next_n_year(target_date=datetime.datetime.today().date(),n=1):
	if target_date.month==2 and target_date.day==29:
		return datetime.date(target_date.year+n,2,28)#如果输入日期是2月29日，则返回n年后的2月28日
	return datetime.date(target_date.year+n,target_date.month,target_date.day)
#返回n月后的同一天

def get_same_day_in_next_n_month(target_date=datetime.datetime.today().date(),n=1):
	new_month=target_date.month+1
	new_year=target_date.year
	if new_month>12:#如果大于12了，则进位
		new_month=1
		new_year+=1
	if n>1:#如果n为1，返回下个月本日
		return get_same_day_in_next_n_month(datetime.date(new_year,new_month,1),n-1)
	else:
		return datetime.date(new_year,new_month,1)

def get_day_start(target_date):
	'''返回某个日期的开始时刻'''
	day_start_time=datetime.time()
	return datetime.datetime.combine(target_date,day_start_time)

def timedelta_division(divided_timedelta,dividing_timedelta):
	'''时间差除法，返回tuple，分别是商和余数'''
	mutiple=divided_timedelta.total_seconds()/dividing_timedelta.total_seconds()
	integer_part=int(floor(mutiple))
	residual=divided_timedelta-integer_part*dividing_timedelta
	return (integer_part,residual)

def datetime2posix_timestamp(target_datetime,time_zone=None):
	'''输入datetime，如果指定时区以该时区来理解datetime，如果没有指定时区，以datetime自带的时区信息解析，如果两个时区信息都没有，以本机所在时区解析
	然后将datetime转化为unix秒时间戳
	'''
	microsecond_part=target_datetime.microsecond
	time_tuple=target_datetime.timetuple()
	int_part=time.mktime(time_tuple)
	float_part=0.000001*microsecond_part
	posix_time=int_part+float_part
	return posix_time
	
	'''
	restored_dt=datetime.datetime.utcfromtimestamp(posix_time)
	restored_dt_2=datetime.datetime.fromtimestamp(posix_time)
	restored_dt_3=posix_timestamp2datetime(posix_time)
	'''
	
	
	
	
	pass

def get_latest_bar_start(bar_period,target_moment=datetime.datetime.now()):
	'''取得最近一个bar的结束时点，不注明则默认为当前时刻'''
	today=target_moment.date()
	day_start=get_day_start(today)
	timedelta_of_today=target_moment-day_start
	integer_part, residual=timedelta_division(timedelta_of_today, bar_period)
	current_bar_start=day_start+integer_part*bar_period#当前未走完的最新bar的开始点，初始化历史数据面板就从这里开始
	return current_bar_start