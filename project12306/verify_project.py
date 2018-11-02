#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import re
import manual_dm
import rk
import requests


class Verify_project():
    def __init__(self):
        s = requests.session()
        s.verify = False
        s.trust_env = False
        s.proxies = {
            'http': '127.0.0.1:8888',
        }
        s.headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        self.s = s

    def ruokuai_image(self):
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.5326066130802138'
        headers = {
            'referer': 'https://kyfw.12306.cn/otn/login/init'
        }
        r = self.s.get(url, headers=headers)
        img = r.content
        rc = rk.RClient('mumuloveshine', 'mumu2018', '7545', 'df49bdfd6416475181841e56ee1dc769')
        answer = rc.rk_create(img, 6113)
        return answer['Result']


    def my_image_1(self):
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-image'
        params = {
            'login_site': 'E',
            'module': 'login',
            'rand': 'sjrand',
            '0.8838711524344427': ''
        }
        r = self.s.get(url, params=params)
        img = r.content
        return img


    def my_image(self):
        dm = manual_dm.Manual()
        a = dm.create(self.my_image_1)
        return a['Result']


    def dama(self):
        answers = self.my_image()
        img_wh = 67
        imgs_d = 5
        img_b = 20
        a = []
        for answer in answers:
            answer = int(answer)
            y_seq, x_seq = divmod(answer - 1, 4)
            print(x_seq, y_seq)
            wide = str(imgs_d + x_seq * (img_wh + imgs_d) + random.randint(img_b, img_wh - img_b))
            high = str(imgs_d + y_seq * (img_wh + imgs_d) + random.randint(img_b, img_wh - img_b))
            a.append(wide)
            a.append(high)
        return ','.join(a)

    def verification(self):
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        data = {
            'answer': self.dama(),
            'login_site': 'E',
            'rand': 'sjrand'
        }
        print(data)
        r = self.s.post(url, data=data)
        print(r)
        print(r.text)
        try:
            json_data = r.json()
            data = json_data['result_code']
            if data == '4':
                print('验证成功')
                return True
            else:
                print('验证失败')
                return False
        except:
            data = re.findall('result_code>(.*?)</result_code', r.text)[0]
            print(data)
            if data == '4':
                print('验证成功')
                return True
            else:
                print('验证失败')
                return False

    def verifig_sure(self):
        b = False

        for i in range(5):
            b = self.verification()
            if b:
                print('验证完毕，进行登录')
                break
            else:
                print('验证失败，重试')
        else:
            print('次数超过五次，请重试')

    def login(self,user_name,password):
        url = 'https://kyfw.12306.cn/passport/web/login'
        data = {
            'username': user_name,
            'password': password,
            'appid': 'otn'
        }
        r = self.s.post(url, data=data)
        data = re.findall('result_code>(.*?)</result_code', r.text)[0]
        if data == '0':
            print('登录成功')
        else:
            print('登录失败')

    def verify_skip_1(self):
        url = 'https://kyfw.12306.cn/otn/login/userLogin'
        data = {
            '_json_att': ''
        }
        r = self.s.post(url, data=data)

        url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        data = {
            'appid': 'otn'
        }
        r = self.s.post(url,data=data)
        json_data=r.json()
        return json_data['newapptk']

    def verify_skip_2(self):
        url = 'https://kyfw.12306.cn/otn/uamauthclient'
        data = {
            'tk': self.verify_skip_1()
        }
        r = self.s.post(url, data=data)
        json_data=r.json()
        code=json_data['result_code']
        print(code)
        if code==0:
            print('验证通过')
        else:
            print('验证失败')


if __name__ == '__main__':
    pro = Verify_project()
    pro.verifig_sure()
    pro.login('huanyixin1989','123456xin')