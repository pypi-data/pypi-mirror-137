# redis的密码,如果没有密码就是''
PASSWORD = ''
HOST = 'localhost'
PORT = '6379'
# 代理池的名称
PROXYPOOL = 'proxies'
# 测试网站
TEST_API = 'https://www.baidu.com/'
TEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
}

# 循环校验时间
CYCLE_VAILD_TIME = 60

# 代理池数量的最小值
LOWER_NUM = 60
# 代理池数量的最大值
UPPER_NUM = 600
# 循环检查添加时间
CHECK_POOL_CYCLE = 60
