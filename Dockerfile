FROM centos:7

RUN pip3 install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com -r requirements.txt

CMD [ "python3", "/crawler_job.py", 'dev']
