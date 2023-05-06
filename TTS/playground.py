import wave

import numpy as np
import pyaudio

from TTS.TTService import TTService

config_combo = [
        # ("TTS/models/CyberYunfei3k.json", "TTS/models/yunfei3k_69k.pth"),
        # ("TTS/models/paimon6k.json", "TTS/models/paimon6k_390k.pth"),
        # ("TTS/models/ayaka.json", "TTS/models/ayaka_167k.pth"),
        # ("TTS/models/ningguang.json", "TTS/models/ningguang_179k.pth"),
        # ("TTS/models/nahida.json", "TTS/models/nahida_129k.pth"),
        # ("TTS/models_unused/miko.json", "TTS/models_unused/miko_139k.pth"),
        # ("TTS/models_unused/yoimiya.json", "TTS/models_unused/yoimiya_102k.pth"),
        # ("TTS/models/noelle.json", "TTS/models/noelle_337k.pth"),
        # ("TTS/models_unused/yunfeimix.json", "TTS/models_unused/yunfeimix_122k.pth"),
        # ("TTS/models_unused/yunfeineo.json", "TTS/models_unused/yunfeineo_25k.pth"),
        # ("TTS/models/yunfeimix2.json", "TTS/models/yunfeimix2_47k.pth")
        ("TTS/models_unused/zhongli.json", "TTS/models_unused/zhongli_44k.pth"),
    ]
for cfg, model in config_combo:
    a = TTService(cfg, model, 'test', 1)
    p = pyaudio.PyAudio()
    audio = a.read('旅行者，今天是星期四，能否威我五十')
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=a.hps.data.sampling_rate,
                    output=True
                    )
    data = audio.astype(np.float32).tostring()
    stream.write(data)
    # Set the output file name
    output_file = "output.wav"

    # Set the audio properties
    num_channels = 1
    sample_width = 2  # Assuming 16-bit audio
    frame_rate = a.hps.data.sampling_rate

    # Convert audio data to 16-bit integers
    audio_int16 = (audio * np.iinfo(np.int16).max).astype(np.int16)

    # Open the output file in write mode
    with wave.open(output_file, 'wb') as wav_file:
        # Set the audio properties
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(frame_rate)

        # Write audio data to the file
        wav_file.writeframes(audio_int16.tobytes())