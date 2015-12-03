#-*- coding: utf-8 -*-
#!/usr/bin/env python

import webapp2
import os
import urllib
import json
import logging

from google.appengine.ext.webapp import template
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import model

def handle_404(request, response, exception):
    # 將 Exception 訊息顯示出來, import logging
    logging.exception(exception)

    # 指定一個頁面輸出
    path = os.path.join(os.path.dirname(__file__), '404.html')
    response.out.write(template.render(path, {}))
    response.set_status(404)

class MainHandler(webapp2.RequestHandler):
    def get(self):

        # 取得參數 name 的值
        name = self.request.get("name", "World")

        # 這邊設定要傳入頁面的參數 name，值為 Seth
        template_values = {
            'name': name
        }

        # 指定 index.html 作為輸出的頁面
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class PostHandler(webapp2.RequestHandler):

    def post(self):

        name = self.request.POST['name']

        template_values = {
            'name': name
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class UploadFilePage(webapp2.RequestHandler):
    def get(self):

        # 取得已上傳的檔案
        files = blobstore.BlobInfo.all();

        # 建立一個 Blobstore 的上傳路徑
        upload_url = blobstore.create_upload_url('/upload')

        # 將 Blobstore 上傳路徑傳至頁面表單的 action 屬性
        values = {"upload_url": upload_url, "files": files}

        # 上傳完成後會導回此頁，並將相關參數傳入，利用參數顯示檔案名稱、預覽檔案
        if len(self.request.query) > 0:
            values['filename'] = self.request.params['filename']
            values['filekey'] = self.request.params['filekey']
            values['filetype'] = self.request.params['filetype']
            values['filesize'] = self.request.params['filesize']

        # 輸出畫面
        path = os.path.join(os.path.dirname(__file__), 'uploadfile.html')
        self.response.out.write(template.render(path, values))

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):

        if len(self.get_uploads()) == 0:
            self.response.write('No file to upload')
        else:
            # 取得已上傳檔案的 BlobInfo 物件
            file = self.get_uploads()[0]
            # 將已上傳檔案的資訊紀錄一起導回 uploadfile.html，
            query = "filename=" + urllib.quote(file.filename) + "&filekey="+str(file.key()) + "&filetype="+ file.content_type + "&filesize="+ str(file.size)

            book = model.InsertBook(file.filename, 'Alex_'+ str(file.key()))

            self.redirect("/uploadfile?" + query)

class ServeFileHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, filekey):
        # 利用 Blob key 來取得檔案
        if not blobstore.get(filekey):
            self.error(404)
        else:
            self.send_blob(filekey)

class deleteFileHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'

        result = {
            "status": 0,
            "msg": None
        }

        blobKey = self.request.get("blobKey", "")

        if blobKey != "":
            blobstore.delete(blobKey)
            result['status'] = 1
        else:
            result['status'] = 0
            result['msg'] = 'blobKey is null'

        self.response.out.write(json.dumps(result))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/post', PostHandler),
    ('/upload', UploadHandler),
    ('/uploadfile', UploadFilePage),
    ('/servefile/([^/]+)?', ServeFileHandler),
    ('/deletefile', deleteFileHandler),
], debug=True)

app.error_handlers[404] = handle_404
