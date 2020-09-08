# -*- coding: utf-8 -*-
import pymysql
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 可以显示中文


def get_data(name, num):
    conn = pymysql.connect(host='114.115.201.98', port=3306, user='root', password='axy#mysql2019', db='shihe_data', charset="utf8", use_unicode=True)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = 'select oname,cf_wsh,cf_sy,lian_sj,zxfy from zxxx_xg where oname = "%s"' % name
    cursor.execute(sql)
    all_data = cursor.fetchall()
    total_num = len(all_data)
    curt_data = all_data[0:num]
    cursor.close()
    conn.close()
    return {'total_num': total_num, 'curt_data': curt_data}


@app.route('/', methods=['GET'])  # http://localhost:5000/api/?name=李国&num=10
def get_api():
    oname = request.args.get('name')
    num = request.args.get('num', 20)
    num = int(num)
    content_dict = get_data(oname, num)
    total_num = content_dict.get('total_num')
    content_list = content_dict.get('curt_data')
    data_list = []
    for content in content_list:
        data_list.append(content)
    item = {'total_num': total_num, 'per_num': num, 'data': data_list}
    return jsonify(item)  # 返回json数据


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)