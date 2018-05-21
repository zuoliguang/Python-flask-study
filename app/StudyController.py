#!/usr/bin/python
# -*- coding: UTF-8 -*- 
from flask import Flask, url_for, request # 处理url
from flask import render_template, redirect # 页面输出跳转
from flask import abort, make_response # 页面相应操作
from flask import session, escape # 会话 
from flask import flash # 闪现 
import os, datetime, random, sys # 系统 时间 随机
import Queue
import pytesseract  
from PIL import Image  # 图片
from pyocr import pyocr

app = Flask(__name__)
APP_PATH = os.getcwd() # 根路径
UPLOAD_FOLDER = APP_PATH + '/upload' # 上传路径
STORAGE_FOLDER = APP_PATH + '/storage' # 预存文件路径

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/test')
def test():
    # abort(401)
    # return upload_path
    return render_template('public/page_not_found.html'), 404

# 传递字符串
@app.route('/study/<username>')
def study_show_username(username='none'):
    return 'Username %s' % username

# 传递数字
@app.route('/study/user/<int:uid>')
def study_show_userId(uid):
	return 'User Id %d' % uid

# 跳转
@app.route('/study/redirect')
def study_redirect():
    url = url_for('study_show_userId', uid=1111)
    return redirect(url)

# 获取传参方式
@app.route('/study/med', methods=['GET', 'POST'])
def med_method():
    return request.method

# 静态文件的路由
@app.route('/study/static')
def get_static():
    return url_for('static', filename='test.css')

# 测试模板
@app.route('/study/template/')
@app.route('/study/template/<name>')
def show_page(name=None):
    return render_template('study/hello.html', name=name)

@app.route('/upload_pag')
def upload_pag():
    return render_template('study/upload.html')

# 文件上传
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + str(random.randint(0,100)) + '-' + f.filename
        file_save_path = UPLOAD_FOLDER + '/' + filename
        f.save(file_save_path)
        im = Image.open(file_save_path)
        im.show()
        return '上传完成'
    else:
        return '上传失败或上传方式错误'

# 定制错误信息
@app.route('/error_page')
def error():
    abort(404) # 抛出404的相应错误
    # return render_template('public/page_not_found.html'), 404

# 监听并捕捉错误404，引导至下面的操作
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('public/page_not_found.html'), 404)
    resp.headers['X-Something'] = 'A value' # 再返回时会将该信息添加到响应信息 Response Headers 里面
    return resp

# 缓存会话
@app.route('/cache')
def study_cache():
    session['a'] = 'test1'
    session['b'] = 'test2'
    session['c'] = 'test3'
    return redirect(url_for('show_cache'))

@app.route('/show_cache')
def show_cache():
    res_str = ''
    if 'a' in session:
        res_str += 'session-a : ' + session['a'] + '<br/>'
        session.pop('a', None) # 删除 session
    if 'b' in session:
        res_str += 'session-b : ' + session['b'] + '<br/>'
        session.pop('b', None) # 删除 session
    if 'c' in session:
        res_str += 'session-c : ' + session['c'] + '<br/>'
        session.pop('c', None) # 删除 session
    return res_str

@app.route('/get_scret_key')
def get_scret_key():
    return os.urandom(24)

# 队列queue
@app.route('/study_queue')
def study_queue():
    ### 一、先进先出 ###
    # str = ''
    # q = Queue.Queue()
    # for i in range(10):
    #     q.put(i)
    # for i in range(10):
    #     str += '%d => ' % q.get()
    # return str # 0 => 1 => 2 => 3 => 4 => 5 => 6 => 7 => 8 => 9 =>

    ### 二、后进先出 ###
    # str = ''
    # q = Queue.LifoQueue()
    # for i in range(10):
    #     q.put(i)
    # for i in range(10):
    #     str += '%d => ' % q.get()
    # return str # 9 => 8 => 7 => 6 => 5 => 4 => 3 => 2 => 1 => 0 =>

    ### 三：按优先标志位读取 ###
    # str = ''
    # p = Queue.PriorityQueue()
    # p.put((3,"3"))
    # p.put((1,"1"))
    # p.put((4,"4"))
    # p.put((2,"2"))
    # size = p.qsize()
    # for i in range(size):
    #     str += '%s => ' % p.get()[1]
    # return str # 1 => 2 => 3 => 4 =>
    # 排列顺序 
    # (1, '1')
    # (2, '2')
    # (3, '3')
    # (4, '4')
    
    ### 四：多元组判断 ###
    str = ''
    p = Queue.PriorityQueue()
    p.put((1, 4, "a"))
    p.put((2, 1, "666"))
    p.put((1, 3, "4"))
    p.put((2, 2, "2"))
    p.put((1, 9, "9"))
    size = p.qsize()
    for i in range(size):
        str += '%s => ' % p.get()[2]
    return str # 4 => a => 9 => 666 => 2 =>
    # 排列顺序 
    # (1, 3, "4")
    # (1, 4, "a")
    # (1, 9, "9")
    # (2, 1, "666")
    # (2, 2, "2")

# Python之图片OCR识别
@app.route('/study_ocr')
def study_ocr():
    file = STORAGE_FOLDER + "/test5.png"
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    tools = pyocr.get_available_tools()[:]
    if len(tools) == 0:
        return "No OCR tool found"
    image = Image.open(file)
    text = tools[0].image_to_string(image, lang='eng')
    return text


if __name__ == '__main__':
    app.secret_key = 'zlgcg'
    app.debug = True # 开启调式模式
    app.run(host='0.0.0.0')