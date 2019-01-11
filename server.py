# -*- coding:utf-8 -*-

"""File Upload API"""
import os
import sys

import datetime
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen

from infer import Classify
default_encoding = 'utf-8'

from tornado.options import define, options
import json
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

define("port", default=48703, help="run on the given port", type=int)

global classify


class BaseHandler(tornado.web.RequestHandler):
    """
    Base Handler for other Request Handler
    """

    def check_ip(self):
        # if self.request.remote_ip[:10] == '192.168.1.':
        #     return True

        return True

    def prepare(self):
        if self.check_ip() is False:
            raise HTTPError(405, reason="invalid ip")

    def on_response(self, response):
        callback = self.get_argument("callback", None)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', '*')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Headers', '*')
        if callback is not None:
            response = str(callback) + '(' + json.dumps(response) + ')'
        else:
            response = json.dumps(response)
        self.write(response)


class ClassifyHandler(BaseHandler):
    """查询接口

    http://127.0.0.1:48703/api/classify

    """


    def post(self):
        _reply = dict()
        _reply['status'] = 0
        _reply['message'] = 'ok'
        metas = self.request.files
        
        date = datetime.datetime.now().strftime('%Y%m%s')
        # save to file_dir
        file_dir = './api_data'
        if os.path.exists(file_dir) is False:
            os.mkdir(file_dir)

        predicts = []
        global classify
        try:
            for fname, fbody in metas.iteritems():
                mfb = fbody[0]
                records = mfb['filename'].split('/')[-1].split('.')[0]
                save_name = '%s/%s_%s.jpg' % (file_dir, date, '_'.join(records))
                with open(save_name, 'wb') as fp:
                    fp.write(mfb['body'])
                print 'predict: %s' % save_name
                predicts.append(classify.predict(save_name))
        except:
            _reply['status'] = -100
            _reply['message'] = 'upload file error'
        else:
            _reply['predicts'] = predicts
        print json.dumps(_reply)
        self.on_response(_reply)
        self.finish()



def start_server():
    global classify
    classify = Classify()
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/api/classify", ClassifyHandler)])
    print "start server at %s" % options.port
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    if sys.getdefaultencoding() != default_encoding:
        reload(sys)
        sys.setdefaultencoding(default_encoding)

    start_server()
