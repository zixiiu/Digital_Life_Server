import logging
import os
import time

import GPT.machine_id
import GPT.tune as tune


class GPTService():
    def __init__(self, args):
        logging.info('初始化ChatGPT服务…')
        self.chatVer = args.chatVer  # ChatGPT版本

        self.tune = tune.get_tune(args.character, args.model)  # 获取tune-催眠咒

        self.counter = 0  # 计数器

        self.brainwash = args.brainwash  # 是否启用Brainwash模式

        if self.chatVer == 1:  # ChatGPT版本为1
            from revChatGPT.V1 import Chatbot
            config = {}
            if args.accessToken:  # 如果有访问令牌
                logging.info('尝试使用访问令牌登录。')
                config['access_token'] = args.accessToken
            else:
                logging.info('尝试使用电子邮件和密码登录。')
                config['email'] = args.email
                config['password'] = args.password
            config['paid'] = args.paid
            config['model'] = args.model
            if type(args.proxy) == str:
                config['proxy'] = args.proxy

            self.chatbot = Chatbot(config=config)  # 初始化V1版本的Chatbot
            logging.info('WEB Chatbot已初始化。')

        elif self.chatVer == 3:  # ChatGPT版本为3
            mach_id = GPT.machine_id.get_machine_unique_identifier()
            from revChatGPT.V3 import Chatbot
            if args.APIKey:  # 如果有API密钥
                logging.info('使用用户提供的API密钥。')
                api_key = args.APIKey
            else:
                logging.info('使用自定义API代理，带有速率限制。')
                # 没有设置OpenAI APIKey 时使用自建端口
                os.environ['API_URL'] = "https://api.geekerwan.net/chatgpt2"
                api_key = mach_id

            self.chatbot = Chatbot(api_key=api_key, proxy=args.proxy, system_prompt=self.tune)  # 初始化V3版本的Chatbot
            logging.info('API Chatbot已初始化。')

    def ask(self, text):
        stime = time.time()
        if self.chatVer == 3:
            prev_text = self.chatbot.ask(text)

        # V1版本
        elif self.chatVer == 1:
            for data in self.chatbot.ask(
                    self.tune + '\n' + text
            ):
                prev_text = data["message"]

        logging.info('ChatGPT响应：%s，用时%.2f秒' % (prev_text, time.time() - stime))
        return prev_text

    def ask_stream(self, text):
        """
        text： 获取到的单句文本
        """
        prev_text = ""  # 保存上一个消息的文本内容
        complete_text = ""  # 保存完整的响应文本内容
        stime = time.time()  # 记录当前时间，用于计算响应时间

        if self.counter % 5 == 0 and self.chatVer == 1:  # 每第5次调用方法且chatVer等于1时执行
            if self.brainwash:  # 如果启用了Brainwash模式
                logging.info('激活Brainwash模式，强化tune。')  # 记录激活Brainwash模式的操作
            else:
                logging.info('注入tune')  # 记录注入tune的操作
            asktext = self.tune + '\n' + text  # 在tune和text之间插入换行符，作为最终传递给ask方法的文本内容
        else:
            asktext = text  # 最终传递给ask方法的文本内容为text

        self.counter += 1  # 计数器自增1

        # 根据chatVer的值选择不同的方法调用，并遍历返回的数据
        for data in self.chatbot.ask(asktext) if self.chatVer == 1 else self.chatbot.ask_stream(text):
            if self.chatVer == 1:
                message = data["message"][len(prev_text):]  # 取出未处理部分的消息内容
            else:
                message = data  # 直接将data赋值给message变量

            # 如果消息中包含句号、感叹号、问号或换行符且complete_text长度大于3，则表示已经接收到完整的响应
            if ("。" in message or "！" in message or "？" in message or "\n" in message) and len(complete_text) > 3:
                complete_text += message  # 将当前消息追加到完整的响应文本中
                logging.info('ChatGPT流式响应：%s，@时间 %.2f秒' % (complete_text, time.time() - stime))  # 记录响应日志
                yield complete_text.strip()  # 返回完整的响应文本，并清除首尾的空白字符
                complete_text = ""  # 重置完整的响应文本
            else:
                complete_text += message  # 将当前消息追加到完整的响应文本中

            prev_text = data["message"] if self.chatVer == 1 else data  # 更新上一个消息的文本内容

        if complete_text.strip():  # 如果还有未返回的完整响应文本
            logging.info('ChatGPT流式响应：%s，@时间 %.2f秒' % (complete_text, time.time() - stime))  # 记录响应日志
            yield complete_text.strip()  # 返回完整的响应文本，并清除首尾的空白字符
