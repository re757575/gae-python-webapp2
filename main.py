#-*- coding: utf-8 -*-
#!/usr/bin/env python

import webapp2
import os
from google.appengine.ext.webapp import

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # 這邊設定要傳入頁面的參數 name，值為 Seth
        template_values = {
            'name': 'Seth'
        }

        # 指定 index.html 作為輸出的頁面
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
