import pymysql
import pymysql.cursors
from DBUtils.PooledDB import PooledDB

_host = '10.200.131.222'
_port = 3306
_userName = 'root'
_pwd = '123456'
_dbName = 'school1'

pool = PooledDB( # 建立池，用于多用户同时访问的流量控制
    creator = pymysql,
    maxconnections = 100,
    mincached = 10,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached = 20,  # 链接池中最多闲置的链接，0和None不限制
    # maxshared = 0,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking = True, # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage = None,  # 一个链接最多被重复使用的次数，None表示无限制
    # 五个要素:
    host = _host, # 服务器所在IP
    port = _port, # 端口号
    user = _userName, # 用户名
    password = _pwd, # 密码
    database = _dbName, # 数据库名

    charset = 'utf8',
    autocommit = True, # 这样不用谢connect commit
    client_flag = pymysql.constants.CLIENT.MULTI_STATEMENTS
    # client_flag = CLIENT.MULTI_STATEMENTS # 允许一条语句中执行多个查询or更新操作
)
# conn = pymysql.connect(
#     host = _host,
#     port = _port,
#     user = _userName,
#     password = _pwd,
#     database = _dbName,
#     charset = "utf8mb4"
# )
conn = pool.connection()
def conMySql(sqlCode): # 连接mysql
    try:
        conn.ping(reconnect=True) # 检查数据库连接正常
        print(sqlCode)
        # 建立游标，对DB发出sql语句
        cursor = conn.cursor(pymysql.cursors.DictCursor) # 返回类型是字典
        cursor.execute(sqlCode) # 执行游标
        conn.commit() # 提交连接
        # conn.close()
        return cursor # 1 True, 0 false
    
    except Exception as er:
        conn.rollback()
        # conn.close()
        return type(er), er

# user = "林忆宁"
# pasw = "123456"
# sql1 = "INSERT INTO login(username, password) VALUES ('%s', '%s')" % (user, pasw)
# sql2 = "select * from login where username = '%s'" % (user)
# ans = conMySql(sql2)
# # conMySql(sql1)
# print(ans.fetchall())