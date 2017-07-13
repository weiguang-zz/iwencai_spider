FROM python:3

WORKDIR /app

ADD . /app

RUN python --version

RUN pip3 install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com -r requirements.txt

EXPOSE 5000

RUN mkdir logs

CMD ["python", "crawler_job.py", "dev"]
