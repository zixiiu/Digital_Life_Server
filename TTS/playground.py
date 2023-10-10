import wave

import numpy as np
import pyaudio

from TTS.TTService import TTService

config_combo = [
    # 配置文件和模型路径的组合
    ("TTS/models/CyberYunfei3k.json", "TTS/models/yunfei3k_69k.pth"),
    ("TTS/models/paimon6k.json", "TTS/models/paimon6k_390k.pth"),
    ("TTS/models/ayaka.json", "TTS/models/ayaka_167k.pth"),
    ("TTS/models/ningguang.json", "TTS/models/ningguang_179k.pth"),
    ("TTS/models/nahida.json", "TTS/models/nahida_129k.pth"),
    ("TTS/models_unused/miko.json", "TTS/models_unused/miko_139k.pth"),
    ("TTS/models_unused/yoimiya.json", "TTS/models_unused/yoimiya_102k.pth"),
    ("TTS/models/noelle.json", "TTS/models/noelle_337k.pth"),
    ("TTS/models_unused/yunfeimix.json", "TTS/models_unused/yunfeimix_122k.pth"),
    ("TTS/models_unused/yunfeineo.json", "TTS/models_unused/yunfeineo_25k.pth"),
    ("TTS/models/yunfeimix2.json", "TTS/models/yunfeimix2_47k.pth"),
    ("TTS/models_unused/zhongli.json", "TTS/models_unused/zhongli_44k.pth"),
]

# 遍历配置文件和模型路径的组合
for cfg, model in config_combo:
    # 初始化 TTS 服务
    a = TTService(cfg, model, 'test', 1)

    # 创建 PyAudio 对象
    p = pyaudio.PyAudio()

    # 生成音频
    audio = a.read('旅行者，今天是星期四，能否威我五十')

    # 打开音频流
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=a.hps.data.sampling_rate,
                    output=True)

    # 将音频数据转换为字节流
    data = audio.astype(np.float32).tostring()

    # 播放音频
    stream.write(data)

    # 设置输出文件名
    output_file = "output.wav"

    # 设置音频属性
    num_channels = 1
    sample_width = 2  # 假设为 16 位音频
    frame_rate = a.hps.data.sampling_rate

    # 将音频数据转换为 16 位整数
    audio_int16 = (audio * np.iinfo(np.int16).max).astype(np.int16)

    # 以写模式打开输出文件
    with wave.open(output_file, 'wb') as wav_file:
        # 设置音频属性
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(frame_rate)

        # 将音频数据写入文件
        wav_file.writeframes(audio_int16.tobytes())