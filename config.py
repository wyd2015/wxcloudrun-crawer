import os

# 是否开启debug模式
DEBUG = True

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", '5GWtdSJm')
db_address = os.environ.get("MYSQL_ADDRESS", '10.33.111.73:3306')
