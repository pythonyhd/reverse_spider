# -*- coding: utf-8 -*-
import json
import logging

import scrapy

from credit_china.config import xinyong_shanxi_settings
from credit_china.work_utils.process_js import process_resp, process_params

logger = logging.getLogger(__name__)


class CreditShanxiSpider(scrapy.Spider):
    name = 'credit_shanxi'
    allowed_domains = ['credit.shaanxi.gov.cn']
    index_url = 'http://credit.shaanxi.gov.cn/queryPermitPublishPage.jspx'
    detail_url = 'http://credit.shaanxi.gov.cn/queryItemData.jspx'
    custom_settings = xinyong_shanxi_settings

    def start_requests(self):
        """爬虫入口函数，第六页开始出现验证码"""
        for page in range(1, 6):
            form_data = {
                "lb": "xzcf",
                "pageNo": str(page),
                "pageSize": "10",
            }
            yield scrapy.FormRequest(url=self.index_url, formdata=form_data, dont_filter=True)

    def parse(self, response):
        """列表页解析"""
        _str = json.loads(response.text).get('list')
        if _str:
            result_list = process_resp(_str)
            for result in result_list:
                id = result.get('id')  # 详情页参数
                psd = process_params(id)
                form_data = {'p': psd}
                yield scrapy.FormRequest(url=self.detail_url, formdata=form_data, callback=self.parse_detail, priority=3)
        else:
            logger.info('列表页请求失败')

    def parse_detail(self, response):
        """详情页解析"""
        _str = json.loads(response.text).get('dataList')
        result = process_resp(_str)
        oname = result.get('xy010101', '')  # 相对人名称
        pname = result.get('xy010105', '')  # 法人
        pname_type = result.get('xy010107', '')  # 法人证件类型
        pname_code = result.get('xy010108', '')  # 法人身份证件号码
        cf_type = result.get('xy020103', '')  # 处罚类别
        cf_wsh = result.get('xy020102', '')  # 行政处罚决定文书号
        uccode = result.get('xy010133', '')  # 统一社会信用代码
        cf_cflb = result.get('xy010133', '')  # 行政相对人类别
        illegal_type = result.get('xy020109', '')  # 违法行为类型
        cf_sy = result.get('xy020104', '')  # 违法事实
        cf_yj = result.get('xy020106', '')  # 处罚依据
        cf_jg = result.get('xy020130', '')  # 处罚内容
        jine = result.get('xy020116')   # 罚款金额
        jine = jine + '万元' if jine else ''
        cf_xzjg = result.get('xy020101', '')  # 处罚机关
        cf_xzjg_code = result.get('xy020134', '')  # 处罚机关统一社会信用代码
        cf_source = result.get('xy020135', '')  # 数据来源单位
        cf_source_code = result.get('xy020136', '')  # 数据来源单位统一社会信用代码
        bz = result.get('xy020108', '')  # 备注
        dep_name = result.get('dep_name', '')  # 报送部门
        cf_jdrq = result.get('xy020107', '')  # 处罚决定日期
        effective_date = result.get('effective_date', '')  # 处罚有效期
        jiezhi = result.get('xy020133', '')  # 公示截止期
        mondify_date = result.get('mondify_date', '')  # 数据更新时间戳
        create_date = result.get('create_date', '')  # 创建时间
        ws_nr_txt = json.dumps(result, ensure_ascii=False)
        uuid = result.get('id')
        item = dict(
            oname=oname, pname=pname, pname_type=pname_type, pname_code=pname_code, cf_type=cf_type, cf_wsh=cf_wsh,
            uccode=uccode, cf_cflb=cf_cflb, illegal_type=illegal_type, cf_sy=cf_sy, cf_yj=cf_yj, cf_jg=cf_jg, jine=jine,
            cf_xzjg=cf_xzjg, cf_xzjg_code=cf_xzjg_code, cf_source=cf_source, cf_source_code=cf_source_code, bz=bz,
            dep_name=dep_name, cf_jdrq=cf_jdrq, effective_date=effective_date, jiezhi=jiezhi, mondify_date=mondify_date,
            create_date=create_date, ws_nr_txt=ws_nr_txt, uuid=uuid,
        )
        yield item