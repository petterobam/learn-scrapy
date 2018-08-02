# -*- coding:utf-8 -*-
# python2.0为SimpleHTTPServer
import http.server
# python2.0为SocketServer
import socketserver
# 自定义端口
PORT = 8888
# 服务句柄定义
Handler = http.server.SimpleHTTPRequestHandler
# TCP服务
httpd = socketserver.TCPServer(("", PORT), Handler)
# 启动Web服务
print("Web服务端口为：", PORT)
httpd.serve_forever()