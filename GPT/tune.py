import logging


def get_tune(character, model):
    if "3.5" in model or "35" in model:
        file_path = 'GPT/prompts/%s35.txt' % character
        logging.info('chatGPT-3.5 提示词: 读取自文件 %s' % file_path)
        return open(file_path, 'r', encoding='utf-8').read()
    elif "Y" in model or "E" in model:
        file_path = 'GPT/prompts/%s4.txt' % character
        logging.info('文心一言（ERNIE-Bot-4） 提示词：读取自文件 %s' % file_path)
        return open(file_path, 'r', encoding='utf-8').read()
    elif "4" in model:
        file_path = 'GPT/prompts/%s4.txt' % character
        logging.info('chatGPT-4 提示词: 读取自文件 %s' % file_path)
        return open(file_path, 'r', encoding='utf-8').read()
    else:
        logging.warning('No matching model found for character: %s' % character)
        return None


exceed_reply = """
你问的太多了，我们的毛都被你撸秃了，你自己去准备一个API，或者一小时后再来吧。
"""

error_reply = """
你等一下，我连接不上大脑了。你是不是网有问题，或者是账号填错了？
"""
