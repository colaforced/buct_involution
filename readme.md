## 北京化工大学内卷辅助脚本##

1. **教务网辅助选课脚本**    

   - **背景：**每逢选课，教务网被挤宕机，配置差的电脑而又孤僻不喜欢求助别人的人，第一时间基本是选不到课了；如果仅是如此，也就认了吧，偏偏还有私下交易的，如约定某个点，同时上线，A退课，B选课。许多不上课却选课的大有人在。

   - **目标：**自立更生，抢吧，也恶心一下他们。

   - **方案：**写个小程序驱动游览器不断刷新页面并自动选择符合条件的课程

   - **技术选型：**selenuim

     

2. **教务网报告提醒脚本**

   -  **背景：**研究生阶段，学院以GPA加德育分作为国家学业奖学金的评价标准，且德育分占比极高，而学术报告这种也被记入德育分中，报告发布时间不确定，对于不好交流的人来说，消息相对闭塞，抢学术报告又成了一件麻烦事。
   -  **目标：**监测报告发布页面，自动提醒。
   -  **方案：**登陆后，脚本定时get相关页面
   -  **技术选型：**百度ai文字识别接口实现图片验证码登陆，requests自动请求。

   

3. **两个脚本通用配置：**

   - 配置环境 python3

   - 在config.py文件内填写好学号，密码

     

4. **选课脚本使用说明：**

   - chromedriver需要和电脑所装chrome游览器版本匹配，附上chromedriver下载链接：http://npm.taobao.org/mirrors/chromedriver/
   - 运行cpreetmpt.py文件，chrome游览器会主动打开教务网页面，在20s内手动输入验证码登陆
   - 游览器会自动跳入选课页面，并在命令行窗口输出可选课程编号，按照提示输入编号即可

   

5. **报告脚本使用说明**

   - 百度ai识别接口需要自己注册百度开发者账号，并申请免费通用文字识别接口。

     - 文档链接： [文字识别-百度智能云 (baidu.com)](https://cloud.baidu.com/doc/OCR/index.html) 

     - access_token获取： [通用参考 - 鉴权认证机制 | 百度AI开放平台 (baidu.com)](https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu) 

       ```python
       # encoding:utf-8
       import requests 
       
       # client_id 为官网获取的AK， client_secret 为官网获取的SK
       host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【官网获取的AK】&client_secret=【官网获取的SK】'
       response = requests.get(host)
       if response:
           print(response.json())
       ```

       

   - 钉钉提醒需要自己拉个群并设置钉钉机器人，复制替换hook链接到config文件内。

     - 钉钉机器人文档： [怎么添加自定义机器人？-钉钉帮助中心 (dingtalk.com)](https://www.dingtalk.com/qidian/help-detail-20781541.html) 
     - DingDingBot使用：参照util/remind.py即可

   - 配置完后，运行apmind.py即可

     

   