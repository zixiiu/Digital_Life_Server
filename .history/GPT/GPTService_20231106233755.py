import logging
import os
import time
import GPT.machine_id
import GPT.tune as tune
import requests
import re

class GPTService():
    #替换一些听起来不太顺畅的文字
    def _replace_str(self, desstr):
        desstr = desstr.replace("！是派蒙！", "！我是派蒙！")
        desstr = desstr.replace("Paimon", "派蒙")
        desstr = desstr.replace("这是派蒙", "我是派蒙")
        return desstr

    #过滤特殊字符, 过滤除中英文, 数字, .,?:"!以外的其他字符
    def _filter_str(self, desstr):
        return ''.join(re.findall(u'[\u4e00-\u9fa5a-zA-Z0-9\u002E\u002C\u003B\u003A\u0022\u0021\u0020\u003F\u0027]', desstr))

    #dest_lang: EN, zh-CN
    def _translate(self, input_text, dest_lang):
        print("translate--> input:" + str(input_text))
        URL = "https://translation.googleapis.com/language/translate/v2"
        target = dest_lang
        key = "AIzaSyDPKOFt2ZN0Ncg176DzjkoixtmwX18puD4"
        q = input_text
        params = {'target': target, 'key': key, 'q': q}

        r = requests.get(url=URL, params=params)
        data = r.json()

        translated_text = data['data']['translations'][0]['translatedText']
        print("translate -> translated:" + translated_text)
        return translated_text

    def __init__(self, args):
        logging.info('Initializing ChatGPT Service...')
        self.chatVer = args.chatVer
        self.tune = tune.get_tune(args.character, args.model)
        self.counter = 0
        self.brainwash = args.brainwash

        if self.chatVer == 1:
            from revChatGPT.V1 import Chatbot
            config = {}
            if args.accessToken:
                logging.info('Try to login with access token.')
                config['access_token'] = args.accessToken
            else:
                logging.info('Try to login with email and password.')
                config['email'] = args.email
                config['password'] = args.password
            config['paid'] = args.paid
            config['model'] = args.model
            if type(args.proxy) == str:
                config['proxy'] = args.proxy

            self.chatbot = Chatbot(config=config)
            logging.info('WEB Chatbot initialized.')

        elif self.chatVer == 3:
            mach_id = GPT.machine_id.get_machine_unique_identifier()
            from revChatGPT.V3 import Chatbot
            if args.APIKey:
                logging.info('you have your own api key. Great.')
                api_key = args.APIKey
            else:
                logging.info('using custom API proxy, with rate limit.')                
                #os.environ['API_URL'] = "http://localhost:8000/v1/chat/completions"
                os.environ['API_URL'] = "http://75.63.212.152:41874/v1/"
                api_key = mach_id
            self.chatbot = Chatbot(api_key=api_key, proxy=args.proxy, system_prompt=self.tune, max_tokens=2048)
            logging.info('API Chatbot initialized.')

    def ask(self, text):
        print("--->ask text:" + text)
        text = self._translate(text, "EN")
        stime = time.time()
        if self.chatVer == 3:
            prev_text = self.chatbot.ask(text)
        # V1
        elif self.chatVer == 1:
            for data in self.chatbot.ask(
                    self.tune + '\n' + text
            ):
                prev_text = data["message"]
        #logging.info('ChatGPT Response: %s, time used %.2f' % (prev_text, time.time() - stime))
        print("--->response:" + prev_text)
        prev_text = self._filter_str(prev_text)
        print("--->filterred:" + prev_text)
        prev_text = self._translate(prev_text, "zh-CN")
        print("--->translated:" + prev_text)
        prev_text = self._replace_str(prev_text)
        print("--->replaced:" + prev_text)
        return prev_text

    def ask_stream(self, text):
        prev_text = ""
        complete_text = ""
        stime = time.time()
        if self.counter % 5 == 0 and self.chatVer == 1:
            if self.brainwash:
                logging.info('Brainwash mode activated, reinforce the tune.')
            else:
                logging.info('Injecting tunes')
            asktext = self.tune + '\n' + text
        else:
            asktext = text
        self.counter += 1
        for data in self.chatbot.ask(asktext) if self.chatVer == 1 else self.chatbot.ask_stream(text):
            message = data["message"][len(prev_text):] if self.chatVer == 1 else data
            if ("。" in message or "！" in message or "？" in message or "\n" in message) and len(complete_text) > 3:
                complete_text += message
                logging.info('ChatGPT Stream Response: %s, @Time %.2f' % (complete_text, time.time() - stime))
                yield complete_text.strip()
                complete_text = ""
            else:
                complete_text += message

            prev_text = data["message"] if self.chatVer == 1 else data

        if complete_text.strip():
            logging.info('ChatGPT Stream Response: %s, @Time %.2f' % (complete_text, time.time() - stime))
            yield complete_text.strip()