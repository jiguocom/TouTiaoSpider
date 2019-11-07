#!/usr/bin/python
# -*- coding: UTF-8 -*-

from selenium import webdriver
from time import sleep
import time
import re
import json
import os


class TouTiao:
    def __init__(self):
        self.uid = '3093819416'
        self.t = time.time()  # 当前时间
        self.option = webdriver.ChromeOptions()# 浏览器设置
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])# 防拦截
        self.browser = webdriver.Chrome(r'./chromedriver.exe',options=self.option)

    #数据提取
    def t_num(self,str):
        str = re.findall(r'\d+\.?\d*', str)[0]
        if re.findall(r'\.', str):
            str = float(str) * 10000
        return int(str)

    # 判断页面时间,滚动页面
    def page_time(self,idNum=2):
        # 提取文章数据
        html = self.browser.find_elements_by_xpath('//li[@ga_event="feed_item_click"]')
        if html:
            # 最后一条是否过期
            i = html[-1]
            date = i.find_elements_by_class_name('lbtn')[idNum].text
            if idNum == 2:
                timeArray = time.strptime(date, "⋅ %Y-%m-%d %H:%M")
            else:
                timeArray = time.strptime(date, " ⋅ %Y-%m-%d %H:%M")
            timeStamp = int(time.mktime(timeArray))

            if self.t < timeStamp + 86400 * 30:
                # js滚动页面
                self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                sleep(1)
                self.page_time(idNum)


    def login(self):
        self.browser.get('https://sso.toutiao.com/login/')
        sleep(2)
        uid = input('请输入作者id：')

        if os.path.exists('cookies.json'):
            self.browser.delete_all_cookies()
            with open('cookies.json', 'r', encoding='utf-8') as f:
                listCookies = json.loads(f.read())
            for cookie in listCookies:
                self.browser.add_cookie({
                    'domain': cookie['domain'],
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'path': '/',
                    'expires': None
                })
            self.browser.get('https://www.toutiao.com/c/user/' + self.uid + '/#mid=3236420868')
            sleep(2)
        else:
            input('确定已输入账号密码？')
            self.browser.find_element_by_id('bytedance-login-submit').click()
            sleep(2)
            cookies = self.browser.get_cookies()
            jsonCookies = json.dumps(cookies)
            with open('cookies.json', 'w') as f:
                f.write(jsonCookies)



    def article_spider(self):
        print('--------------------------文章数据--------------------------------------')
        # 切换文章tab
        self.browser.find_element_by_xpath('//li[@idx=0]').click()
        sleep(2)
        self.page_time()
        article_num = 0
        article_comment = 0
        article_n = 0
        html = self.browser.find_elements_by_xpath('//li[@ga_event="feed_item_click"]')
        if html:
            for i in html:
                num = i.find_elements_by_class_name('lbtn')[0].text
                comment = i.find_elements_by_class_name('lbtn')[1].text
                date = i.find_elements_by_class_name('lbtn')[2].text

                print('%s %s %s' % (num, comment, date))

                if num != '置顶':
                    # 阅读数处理# 评论数处理
                    num = self.t_num(num)
                    comment = self.t_num(comment)

                    # 统计
                    article_num += num
                    article_comment += comment
                    article_n += 1
                    # print('%s %s %s' % (num, comment, date))

                    timeArray = time.strptime(date, "⋅ %Y-%m-%d %H:%M")
                    timeStamp = int(time.mktime(timeArray))
                    if self.t >= timeStamp + 86400 * 30:
                        break

        print('文章总数：%d 阅读总数：%d 评论总数：%d' % (article_n, article_num, article_comment))


    def vedio_spider(self):
        print('--------------------------视频数据--------------------------------------')
        # 切换视频tab
        self.browser.find_element_by_xpath('//li[@idx=1]').click()
        sleep(2)
        self.page_time()
        vedio_num = 0
        vedio_comment = 0
        vedio_n = 0
        html = self.browser.find_elements_by_xpath('//li[@ga_event="feed_item_click"]')
        if html:
            for i in html:
                num = i.find_elements_by_class_name('lbtn')[0].text
                comment = i.find_elements_by_class_name('lbtn')[1].text
                date = i.find_elements_by_class_name('lbtn')[2].text

                print('%s %s %s' % (num, comment, date))

                if num != '置顶':
                    # 阅读数处理# 评论数处理
                    num = self.t_num(num)
                    comment = self.t_num(comment)

                    # 统计
                    vedio_num += num
                    vedio_comment += comment
                    vedio_n += 1
                    # print('%s %s %s' % (num, comment, date))

                    timeArray = time.strptime(date, "⋅ %Y-%m-%d %H:%M")
                    timeStamp = int(time.mktime(timeArray))
                    if self.t >= timeStamp + 86400 * 30:
                        break

        print('视频总数：%d 阅读总数：%d 评论总数：%d' % (vedio_n, vedio_num, vedio_comment))

    def wtt_spider(self):
        print('--------------------------微头条数据--------------------------------------')
        # 切换视频tab
        self.browser.find_element_by_xpath('//li[@idx=2]').click()
        sleep(2)
        self.page_time(3)
        wtt_num = 0
        wtt_zan = 0
        wtt_comment = 0
        wtt_n = 0
        html = self.browser.find_elements_by_xpath('//li[@ga_event="feed_item_click"]')
        if html:
            for i in html:
                num = i.find_elements_by_class_name('lbtn')[0].text
                zan = i.find_elements_by_class_name('lbtn')[1].text
                comment = i.find_elements_by_class_name('lbtn')[2].text
                date = i.find_elements_by_class_name('lbtn')[3].text

                print('%s %s %s %s' % (num, zan, comment, date))

                if num != '置顶':
                    # 阅读数处理# 评论数处理
                    num = self.t_num(num)
                    zan = self.t_num(zan)
                    comment = self.t_num(comment)

                    # 统计
                    wtt_num += num
                    wtt_zan += zan
                    wtt_comment += comment
                    wtt_n += 1
                    # print('%s %s %s' % (num, comment, date))

                    timeArray = time.strptime(date, " ⋅ %Y-%m-%d %H:%M")
                    timeStamp = int(time.mktime(timeArray))
                    if self.t >= timeStamp + 86400 * 30:
                        break

        print('微头条总数：%d 阅读总数：%d 点赞数：%d 评论总数：%d' % (wtt_n, wtt_num,wtt_zan, wtt_comment))

    def close(self):
        # 关闭浏览器
        self.browser.quit()
        exit()


if __name__ == '__main__':
    tou_tiao = TouTiao()
    tou_tiao.login()
    tou_tiao.article_spider()
    tou_tiao.vedio_spider()
    tou_tiao.wtt_spider()
    tou_tiao.close()



