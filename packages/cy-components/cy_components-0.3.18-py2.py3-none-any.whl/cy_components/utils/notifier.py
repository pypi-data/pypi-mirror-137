import logging
import json
import requests
from datetime import datetime
from enum import IntEnum


class MessageType(IntEnum):
    DingDing = 0
    WeChatWork = 1
    Telegram = 2
    ServerJiang = 3


class MessageHandler:

    @staticmethod
    def __send_wechatwork_msg(content, token):
        """发送企业微信通知"""
        logger = logging.getLogger('MessageHandler.WechatWork')
        logger.setLevel(logging.INFO)
        logger.info(content)
        try:
            msg = {
                "msgtype": "markdown",
                "markdown": {"content": content + '\n>' + datetime.now().strftime("%m-%d %H:%M:%S")}
            }
            Headers = {"Content-Type": "application/json ;charset=utf-8 "}
            url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + token
            body = json.dumps(msg)
            requests.post(url, data=body, headers=Headers, timeout=15)
        except Exception as err:
            logger.error('Send WechatWork message failed: %s', format(repr(err)))

    @staticmethod
    def __send_dingding_msg(title, content, token):
        """send meesage by dingding"""
        logger = logging.getLogger('MessageHandler.Dingding')
        logger.setLevel(logging.INFO)
        logger.info(content)
        try:
            msg = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": content + '\n>' + datetime.now().strftime("%m-%d %H:%M:%S")
                }
            }
            Headers = {"Content-Type": "application/json ;charset=utf-8 "}
            url = 'https://oapi.dingtalk.com/robot/send?access_token=' + token
            body = json.dumps(msg)
            requests.post(url, data=body, headers=Headers, timeout=15)
        except Exception as err:
            logger.error('Send Dingding message failed: %s', format(repr(err)))

    @staticmethod
    def __sending_telegram_msg(msg, token):
        try:
            bot_token = token.split(';;;')[0]
            bot_chatID = token.split(';;;')[1]
            msg = msg.replace('**', '*')
            url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage'
            body = {
                'parse_mode': 'Markdown',
                'chat_id': bot_chatID,
                'text': msg
            }
            print(requests.post(url, data=body).text)
        except Exception as err:
            print('Send Telegram message failed: %s', format(repr(err)))

    @staticmethod
    def __sending_server_jiang_msg(title, message, token):
        try:
            api = "https://sctapi.ftqq.com/{}.send".format(token)
            data = {
                'text': title,
                'desp': message
            }
            result = requests.post(api, data=data)
            return(result)
        except Exception as err:
            print('Send ServerJiang message failed: %s', format(repr(err)))

    @ staticmethod
    def send_message(msg, title='Message', type=MessageType.DingDing, token=None):
        """Send simple message"""
        if type == MessageType.DingDing:
            MessageHandler.__send_dingding_msg(title, msg, token)
        elif type == MessageType.WeChatWork:
            MessageHandler.__send_wechatwork_msg(msg, token)
        elif type == MessageType.Telegram:
            MessageHandler.__sending_telegram_msg(msg, token)
        elif type == MessageType.ServerJiang:
            MessageHandler.__sending_server_jiang_msg(title, msg, token)
