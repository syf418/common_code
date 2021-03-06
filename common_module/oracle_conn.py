# -*- coding: utf-8 -*-
# @Time: 2020/3/25 10:46
import warnings
warnings.filterwarnings(action="ignore")

import os
os.environ['NLS_LANG']='AMERICAN_AMERICA.ZHS16GBK'

import pandas as pd
from pandas import DataFrame
import cx_Oracle
import traceback

from common_project.common_module.config_module import get_config
from common_project.common_module.logging_module import logging_func
logger = logging_func()

# configuration
rac_cluster = False

Oracle_info = get_config("Oracle")
db_username = Oracle_info["db_username"]
db_password = Oracle_info["db_password"]
db_host = Oracle_info["db_host"]
db_service_name = Oracle_info["db_service_name"]
if rac_cluster:
    dsn = Oracle_info["dsn"]

'''
dsn sample：
     (DESCRIPTION =
    (ADDRESS_LIST =
      (FAILOVER = ON)
      (LOAD_BALANCE = OFF)  
        (ADDRESS = (PROTOCOL = TCP)(HOST = xxx.xxx.x.xxx)(PORT = 1521))	
     	(ADDRESS = (PROTOCOL = TCP)(HOST = xxx.xxx.x.xxx)(PORT = 1521))
    	(ADDRESS = (PROTOCOL = TCP)(HOST = xxx.xxx.x.xxx)(PORT = 1521))
    	(ADDRESS = (PROTOCOL = TCP)(HOST = xxx.xxx.x.xxx)(PORT = 1521))
    )
    (CONNECT_DATA =
    	(SERVER = DEDICATED)
    	(FAILOVER_MODE=(TYPE=select)(METHOD=basic))
    	(INSTANCE_ROLE = ANY)
    	(SERVICE_NAME = pdb_ipms)
    )
  )
'''

# connect to Oracle
def connect_oracle(sql_text):
    if not rac_cluster:
        conn = cx_Oracle.connect(user_info)
    else:
        db1 = cx_Oracle.connect(str(db_username), str(db_password), dsn=str(dsn))
    print("数据库已成功连接...", flush=True)
    logger.info("Database connection successful!")
    cursor = conn.cursor()
    try:
        cursor.execute(sql_text)
        result = cursor.fetchall()
        # 获取表字段
        title = [i[0] for i in cursor.description]
        df = pd.DataFrame(result, columns=title)
        return df
    except BaseException as e:
        logger.exception("An exception occurred to the data acquisition!")
        logger.exception(str(traceback.print_exc()))
        cursor.close()
        conn.close()
        return None

# insert into table
def insert_into_oracle(df:DataFrame,  insert_sql:str):
    if not rac_cluster:
        conn = cx_Oracle.connect(user_info)
    else:
        db1 = cx_Oracle.connect(str(db_username), str(db_password), dsn=str(dsn))
    print("数据库连接成功...", flush=True)
    logger.info("Database connection successful!")
    cursor = conn.cursor()
    try:
        result = df.values.tolist()
        cursor.prepare(insert_sql)
        cursor.executemany(None, result)
        cursor.close()
        conn.commit()
        conn.close()
        logger.info("Data successfully inserted!")
    except:
        logger.exception("An exception occurred to the data insertion!")
        logger.exception(str(traceback.print_exc()))
        cursor.close()
        conn.close()
