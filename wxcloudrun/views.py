from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


@app.route('/api/price/type', methods=['GET', 'POST'])
def get_price_type():
    return make_succ_response(['FUEL'])


@app.route('/api/price/fuel', methods=['POST'])
def get_fuel_price():
    headers = {
        "Host": 'm.qiyoujiage.com',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Connection': 'Keep-Alive',
        'Content-Type': 'text/plain; Charset=UTF-8',
        'Accept-Language': 'zh-cn',
    }
    resp = requests.get('http://m.qiyoujiage.com/beijing.shtml', headers=headers)
    soup = BeautifulSoup(resp.content, 'html.parser')
    dl_list = soup.find_all('dl')
    body = ''
    for dl in dl_list:
        body += f"- {dl.find('dt').text}：{dl.find('dd').text.replace('(', '').replace(')', '/升')}\n"
    abstract = soup.find('div', attrs={'style':' border:solid 1px #009cff; margin:5px; padding:5px;'}).text.replace('\n', '').replace('\r', '')
    msg = {
        'title': '北京燃油价格',
        'abstract': f"<p style='color: red'>{abstract}</p>",
        'body': body,
    }
    return make_succ_response(msg)