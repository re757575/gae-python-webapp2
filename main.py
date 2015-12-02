#-*- coding: utf-8 -*-
#!/usr/bin/env python

import webapp2
import os
from google.appengine.ext.webapp import template

class MainHandler(webapp2.RequestHandler):
    def get(self):

        # 取得參數 name 的值
        name = self.request.get("name")

        # 取得所有參數
        self.request.GET

        # 取得參數 name 的值，若有兩個 name 參數則顯示最後一個
        self.request.GET['name']

        # 取得所有名為 name 參數值
        self.request.GET.getall('name')

        # 取得所有參數
        self.request.GET.items()

        # 這邊設定要傳入頁面的參數 name，值為 Seth
        template_values = {
            'name': name
        }

        # 指定 index.html 作為輸出的頁面
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
