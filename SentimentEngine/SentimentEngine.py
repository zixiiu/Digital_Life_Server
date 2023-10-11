import logging

import numpy as np
import onnxruntime
from transformers import BertTokenizer


class SentimentEngine():
    def __init__(self, model_path):
        logging.info('Initializing Sentiment Engine...')
        onnx_model_path = model_path

        self.ort_session = onnxruntime.InferenceSession(onnx_model_path, providers=['CPUExecutionProvider'])

        self.tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

    def infer(self, text):
        # 使用BertTokenizer对文本进行分词和编码
        tokens = self.tokenizer(text, return_tensors="np")
        input_dict = {
            "input_ids": tokens["input_ids"],
            "attention_mask": tokens["attention_mask"],
        }
        # 将input_ids和attention_mask转换为int64类型
        input_dict["input_ids"] = input_dict["input_ids"].astype(np.int64)
        input_dict["attention_mask"] = input_dict["attention_mask"].astype(np.int64)
        # 使用ONNX运行时执行推理
        logits = self.ort_session.run(["logits"], input_dict)[0]
        # 计算概率分布
        probabilities = np.exp(logits) / np.sum(np.exp(logits), axis=-1, keepdims=True)
        # 获取预测结果
        predicted = np.argmax(probabilities, axis=1)[0]
        logging.info(f'Sentiment Engine Infer: {predicted}')
        return predicted


if __name__ == '__main__':
    # 情绪测试文本
    t = '哦，当然，如果PyCharm和VSCode之间搞不定，也许它们只是在争夺谁是最适合的编辑器冠军呢！'
    s = SentimentEngine('SentimentEngine/models/paimon_sentiment.onnx')
    # 0开心,1  害怕,2 生气,3 失落,4 好奇,5 戏谑
    r = s.infer(t)
    print(r)