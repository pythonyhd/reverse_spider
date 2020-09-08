# -*- coding: utf-8 -*-
import json
from urllib import parse

import jsonpath
import requests

from fake_useragent import UserAgent


url = 'https://docs.python.org/3.5/search.html?q=parse&check_keywords=yes&area=default'
parseResult = parse.urlparse(url)
query = parseResult.query
query_dict = parse.parse_qs(query)
print(query_dict)
dic = parse.parse_qs('action=addblog&job=modify&tid=1766670')
print(dic)
data = parse.parse_qsl('action=addblog&job=modify&tid=1766670')
print(data)
dic_tuple = dict(data)
print(dic_tuple)


class AcficSpider(object):
    headers = {'User-Agent': UserAgent().random}
    list_url = 'http://www.acfic.org.cn/shixin/new/SearchActionAll'

    def start_requests(self, query):
        form_data = {
                "iname": query,
                "code": "",
                "areaid": "0",
                "page": "1",
                "rows": "10",
        }
        res = requests.post(url=self.list_url, data=form_data, headers=self.headers)
        return res

    def parse_with_jsonpath(self, response):
        """
        通过jsonpath解析数据，不合适
        :param response:
        :return:
        """
        base_item = {'xxly': '哈哈'}
        result = json.loads(response.text)
        age = jsonpath.jsonpath(result, expr='$.rows[*].age')  # 年龄
        area_id = jsonpath.jsonpath(result, expr='$.rows..area_id')  # 地区id
        area_name = jsonpath.jsonpath(result, expr='$.row[*].area_name')  # 地区名称
        cardnum = jsonpath.jsonpath(result, expr='$.row..cardnum')  # 身份证号
        fkey = jsonpath.jsonpath(result, expr='$.rows[*].cards[*].fkey')  # 钥匙
        id = jsonpath.jsonpath(result, expr='$.rows[*].cards..id')  # 数据id
        case_code = jsonpath.jsonpath(result, expr='$.rows[*].case_code')  # 案号
        court_name = jsonpath.jsonpath(result, expr='$.rows[*].court_name')  # 法院名称
        disreput_type_name = jsonpath.jsonpath(result, expr='$.rows[*].disreput_type_name')  #
        duty = jsonpath.jsonpath(result, expr='$.rows..duty')  # 内容描述
        gist_cid = jsonpath.jsonpath(result, expr='$.rows..gist_cid')  # 文书号
        iname = jsonpath.jsonpath(result, expr='$.rows..iname')  # 主体名
        performance = jsonpath.jsonpath(result, expr='$.rows..performance')  # 履行情况
        publish_date = jsonpath.jsonpath(result, expr='$.rows..publish_date')  # 公示日期
        reg_date = jsonpath.jsonpath(result, expr='$.rows..reg_date')  #
        sex_name = jsonpath.jsonpath(result, expr='$.rows..sex_name')  # 性别
        unperformed_part = jsonpath.jsonpath(result, expr='$.rows..unperformed_part')
        ws_nr_txt = json.dumps(result, ensure_ascii=False)
        item_org = dict(oname=iname, anhao=case_code, cf_wsh=gist_cid)

    def parse_list(self, response):
        """
        自定义方法处理json数据
        :param response:
        :return:
        """
        use_data = dict()
        use_data['data'] = []
        results = json.loads(response.text)
        rows = results.get('rows')
        for row in rows:
            AcficSpider._insert(use_data, row)
            cards = row.get('cards')
            for card in cards:
                AcficSpider._insert(use_data, card)
        return use_data

    @staticmethod
    def str_dict(dic, keys):
        import html
        return {k: html.unescape(dic[k]) for k in dic if k in keys}

    @staticmethod
    def _insert(use_data, dic):
        keys = ('iname', 'age', 'area_id', 'area_name', 'cardnum', 'case_code', 'court_name', 'disreput_type_name', 'duty', 'gist_cid', 'gist_nuit', 'id', 'performance', 'performed_part', 'publish_date', 'reg_date', 'sex_name', 'unperformed_part', 'fkey')
        sub_data = AcficSpider.str_dict(dic, keys)
        use_data['data'].append(sub_data)


if __name__ == '__main__':
    conn = AcficSpider()
    res = conn.start_requests('史贺')
    des = conn.parse_list(res)
    print(des)
    # conn.parse_with_jsonpath(res)
