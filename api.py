
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import logging
import logging.config
import config
import os
import redis
import time


app = Flask(__name__)
api = Api(app)





#
class MVBacktest(Resource):
    '''
    该接口运用马克维茨的均值方差策略进行回测,返回回测结果
    改接口不考虑佣金
    '''
    def get(self):

        pass

    def checkArgs(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start', required=True)
        parser.add_argument('end', required=True)
        parser.add_argument('codes', required=True)
        parser.add_argument('lb')
        parser.add_argument('ub')
        parser.add_argument('reblanceFreq', required=True)  # 调仓周期
        parser.add_argument('lookback', default=250)  # 用多长的历史数据
        parser.add_argument('base', default=['SHSN300'])
        args = parser.parse_args()

        codes = args['codes'].split(',')
        lb = args['lb'].split(',') if args['lb'] else [0 for _ in range(len(codes))]
        ub = args['ub'].split(',') if args['ub'] else [1 for _ in range(len(codes))]
        if not (len(codes) == len(lb) and len(lb) == len(ub)):
            abort(404, message="codes,lb,ub 's length must align")
        if not isinstance(args['base'], list):
            args['base'] = args['base'].split(',')

        args['codes'] = args['codes'].split(',')
        args['lb'] = args['lb'].split(',')
        args['ub'] = args['ub'].split(',')

        return args

##
## Actually setup the Api resource routing here
##
api.add_resource(MVBacktest, '/backtest')


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('use: python api.py [dev|test|prod]来启动程序')
    #初始化日志配置
    if not os.path.exists("logs"):
        os.makedirs("logs")
    logging.config.fileConfig('conf/log.prop')
    #初始化环境配置
    filename = "conf/config_%s.cfg" % sys.argv[1]
    config.init(filename)


    app.run(host='0.0.0.0',debug=True)