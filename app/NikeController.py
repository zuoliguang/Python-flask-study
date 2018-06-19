#!/usr/bin/python
# -*- coding: UTF-8 -*- 
from flask import Flask, url_for, request # 处理url
from flask import render_template, redirect # 页面输出跳转
from flask import abort, make_response # 页面相应操作
from flask import session, escape # 会话 
from flask import flash # 闪现 
import os, json, datetime, random, md5, math # 系统 时间 随机 ...
import Queue # 队列变量
from PIL import Image  # 图片
from pyocr import pyocr # 文字识别
import urllib2 # 远程访问
import re # 正则匹配
from bs4 import BeautifulSoup

app = Flask(__name__)
APP_PATH = os.getcwd() # 根路径
UPLOAD_FOLDER = APP_PATH + '/upload' # 上传路径
STORAGE_FOLDER = APP_PATH + '/storage' # 预存文件路径

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/nike_list')
def nike_list():
    allurl = 'https://www.nike.com/cn/launch/?p=' + str(1)
    response = urllib2.urlopen(allurl)
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return html

if __name__ == '__main__':
    app.secret_key = 'zlgcg'
    app.debug = True # 开启调式模式
    app.run(host='0.0.0.0')