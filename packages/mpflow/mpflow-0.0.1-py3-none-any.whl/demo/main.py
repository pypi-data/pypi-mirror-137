from mpflow import Context
import yaml

# 加载配置
with open('config.yml', 'r') as f:
    conf = yaml.safe_load(f.read())

# 初始化全局上下文
c = Context(conf)
# 开始运行
c.start()
