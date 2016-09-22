#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
一个使用github webhook 自动更新网站的脚本
首先需要设置环境变量`export GH_SECRET_TOKEN='your secret token'`, 
GH_SECRET_TOKEN 可以使用 `ruby -rsecurerandom -e 'puts SecureRandom.hex(20)'` 生成 
"""

import os
import subprocess
import json
import hmac
from http.server import HTTPServer, BaseHTTPRequestHandler

work_dir = '/home/liuenyan/django-blog'

class WebhooksRequestHandler(BaseHTTPRequestHandler):
    """
    一个用于处理 http 请求的类
    """
    def get_body(self):
        if not hasattr(self, 'body_content'):
            print("msg attribute is not found")
            self.body_content = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        return self.body_content

    def is_valid_signature(self):
        method, hashsum = self.headers.get("X-Hub-Signature", "").split('=')
        key = os.environ.get('GH_SECRET_TOKEN').encode('utf-8')
        msg = self.get_body()
        hashsum1 = hmac.new(key, msg, method).hexdigest()
        if hashsum1 == hashsum:
            return True
        else:
            return False

    def is_valid_request(self):
        if not self.headers.get("User-Agent", "").startswith("GitHub-Hookshot/"):
            print("Invalid User-Agent.")
            return False
        elif not self.headers.get("Content-Type", "")=="application/json":
            print("Invalid Content Type.")
            return False
        elif not self.is_valid_signature():
            print("Invalid X-Hub-Signature.")
            return False
        else:
            return True

    def deploy_site(self):
        event = self.headers.get("X-GitHub-Event")
        if event == "ping":
            print("Receive ping request.")
            #data = json.loads(self.get_body(), sort_keys=True, indent=4)
            #print(data)
            self.send_response(200, "OK")
            self.end_headers()
        elif event == "push":
            # run git pull command
            print("receive pull request.")
            os.chdir(workdir)
            try:
                subprocess.run("git pull", shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print("[git pull] command return ", e.returncode)
                self.send_error(500)
            else:
                self.send_response(200)
                self.end_headers()
        else:
            self.send_error(403) 

    def do_GET(self):
        print(self.requestline)
        print(self.headers)
        self.send_error(404) 

    def do_POST(self):
        print(self.requestline)
        print(self.headers)
        if self.path == '/deploy' and self.is_valid_request():
            self.deploy_site()
        else:
            self.send_error(404) 


if __name__ == '__main__':
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, WebhooksRequestHandler)
    httpd.serve_forever()
