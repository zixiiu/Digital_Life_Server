from flask import Flask, request, send_file
from pydub import AudioSegment
import sys
import time
import os
import torch
import logging
import soundfile

sys.path.append('TTS/vits')
import TTS.vits.commons as commons
import TTS.vits.utils as utils

from TTS.vits.models import SynthesizerTrn
from TTS.vits.text.symbols import symbols
from TTS.vits.text import text_to_sequence

app = Flask(__name__)

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

cfg_path = "TTS/models/peppa_9k.json"
model_path = "TTS/models/peppa_9k.pth"

def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.symbols, [] if is_symbol else hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm


class TTService():
    def __init__(self, cfg, model, char, speed):
        logging.info('Initializing TTS Service for %s...' % char)
        self.hps = utils.get_hparams_from_file(cfg)
        self.speed = speed
        self.net_g = SynthesizerTrn(
            len(symbols),
            self.hps.data.filter_length // 2 + 1,
            self.hps.train.segment_size // self.hps.data.hop_length,
            n_speakers=self.hps.data.n_speakers,
            **self.hps.model).cuda()
        _ = self.net_g.eval()
        _ = utils.load_checkpoint(model, self.net_g, None)

    def read(self, text):
        text = text.replace('~', '！')
        stn_tst = get_text(text, self.hps)
        with torch.no_grad():
            x_tst = stn_tst.cuda().unsqueeze(0)
            x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
            audio = self.net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.2, length_scale=self.speed)[0][
                0, 0].data.cpu().float().numpy()
        return audio

    def read_save(self, text, filename, sr):
        stime = time.time()
        au = self.read(text)
        soundfile.write(filename, au, sr)
        logging.info('VITS Synth Done, time used %.2f' % (time.time() - stime))

tts = TTService(cfg=cfg_path, model=model_path, char="char_var", speed=1.0)

@app.route('/v1/audio/speech', methods=['POST'])
def post_text_to_audio():
    text = request.json['input']
    audio = tts.read(text)
    soundfile.write('audio.wav', audio, 44100)
    sound = AudioSegment.from_wav("audio.wav")
    sound.export("audio.mp3", format="mp3")
    return send_file('audio.mp3', mimetype='audio/mp3')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
