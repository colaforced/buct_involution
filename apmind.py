import re
import time
import requests
from pyquery import PyQuery as pq
from PIL import Image
from retrying import retry
from util.remind import dingding
from config import STUDENT_ID, PASSWORD, DINGDING_WEBBOOK, ACCES_TOKEN


def step_one():
    """
    get登录页获取
        服务器生成的cookie: ASP.NET_SessionId
        三个参数值：__VIEWSTATE、__VIEWSTATEGENERATOR、__EVENTVALIDATION

    :return:
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'http://yjsy.buct.edu.cn:8080/pyxx/topbanner.aspx',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }
    response = requests.get('http://yjsy.buct.edu.cn:8080/pyxx/login.aspx', headers=headers)
    cookies = requests.utils.dict_from_cookiejar(response.cookies)
    doc = pq(response.text)
    VIEWSTATE = doc("input")[0].valueq
    VIEWSTATEGENERATOR = doc("input")[1].value
    EVENTVALIDATION = doc("input")[2].value
    return (cookies, VIEWSTATE, VIEWSTATEGENERATOR, EVENTVALIDATION)


def step_two(cookies):
    """下载验证码"""

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
        'Accept': 'image/webp,*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Referer': 'http://yjsy.buct.edu.cn:8080/pyxx/login.aspx',
        'Cache-Control': 'max-age=0',
    }
    response = requests.get('http://yjsy.buct.edu.cn:8080/pyxx/PageTemplate/NsoftPage/yzm/IdentifyingCode.aspx',
                            headers=headers, cookies=cookies)
    with open('pcahe/IdentifyingCode.gif', 'wb') as f:
        f.write(response.content)

    im = Image.open('pcahe/IdentifyingCode.gif')
    im.tell()
    im.save('pcahe/IdentifyingCode.png')


def step_three():
    """识别验证码"""
    import base64

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    f = open('pcahe/IdentifyingCode.png', 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img}
    access_token = ACCES_TOKEN
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        r = response.json()
        print(r)
        code = r['words_result'][0]['words']
        if len(code) != 4:
            raise Exception
        else:
            return code


@retry(stop_max_attempt_number=15, wait_random_min=500)
def step_two_and_three(cookies):
    step_two(cookies)
    code = step_three()
    return code


@retry(stop_max_attempt_number=5, wait_random_min=500)
def step_four(cookies, VIEWSTATE, VIEWSTATEGENERATOR, EVENTVALIDATION):
    """上传验证结果"""
    code = step_two_and_three(cookies)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://yjsy.buct.edu.cn:8080',
        'Connection': 'keep-alive',
        'Referer': 'http://yjsy.buct.edu.cn:8080/pyxx/login.aspx',
        'Upgrade-Insecure-Requests': '1',
    }

    data = {
        '__VIEWSTATE': VIEWSTATE,
        '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
        '__EVENTVALIDATION': EVENTVALIDATION,
        '_ctl0:txtusername': STUDENT_ID,
        '_ctl0:txtpassword': PASSWORD,
        '_ctl0:txtyzm': code,
        '_ctl0:ImageButton1.x': '47',
        '_ctl0:ImageButton1.y': '6'
    }
    response = requests.post('http://yjsy.buct.edu.cn:8080/pyxx/login.aspx', headers=headers, cookies=cookies,
                             data=data)
    if response.status_code == 200:
        if '你输入的验证码错误' in response.text:
            raise Exception
    else:
        raise Exception


def cookie_init():
    cookies, VIEWSTATE, VIEWSTATEGENERATOR, EVENTVALIDATION = step_one()
    step_four(cookies, VIEWSTATE, VIEWSTATEGENERATOR, EVENTVALIDATION)
    return cookies


def get_aim_page(cookies):
    """get_aim_page在cookie失效时返回0，无可选报告时，返回空列表，有可选报告时返回非控列表"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Referer': 'http://yjsy.buct.edu.cn:8080/pyxx/leftmenu.aspx',
        'Upgrade-Insecure-Requests': '1',
    }

    params = (
        ('xh', STUDENT_ID),
    )

    response = requests.get('http://yjsy.buct.edu.cn:8080/pyxx/txhdgl/hdlist.aspx', headers=headers, params=params,
                            cookies=cookies)

    if '未将对象引用设置到对象的实例' in response.text:
        return 0
    else:
        nt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(nt + ': ' + 'get目标页面成功')
        html = response.text
        r = '<td align="center" style="width:30px;">(.*?)</td><td align="center">(.*?)</td><td align="center">(.*?)</td><td align="center" style="width:80px;">(.*?)</td><td align="center" style="width:80px;">(.*?)</td><td align="center" style="width:150px;">(.*?)</td><td align="center" style="width:40px;">(.*?)</td><td align="center" style="width:40px;">(.*?)</td><td align="center">(.*?)</td><td align="center" style="width:30px;">(.*?)</td><td align="center" style="width:80px;">(.*?)</td><td align="center" style="width:80px;">(.*?)</td><td align="center" style="width:30px;">&nbsp;</td><td nowrap="nowrap" align="center" style="width:26px;">'
        result_list = re.findall(r, html)
        info_list = []
        for act in result_list:
            a = int(act[6])
            b = int(act[7])
            # if a<=b: continue
            """剩余名额<3则跳过"""
            if a - b <= 3: continue
            info = {
                '类型': act[0],
                '报告（活动）名称': act[1],
                '发布单位': act[2],
                '报告开始': act[3],
                '报告结束': act[4],
                '地点': act[5],
                '可报名人数': act[6],
                '已报名人数': act[7],
                '主办单位': act[8],
                '报名方式': act[9],
                '报名开始': act[10],
                '报名截止': act[11],
            }
            info_list.append(info)
        return info_list


def dingding_multi_acts(multi_acts):
    """格式化处理报告信息，发送至钉钉群"""
    nt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    for act in multi_acts:
        text = str(act)
        text = re.sub(r'[,,{,},]', '\n', text)
        text = re.sub(r'\'', '', text)
        msg = '监控报警:%s %s' % (nt, text)
        dingding(msg, DINGDING_WEBBOOK)


@retry(stop_max_attempt_number=5, wait_random_min=60000)
def monitor_main():
    """主要检测程序，每隔一分钟扫描一次"""
    cookies = {'ASP.NET_SessionId': 'ruesedbkt41cpovqt01wiblz'}
    while True:
        res = get_aim_page(cookies)
        if res != 0:
            dingding_multi_acts(res)
        else:
            cookies = cookie_init()
            continue
        time.sleep(60)


if __name__ == '__main__':
    try:
        """闲置手机termux终端运行设置手机不休眠"""
        import os

        os.system('termux-wake-lock')
    except:
        print('非termux终端，无需termux-wake-lock')

    while True:
        try:
            monitor_main()
        except:
            print("主程序错误,休眠5分钟")
            time.sleep(300)
