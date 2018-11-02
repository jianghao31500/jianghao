import json
import random

import requests
import time
import urllib3
import re

from scrent import Scrent
from zuowei import seat

urllib3.disable_warnings()

class Pro_12306(Scrent):
    b=False
    def skip_1(self):
        url='https://kyfw.12306.cn/otn/login/userLogin'
        r=self.s.get(url)

    def  visit_submitOrderRequest(self,result):
        self.result=result
        url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        data = {
            'secretStr': result[0],
            'train_date':result[37],
            'back_train_date': '',
            'tour_flag': 'dc',
            'purpose_codes': result[38],
            'query_from_station_name':self.from_city.encode().decode('gbk',errors='ignore'),
            'query_to_station_name': self.destination.encode().decode('gbk',errors='ignore'),
            'undefined': ''
        }
        r = self.s.post(url, data=data)
        print(r.text)
        if r.json()['status']:
            print('进入{}车次:{}预定页面成功,发车时间为{}'.format(result[37],result[3],result[8]))
            return True
        else:
            print('进入{}车次:{}预定页面失败'.format(result[37],result[3]))
            return False

    def visit_confirmPassenger(self):
        url='https://kyfw.12306.cn/otn/login/userLogin'
        self.s.get(url)

        url='https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        data={
            '_json_att': ''
        }
        r=self.s.post(url,data=data)
        self.globalRepeatSubmitToken=re.findall("globalRepeatSubmitToken = '(.*?)'",r.text)[0]
        print(self.globalRepeatSubmitToken)
        self.leftTicketStr=re.findall("'ypInfoDetail':'(.*?)'",r.text)[0]
        self.key_check_isChange=re.findall("key_check_isChange':'(.*?)'",r.text)[0]

    def visit_staff(self):
        url='https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        data={
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.globalRepeatSubmitToken
        }
        r=self.s.post(url,data=data)
        return r.json()['data']['normal_passengers']

    def screen_out(self,riding_name):
        self.normal_passengers = self.visit_staff()
        normal_passengers = self.normal_passengers
        normal_passenger = []
        passengerTicketStr=[]
        for i in riding_name:
            for j in normal_passengers:
                if j['passenger_name'] == i:
                    normal_passenger.append(j)
                    break
            else:
                print('{}不存在，请添加新的联系人'.format(i))
        return normal_passenger



    def visit_checkOrderInfo(self,riding_name,riding_sex):
        normal_passenger=self.screen_out(riding_name)
        self.passengerTicketStr=''
        self.oldPassengerStr=''
        li={'成人':1,'儿童':2,'学生':3,'残军':4}
        for j in self.zuowei:
            if self.result[self.zuoweis[j]]:
                for i in normal_passenger:
                    self.passengerTicketStr+='{},{},{},{},{},{},{},N_'.format(seat[j],i["passenger_flag"],li[riding_sex],i["passenger_name"],i["passenger_id_type_code"],i["passenger_id_no"],i["mobile_no"])
                    self.oldPassengerStr+='{},{},{},{}_'.format(i["passenger_name"],i["passenger_id_type_code"],i["passenger_id_no"],i["passenger_type"])
        self.passengerTicketStr.rstrip('_')
        url='https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        data={
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': self.passengerTicketStr,
            'oldPassengerStr': self.oldPassengerStr,
            'tour_flag': 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.globalRepeatSubmitToken
        }
        r=self.s.post(url,data=data)
        self.canChooseSeats=r.json()['data']['canChooseSeats']

    def visit_getQueueCount(self):
        url='https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        data={
            'train_date': time.strftime('%a %b %d %Y ',time.strptime(self.result[37], "%Y-%m-%d" ))+'00:00:00 GMT+0800 (中国标准时间)',
            'train_no': self.result[2],
            'stationTrainCode': self.result[3],
            'seatType': 'O',
            'fromStationTelecode': self.result[6],
            'toStationTelecode': self.result[7],
            'leftTicket': self.leftTicketStr,
            'purpose_codes': '00',
            'train_location': 'P4',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.globalRepeatSubmitToken
        }
        r=self.s.post(url,data=data)
        return r.json()


    def visit_confirmSingleForQueue(self):
        if self.canChooseSeats=='Y':
            choose_seats = '1A'
        else:
            choose_seats=''
        url='https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        data={
            'passengerTicketStr': self.passengerTicketStr,
            'oldPassengerStr': self.oldPassengerStr,
            'randCode': '',
            'purpose_codes': '00',
            'key_check_isChange': self.key_check_isChange,
            'leftTicketStr': self.leftTicketStr,
            'train_location': self.result[15],
            'choose_seats': choose_seats,
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.globalRepeatSubmitToken
        }
        r=self.s.post(url,data=data)
        return  r.json()


    def queryOrderWaitTime(self):
        url='https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime'
        params={
                'random': str(round(time.time() * 1000)),
                'tourFlag': 'dc',
                '_json_att': '',
                'REPEAT_SUBMIT_TOKEN': self.globalRepeatSubmitToken
            }
        r=self.s.get(url,params=params)
        return r.json()


if __name__ == '__main__':
    while True:
        try:
            pro = Pro_12306(['2018-09-28'],'北京','光山')
            pro.verifig_sure()
            pro.login('17858802961','woshishuiwxj1124')
            pro.verify_skip_2()
            pro.skip_1()
        except:
            print('出现错误，重试')
        else:
            break

    while True:
        try:
            results=pro.scrent_query(train_type='快速',zuowei=['硬卧'])
            time.sleep(2)
        except json.decoder.JSONDecodeError:
            print('出现错误')
        else:
            break
    while True:
            if not results:
                results = pro.scrent_query(train_type='快速', zuowei=['硬卧'])
                print('目前车次无票，刷新重试')
                time.sleep(1)
            else:
                b=False
                for result in results:
                    print(result)
                    if pro.visit_submitOrderRequest(result):
                        pro.visit_confirmPassenger()
                        pro.visit_checkOrderInfo(['蒋长浩'],'成人')
                        pro.visit_getQueueCount()
                        time.sleep(5)
                        data_json=pro.visit_confirmSingleForQueue()
                        print(data_json)
                        time.sleep(5)
                        if data_json['data'].get('submitStatus'):
                            while True:
                                data_json=pro.queryOrderWaitTime()['data']
                                time.sleep(4)
                                print(data_json)
                                if data_json['waitTime']<0:
                                    print('抢票成功')
                                    break
                                else:
                                    print('排队中,还需要等待时间{}，前面人数{}'.format(data_json["waitTime"],data_json["waitCount"]))
                        else:
                            print('提交失败')
                        break


                    else:
                        print('进行下一个')
                if b:
                        break





    # pro.visit_checkOrderInfo()
    # pro.visit_getQueueCount()
    # pro.visit_confirmSingleForQueue()
    # pro.visit_queryOrderWaitTime()
    # pro.thred('2018-08-30','北京','信阳')  #时间格式 ****-**-**  可以是列表
    # pro.second()
