import requests
import lxml
import logging
import utils
import config
import jinja2
from jinja2 import Environment,FileSystemLoader
from time import sleep

utils.set_logconf()
config.init("conf/config_dev.cfg")


questions = [
    '连续3天价升量缩，收盘价>开盘价，最近3天的涨幅小于5%，dde大单净量>0.28%，上市板块不包含创业板，股票简称不包含st，boll未突破上轨',
    '前2天涨跌幅小于-5%；跳空高开；振幅小于2%；非创业',
    '振幅大于16%，涨停，ARBR大于85小于239，2日均线3日均线多头排列，市净率大于2.8，市销率大于0，量价齐升，流通市值大于18.5亿小于450亿，BOLL未突破上轨，K大于32，资产负债率小于79%，近2个月的区间上榜次数大于0次',
    '底部反转，总市值小于30亿+；不包含st；无退市预警；非停牌，非涨停，非创业板，总市值从小到大排名；'
]

base_url = 'http://www.iwencai.com/stockpick/search'

results = {}
for q in questions:

    logging.info("获取问句:%s的股票" % q)
    params = {
        'w':q
    }

    rval = requests.get(base_url,params=params)
    if rval.status_code==200:

        from lxml import etree
        html = etree.HTML(rval.content)
        elements = html.xpath('//td/div[@class="em graph alignCenter graph"]/a')
        stock_names = []
        for e in elements:
            stock_name = e.text
            stock_names.append(stock_name)

        results[q] = stock_names

logging.info("选出的iwencai的股票有 %s" % results)
addrs = config.get('email','receive_email_addr').split(',')

env = Environment(loader=FileSystemLoader('template'))
email_temp = env.get_template('email_template.html')
html = email_temp.render(results=results)

logging.info("发送邮件到邮箱%s" % addrs)
i=0
while True:
    try:
        subject = config.get('email','subject')
        body = html
        format = 'html'
        utils.send_mail_qq(addrs, subject, body, format='html')
        logging.info("发送邮件成功")
        break
    except Exception as e:
        i += 1
        if i > 3:
            break
        print('exception',e)
        sleep(10)
        print('send again')
        format = 'plain'
        continue

