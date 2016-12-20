# -*- coding: utf-8 -*-


from program_top.utilities.data_container_operations import nested_dict_apply
from utilities.string_and_unicode import to_string_if_unicode
from sqlalchemy import create_engine,MetaData,inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlalchemy_dialect={
	'microsoft':'mssql+pymssql'
}

def quick_mapper(table):
	Base = declarative_base()
	class GenericMapper(Base):
		__table__ = table
		pass
	return GenericMapper

class sql_session(object):
	def __init__(self,db_config):
		
		dialect=sqlalchemy_dialect[db_config['db_type']]
		db_info=db_config['db_name']
		uid=db_config['login_name']
		pwd=db_config['password']
		sqlalchemy_connection_string='%s://%s:%s@%s:%d/%s'%(dialect,uid,pwd,db_config['host'],db_config['port'],db_info)
		
		pyodbc_string='%s://%s:%s@%s/%s?port=%d'%(dialect,uid,pwd,db_config['host'],db_info,db_config['port'])
		
		
		self.make_session(sqlalchemy_connection_string)
		pass
		
	def make_session(self,connection_string):
		engine=create_engine(connection_string, echo=False, convert_unicode=False,encoding='utf-8')
		Session=sessionmaker(bind=engine)
		self.session=Session()
		self.engine=engine
		
		convention={"ix": 'ix_%(column_0_label)s', "uq": "uq_%(table_name)s_%(column_0_name)s"}
		
		self.metadata=MetaData(bind=self.engine,naming_convention=convention)
		pass
	
	def list_all_tables(self):
		inspector=inspect(self.engine)
		table_names=nested_dict_apply(inspector.get_table_names(),to_string_if_unicode)
		return table_names
	pass



def pyodbc_row_record2dict(pyodbc_record):
	'''将pyodbc的一行查询结果变成字典'''
	columns=[column[0] for column in pyodbc_record.cursor_description]
	a_result=dict(zip(columns, pyodbc_record))
	return a_result




class ms_sql_adapter(object):
	def __init__(self,db_config):
		super(ms_sql_adapter, self).__init__()
		connection_driver_info='{SQL Server}'
		server_info=db_config['host']+','+str(db_config['port'])+'\\'+db_config['db_instance_name']
		db_info=db_config['db_name']
		uid=db_config['login_name']
		pwd=db_config['password']
		#dialect+driver://username:password@host:port/database
		
		sqlalchemy_connection_string='mssql+pyodbc://%s:%s@%s:%d/%s'%(uid,pwd,db_config['host'],db_config['port'],db_config['db_instance_name'])
		
		self.__current_engine=create_engine(sqlalchemy_connection_string)
		self.metadata=MetaData(self.__current_engine)
		
		
		
		pass
	
	def scan_all_tables(self):
		
		
		
		all_tables=self.mssql_cur.tables()
		
		table_list=[]
		
		for rows in all_tables:
			if rows.table_type=='TABLE':
				table_list.append(rows.table_name)
			else:
				#print rows
				pass
			pass
		all_tables_result=nested_dict_apply(target_data_for_json=table_list, operation_function=to_string_if_unicode)
		return all_tables_result
	pass