import configparser
import os

# 读配置文件
config = configparser.ConfigParser()
config.read('.env', encoding='utf-8')

# 配置 openai 环境变量
os.environ['OPENAI_BASE_URL'] = config.get('openai', 'base_url')
os.environ['OPENAI_API_KEY'] = config.get('openai', 'api_key')
model_name = config.get('openai', 'model_name')

# 设置代理
http_proxy = config.get('openai', 'http_proxy')
https_proxy = config.get('openai', 'https_proxy')
if http_proxy:
    os.environ['http_proxy'] = http_proxy
if https_proxy:
    os.environ['https_proxy'] = https_proxy
