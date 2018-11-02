#!/usr/bin/env python
# -*- coding: utf-8 -*-
from verify_project import Verify_project
from zuowei import didian
from urllib import parse

__author__ = 'jianghao'


class Scrent(Verify_project):
    """
    对获取的车次进行筛选
    """

    def __init__(self, times, from_city, destination):
        '''
        :param times: 你要坐车的时间  是一个列表
        :param from_city: 坐车的起点
        :param destination: 终点站
        '''
        self.times = times
        self.from_city = from_city
        self.destination = destination
        super().__init__()

    def toponym(self, city):
        return didian()[city]

    def query(self, purpose_code='普通'):
        from_city = self.toponym(self.from_city)
        destination = self.toponym(self.destination)
        purpose_codes = {'普通': 'ADULT', '学生': '0X00'}
        purpose_code = purpose_codes[purpose_code]
        result = []
        for time in self.times:
            url = 'https://kyfw.12306.cn/otn/leftTicket/query'
            params = {
                'leftTicketDTO.train_date': time,
                'leftTicketDTO.from_station': from_city,
                'leftTicketDTO.to_station': destination,
                'purpose_codes': purpose_code
            }
            r = self.s.get(url, params=params)
            json_data = r.json()
            results = json_data['data']['result']
            a = []
            for i in range(len(results)):
                i = results[i].split('|') + [time] + [purpose_code]
                a.append(i)
            a.pop(0)
            result += a
        return result

    def scrent_query(self, zuowei=None, train_type=None, train_num=None, start_time=None, end_time=None,
                     purpose_code='普通'):
        '''
        result = self.query(purpose_code)     返回一个符合条件的车次信息
        :param zuowei: 你要选择的席次   可以是一个列表  默认为空
        :param traim_type:选择车的类型
        :param train_num:选择固定的车次
        :param start_time:选择车次最早的发车时间   格式必须为 **:**  24小时制
        :param end_time:选择车次最晚的发车时间         格式必须为 **:** 24小时制
        :param purpose_code: 选择学生票还是普通票   默认为普通票
        :return:
        '''
        zuoweis = {'高级软卧': 21, '软卧': 23, '软座': 24, '无座': 26, '硬卧': 28, '二等座': 30, '一等座': 31, '商务座': 32, '动卧': 33}
        train_types = {'高铁': 'G', '直达': 'Z', '动车': 'D', '特快': 'T', '快速': 'K', '城际': 'C', '其他': ''}
        self.zuoweis = zuoweis
        self.zuowei = zuowei

        results = [i for i in self.query(purpose_code) if i[0]]
        # 筛选能预定的车次信息

        results = [i for i in results if train_types[train_type] == i[3][0] or (train_type == '其他' and i[3].isdigit())]
        # 筛选指定类型的车辆的车次信息
        print(len(results))

        if train_num:
            results = [i for j in train_num for i in results if i[3] == j]
            print('符合的车次共有{}条'.format(len(results)))
        # 筛选指定的车辆的车次信息


        if start_time:
            results = [i for i in results if i[8] >= start_time]
            print(len(results))

        if end_time:
            results = [i for i in results if i[8] <= end_time]

        if zuowei:
            results = [i for j in zuowei for i in results if i[zuoweis[j]] and i[zuoweis[j]] != '无']
        # 筛选指定的座位类型的车次信息

        results = [[parse.unquote(i[0])] + i[1:] for i in results]
        print('符合所有条件的车次有{}条'.format(len(results)))
        return results


if __name__ == '__main__':
    pass
