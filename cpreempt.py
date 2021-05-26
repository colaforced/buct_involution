from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import datetime
from pyquery import PyQuery
import random
from config import STUDENT_ID, PASSWORD

browser = webdriver.Chrome(executable_path='src/chromedriver.exe')
wait = WebDriverWait(browser, 20)

browser.get('http://yjsy.buct.edu.cn:8080/pyxx/login.aspx')

A = browser.find_element_by_id('_ctl0_txtusername')
B = browser.find_element_by_id('_ctl0_txtpassword')
A.send_keys(STUDENT_ID)
B.send_keys(PASSWORD)

button = browser.find_element_by_id('_ctl0_ImageButton1')
time.sleep(15)

# init
browser.get('http://yjsy.buct.edu.cn:8080//PYXX/pygl/pyjhxk.aspx?xh={}'.format(STUDENT_ID))
doc = PyQuery(browser.page_source)
maths = doc('#dgData > tbody > tr')

p = 0
for each in maths.items():
    print(p, end=' @@@ ')
    class_name = each('td:nth-child(1)')
    print(class_name)
    p += 1

# dgData > tbody > tr:nth-child(2)  第一门课
li = list(map(int, input('输入想选的课的数字，用空格做分割:').split()))

count = 0
while True:
    count += 1
    try:
        day = datetime.datetime.now()
        print(day)
        browser.get('http://yjsy.buct.edu.cn:8080//PYXX/pygl/pyjhxk.aspx?xh={}'.format(STUDENT_ID))
    except Exception as e:
        print(e)
    else:
        doc = PyQuery(browser.page_source)
        for n in li:
            tr = '#dgData > tbody > tr:nth-child({})'.format(str(n + 1))
            my_class = doc(tr)
            print(my_class('td:nth-child(1)').text(), '-----', my_class('td:nth-child(12)').text())

            if '未满' in my_class.text():
                button_id = my_class('td a').attr.id
                c = browser.find_element_by_id(button_id)
                c.click()
                day = datetime.datetime.now()
                print(day)
                break

    time.sleep(2 * random.random())
    print('已刷新次数:', count, end='\n\n')

    try:
        browser.refresh()
    except Exception as e:
        print(e)
    time.sleep(1)
