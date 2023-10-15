import logging
import os
import time

import GPT.machine_id
import GPT.tune as tune


class GPTService():
    def __init__(self, args):
        logging.info('初始化ChatGPT服务…')
        self.chatVer = args.chatVer  # ChatGPT版本

        self.tune = tune.get_tune(args.character, args.model)  # 获取tune

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
                # 没有设置OpenAI APIKey 时使用geekerwan自建端口
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
        prev_text = ""
        complete_text = ""
        stime = time.time()
        if self.counter % 5 == 0 and self.chatVer == 1:
            if self.brainwash:
                logging.info('激活Brainwash模式，强化tune。')
            else:
                logging.info('注入tune')
            asktext = self.tune + '\n' + text
        else:
            asktext = text
        self.counter += 1
        for data in self.chatbot.ask(asktext) if self.chatVer == 1 else self.chatbot.ask_stream(text):
            message = data["message"][len(prev_text):] if self.chatVer == 1 else data

            if ("。" in message or "！" in message or "？" in message or "\n" in message) and len(complete_text) > 3:
                complete_text += message
                logging.info('ChatGPT流式响应：%s，@时间 %.2f秒' % (complete_text, time.time() - stime))
                yield complete_text.strip()
                complete_text = ""
            else:
                complete_text += message

            prev_text = data["message"] if self.chatVer == 1 else data

        if complete_text.strip():
            logging.info('ChatGPT流式响应：%s，@时间 %.2f秒' % (complete_text, time.time() - stime))
            yield complete_text.strip()
