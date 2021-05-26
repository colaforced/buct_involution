from DingDingBot.DDBOT import DingDing
#
# def dingding(info_list):
#     """格式化处理报告信息，发送至钉钉群"""
#     webhook = "https://oapi.dingtalk.com/robot/send?" \
#               "access_token=2e8a6ba36cf02d3c2da6f3324ca6efdd7103f2c4f87fb6de5edf4231cea11852"
#     dd = DingDing(webhook=webhook)
#     nt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#
#     for act in info_list:
#         text = str(act)
#         text = re.sub(r'[,,{,},]', '\n', text)
#         text = re.sub(r'\'', '', text)
#         dd.Send_Text_Msg('监控报警:%s %s' % (nt,text))


def dingding(message, hook_api):
    dd = DingDing(webhook= hook_api)
    dd.Send_Text_Msg(message)