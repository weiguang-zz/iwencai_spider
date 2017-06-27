#配置类,应用启动的时候根据运行的环境进行初始化
import logging
from configparser import ConfigParser

cf = None
def init(filename):
    import os
    if not os.path.isfile(filename):
        raise Exception('file not exists:%s' % filename)
    logging.info("初始化配置文件:%s" % filename)
    global cf
    cf = ConfigParser()
    cf.read(filename)

def get(sec, prop):
    if cf:
        return cf.get(sec, prop)
    else:
        raise Exception('initialize first')


if __name__=="__main__":
    init("conf/config_dev.cfg")
    print(cf.get('db','host'))