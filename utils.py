#coding=utf8
import os
import logging
import mimetypes
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
import json
import codecs
from xml.dom import minidom
import os
import logging.config

def synchronized(lock):
    """ Synchronization decorator. """

    def wrap(f):
        def newFunction(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return newFunction
    return wrap


def get_module_path():
    return os.path.dirname(__file__)

def get_absolute_path(path):
    return os.path.join(os.path.dirname(__file__),path)

def send_mail(to_list, subject, body, format='plain', attachFileName=None):
    # if isinstance(body, unicode):
    #     body = str(body)
    fromMail = "13240811524@163.com"
    me = ("%s<" + fromMail + ">") % (Header("自动邮件通知", 'utf-8'),)

    outer = MIMEMultipart()

    # if not isinstance(subject, unicode): python3默认使用Unicode编码
    #     subject = unicode(subject)
    outer['Subject'] = subject
    outer['From'] = me
    outer['To'] = ";".join(to_list)
    outer["Accept-Language"] = "zh-CN"
    outer["Accept-Charset"] = "ISO-8859-1,utf-8"

    if attachFileName:
        ctype, encoding = mimetypes.guess_type(attachFileName)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(attachFileName, 'rb') as fp:
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(fp.read())

        encoders.encode_base64(msg)

        fileName = attachFileName[(attachFileName.rfind('/') + 1):]
        msg.add_header('Content-Disposition', 'attachment', filename=fileName)
        outer.attach(msg)

    textPart = MIMEText(body, format, 'utf-8')
    outer.attach(textPart)

    try:
        s = smtplib.SMTP('smtp.163.com')
        # s.connect("")
        s.login("13240811524@163.com", "4306364abc")
        s.sendmail(outer['From'], to_list, outer.as_string())
        s.close()
        return True
    except Exception as e:
        logging.info('send email error',e)
        return False

def send_mail_163(to_list, subject, body, format='plain'):
    try:
        msg = MIMEText(body, format, 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')

        # 报错原因是因为“发件人和收件人参数没有进行定义
        msg['from'] = '13240811524@163.com'
        msg['to'] = ";".join(to_list)

        smtp = smtplib.SMTP()
        smtp.connect("smtp.163.com")
        smtp.login("13240811524@163.com", "4306364abc")
        smtp.sendmail("13240811524@163.com", to_list, msg.as_string())
        smtp.quit()
        logging.info('邮件发送成功email has send out !')
    except Exception as e:
        logging.error("send mail error", e)


def set_logconf():
    #获取的是相对于执行路劲的相对目录，如执行python a.python，则ppath是None
    ppath=os.path.dirname(__file__)

    #logging的配置
    logging.config.fileConfig(ppath+"/conf/log.prop" if ppath else "conf/log.prop")

    os.chdir(ppath)#设置执行目录为项目的主目录

if __name__=='__main__':
    set_logconf()
    send_mail_163(['812674168@qq.com'],'雄安新区打开涨停板的股票',"你好, FYI")


