#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'jianghao'


def screen_out(self, riding_name):
    self.normal_passengers = self.visit_staff()
    normal_passengers = self.normal_passengers
    normal_passenger = []
    passengerTicketStr = []
    for i in riding_name:
        for j in normal_passengers:
            if j['passenger_name'] == i:
                normal_passenger.append(j)
                break
        else:
            print('{}不存在，请添加新的联系人'.format(i))
    result = self.result

