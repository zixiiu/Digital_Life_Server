import sys
import time

sys.path.append('TTS/vits')

import soundfile
import os

os.environ["PYTORCH_JIT"] = "0"
import torch

import TTS.vits.commons as commons
import TTS.vits.utils as utils

from TTS.vits.models import SynthesizerTrn
from TTS.vits.text.symbols import symbols
from TTS.vits.text import text_to_sequence

import logging

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def get_text(text, hps):
    """
    将文本转换为数字序列

    Args:
        text (str): 要转换的文本
        hps: 模型超参数

    Returns:
        torch.LongTensor: 文本的数字序列
    """
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm


class TTService():
    def __init__(self, cfg, model, char, speed):
        """
        初始化 TTS 服务

        Args:
            cfg (str): 配置文件路径
            model (str): 模型路径
            char (str): 服务的特征 - 角色
            speed (float): 音频生成速度
        """
        logging.info('Initializing TTS Service for %s...' % char)
        self.hps = utils.get_hparams_from_file(cfg)
        self.speed = speed
        self.net_g = SynthesizerTrn(
            len(symbols),
            self.hps.data.filter_length // 2 + 1,
            self.hps.train.segment_size // self.hps.data.hop_length,
            **self.hps.model).cuda()
        _ = self.net_g.eval()
        _ = utils.load_checkpoint(model, self.net_g, None)

    def read(self, text):
        """
        读取文本并生成音频

        Args:
            text (str): 要转换为音频的文本

        Returns:
            numpy.ndarray: 生成的音频信号
        """
        text = text.replace('~', '！')
        stn_tst = get_text(text, self.hps)
        with torch.no_grad():
            x_tst = stn_tst.cuda().unsqueeze(0)
            x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
            audio = \
                self.net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.2, length_scale=self.speed)[0][
                    0, 0].data.cpu().float().numpy()
        return audio

    def read_save(self, text, filename, sr):
        """
        读取文本并生成音频，并保存到文件

        Args:
            text (str): 要转换为音频的文本
            filename (str): 保存音频的文件名
            sr (int): 采样率
        """
        stime = time.time()
        audio = self.read(text)
        soundfile.write(filename, audio, sr)
        logging.info('VITS Synth Done, time used %.2f' % (time.time() - stime))
