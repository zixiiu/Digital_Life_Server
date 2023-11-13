import logging
import time
import requests
import json

from GPT import tune


class ERNIEBot():
    def __init__(self, args):
        """
        ERNIEBot-4 文心一言-4
        """
        self.access_token = ""
        logging.info('初始化ERNIE-Bot服务...')

        self.tune = tune.get_tune(args.character, args.model)  # 获取tune-催眠咒

        self.counter = 0  # 洗脑计数器

        if "4" in args.model:  # ERNIE-Bot-4
            self.baseurl = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token="
        else:  # ERNIE-Bot
            self.baseurl = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token="

        self.brainwash = args.brainwash  # 是否启用Brainwash模式

        # self.access_token = self.get_access_token(args.APIKey, args.SecretKey)  # 获取访问令牌

        self.is_executed = False  # 标志变量，注入是否已经启用过，初始设置为False

        logging.info("ERNIE-Bot已初始化。")

    def get_access_token(self, APIKey, SecretKey):
        """
        使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
        """
        access_token = ''
        if APIKey != '' and SecretKey != '':
            # logging.info('使用用户提供的应用API Key密钥。')
            url = "https://aip.baidubce.com/oauth/2.0/token"
            params = {"grant_type": "client_credentials", "client_id": {APIKey}, "client_secret": {SecretKey}}
            response = requests.post(url, params=params)
            access_token = response.json().get("access_token")
            # logging.info('获取 Access Token，创建会话成功。')
        else:
            logging.info('应用 API Key 或 Secret Key未填写。')
        return access_token

    # 每次提问都带有历史1k字节的对话历史
    def get_history(self):
        """
        获取历史记录
        """
        url = self.baseurl + self.access_token

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": "你好，我是ERNIE-Bot。"
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        with requests.post(url, headers=headers, data=payload) as response:
            response_json = response.json()
            history = response_json.get("history")

        return history

    def process_text(self, text):
        # 辅助函数，用于处理洗脑和提示词逻辑
        if self.brainwash and self.counter % 5 == 0:
            logging.info('激活Brainwash模式，强化tune。')
            processed_text = self.tune + '\n' + text
        elif not self.is_executed:
            processed_text = self.tune + '\n' + text
            self.is_executed = True
        else:
            processed_text = text

        return processed_text

    # 单轮请求
    def ask(self, text):
        """
        单轮请求
        text： 语音转换的完整文本
        """
        stime = time.time()

        url = self.baseurl + self.access_token

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": self.process_text(text)
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        with requests.post(url, headers=headers, data=payload) as response:
            response_json = response.json()
            result = response_json.get("result")

        logging.info('ERNIE-Bot响应：%s，用时%.2f秒' % (result, time.time() - stime))
        return result

    def ask_stream(self, text):
        """
        text： 获取到的单句文本
        """
        stime = time.time()  # 记录当前时间，用于计算响应时间

        self.counter += 1  # 计数器自增1

        # 根据chatVer的值选择不同的方法调用，并遍历返回的数据
        # 如果条件为True，那么表达式的结果是self.chatbot.ask_stream(text)；如果条件为False，那么表达式的结果将是迭代器循环的结果。

        url = self.baseurl + self.access_token

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": self.process_text(text)
                },
            ],
            "stream": True
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, stream=True)
        # generator 生成器本身就是迭代器，所以只能遍历一次。
        for message in response.iter_lines():
            if message:
                message = json.loads(message[6:].decode('utf-8'))  # 将字节转换为字符串，并解析为JSON对象
                is_end = message.get("is_end", False)  # 检查 "is_end" 字段的值，默认为 False
                complete_text = message.get("result")  # 取出消息部分
                logging.info('ERNIEBot流式响应：%s，@时间 %.2f秒' % (complete_text, time.time() - stime))  # 记录响应日志
                yield complete_text.strip()  # 返回片段的响应文本，并清除首尾的空白字符

                if is_end:
                    break
            else:
                # b'' 或 无法请求 等
                pass
