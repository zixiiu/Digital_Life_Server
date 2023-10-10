import logging


def get_tune(character, model):
    if "3.5" in model:
        filename = character + '35.txt'
        logging.info('chatGPT prompt: %s' % filename)
        return open('GPT/prompts/' + filename, 'r', encoding='utf-8').read()
    if '4' in model:
        filename = character + '4.txt'
        logging.info('chatGPT prompt: %s' % filename)
        return open('GPT/prompts/' + filename, 'r', encoding='utf-8').read()


exceed_reply = """
你问的太多了，我们的毛都被你撸秃了，你自己去准备一个API，或者一小时后再来吧。
"""

error_reply = """
你等一下，我连接不上大脑了。你是不是网有问题，或者是账号填错了？
"""
