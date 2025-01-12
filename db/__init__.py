import pymysql
import pymysql.cursors
from dbutils.pooled_db import PooledDB
from dotenv import load_dotenv

import os

load_dotenv()

pool = PooledDB(  # 建立池，用于多用户同时访问的流量控制
    creator=pymysql,
    maxconnections=100,
    mincached=10,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=20,  # 链接池中最多闲置的链接，0和None不限制
    # maxshared = 0,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制

    host=os.environ['DB_HOST'],  # 服务器所在IP
    port=int(os.environ['DB_PORT']),  # 端口号
    user=os.environ['DB_USERNAME'],  # 用户名
    password=os.environ['DB_PASSWORD'],  # 密码
    database=os.environ['DB_DATABASE'],  # 数据库名

    charset='utf8',
    autocommit=True,  # 这样不用谢connect commit
    client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS
    # client_flag = CLIENT.MULTI_STATEMENTS # 允许一条语句中执行多个查询or更新操作
)

connection = pool.connection()

def invoke(sql):  # 连接mysql
    connection.ping(reconnect=True)  # 检查数据库连接正常
    print(sql)
    # 建立游标，对DB发出sql语句
    cursor = connection.cursor(pymysql.cursors.DictCursor)  # 返回类型是字典
    cursor.execute(sql)  # 执行游标
    connection.commit()  # 提交连接
    return cursor

def invoke_insertion(sql):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    last_id = cursor.lastrowid
    connection.commit()
    return last_id
