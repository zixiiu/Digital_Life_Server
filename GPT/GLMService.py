import logging
import os
import time

import GPT.machine_id
import GPT.tune as tune
import zhipuai

class GLMService():
    def __init__(self, args):
        r'''APIKey=your chatGLM api key
        chatVer is useless now
        brainwash 
        TODO:ADD model arg
        加入history，以拥有记忆
        '''
        self.model="chatglm_pro"#args.model
        logging.info('Initializing ChatGLM Service...')
        

        self.tune = tune.get_tune(args.character, args.model)

        self.brainwash = args.brainwash

        self.counter = 0
        # API connect to zhipuai
        zhipuai.api_key=args.APIKey
        logging.info('API ChatGLM initialized.')



    def ask(self, text):
        stime = time.time()
        	# 请求模型
        response = zhipuai.model_api.invoke(
            model=self.model,
            prompt=[
                {"role": "user", "content": self.tune+ text},
                
            ]
        )
        prev_text=response['data']['choices'][0]['content']
        logging.info('ChatGLM Response: %s, time used %.2f' % (prev_text, time.time() - stime))
        return prev_text

    def ask_stream(self, text):
        stime = time.time()
        #  #求asktext
        # if self.counter % 5 == 0 and self.chatVer == 1:
        #     if self.brainwash:
        #         logging.info('Brainwash mode activated, reinforce the tune.')
        #     else:
        #         logging.info('Injecting tunes')
        #     asktext = self.tune + '\n' + text
        # else:
        #     asktext = text
        asktext = self.tune + '\n' + text
        response = zhipuai.model_api.sse_invoke(
            model=self.model,
            prompt=[
                {"role": "user", "content": asktext},
                
            ]
        )

        # prev_text = ""
        complete_text = ""        
        self.counter += 1
        for event in response.events():
            if event.event == "add":
                message=event.data
                print(event.data,end='')
            elif event.event == "error" or event.event == "interrupted":
                message=event.data
                print(event.data)
            elif event.event == "finish":
                message=event.data+'\n'
                print(event.data)
                #   print(event.meta)
            else:
                message=event.data
                print(event.data)
            message=event.data
            #判断是否成句子
            if ("。" in message or "！" in message or "？" in message or "\n" in message) and len(complete_text) > 3:
                complete_text += message
                logging.info('chatGLM Stream Response: %s, @Time %.2f' % (complete_text, time.time() - stime))
                yield complete_text.strip()
                complete_text = ""
            else:
                complete_text += message
            pass
        if complete_text.strip():
            logging.info('chatGLM Stream Response: %s, @Time %.2f' % (complete_text, time.time() - stime))
            yield complete_text.strip()




def sentence_fix():
    #句子组装
    pass