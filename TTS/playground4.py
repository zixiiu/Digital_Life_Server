import wave
import numpy as np
from .TTService import TTService

config_combo = [
    ("/root/vits_zh/miko.json", "/root/vits_zh/miko_139k.pth"),
#    ("/root/vits_zh/zhongli.json", "/root/vits_zh/zhongli_44k.pth"),
]

for cfg, model in config_combo:
    # 创建 TTService 实例
    tts_service = TTService(cfg, model, 'test', 1)

    # 生成音频
    #audio = tts_service.read('你好啊, 你是谁啊')
    audio = tts_service.read('啊, 又是那只野猫，那只死猫，它每一次都要欺负小咪，这一次我绝对不会饶他，小咪，我来了')

    # 设置输出文件名
    output_file = "output.wav"

    # 设置音频属性
    num_channels = 1
    sample_width = 2  # 假设为 16 位音频
    frame_rate = tts_service.hps.data.sampling_rate

    # 将音频数据转换为 16 位整数
    audio_int16 = (audio * np.iinfo(np.int16).max).astype(np.int16)

    # 以写入模式打开输出文件
    with wave.open(output_file, 'wb') as wav_file:
        # 设置音频属性
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(frame_rate)

        # 将音频数据写入文件
        wav_file.writeframes(audio_int16.tobytes())

    print(f"Audio saved to {output_file}")
