# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import traceback
from pathlib import Path
from typing import List, Union, Tuple

import librosa
import numpy as np

from .utils import (CharTokenizer, Hypothesis, ONNXRuntimeError,
                    OrtInferSession, TokenIDConverter, WavFrontend, get_logger,
                    read_yaml)

logging = get_logger()


class RapidParaformer():
    def __init__(self, config_path: Union[str, Path]) -> None:
        if not Path(config_path).exists():
            raise FileNotFoundError(f'{config_path} does not exist.')

        config = read_yaml(config_path)

        self.converter = TokenIDConverter(**config['TokenIDConverter'])
        self.tokenizer = CharTokenizer(**config['CharTokenizer'])
        self.frontend = WavFrontend(
            cmvn_file=config['WavFrontend']['cmvn_file'],
            **config['WavFrontend']['frontend_conf']
        )
        self.ort_infer = OrtInferSession(config['Model'])
        self.batch_size = config['Model']['batch_size']

    def __call__(self, wav_content: Union[str, np.ndarray, List[str]]) -> List:
        waveform_list = self.load_data(wav_content)
        waveform_nums = len(waveform_list)

        asr_res = []
        for beg_idx in range(0, waveform_nums, self.batch_size):
            end_idx = min(waveform_nums, beg_idx + self.batch_size)

            feats, feats_len = self.extract_feat(waveform_list[beg_idx:end_idx])

            try:
                am_scores, valid_token_lens = self.infer(feats, feats_len)
            except ONNXRuntimeError:
                logging.warning("input wav is silence or noise")
                preds = []
            else:
                preds = self.decode(am_scores, valid_token_lens)

            asr_res.extend(preds)
        return asr_res

    def load_data(self,
                  wav_content: Union[str, np.ndarray, List[str]]) -> List:
        def load_wav(path: str) -> np.ndarray:
            waveform, sr = librosa.load(path, sr=None)
            waveform = librosa.resample(waveform, orig_sr=sr, target_sr=16000)
            return waveform[None, ...]

        if isinstance(wav_content, np.ndarray):
            return [wav_content]

        if isinstance(wav_content, str):
            return [load_wav(wav_content)]

        if isinstance(wav_content, list):
            return [load_wav(path) for path in wav_content]

        raise TypeError(
            f'The type of {wav_content} is not in [str, np.ndarray, list]')

    def extract_feat(self,
                     waveform_list: List[np.ndarray]
                     ) -> Tuple[np.ndarray, np.ndarray]:
        feats, feats_len = [], []
        for waveform in waveform_list:
            speech, _ = self.frontend.fbank(waveform)
            feat, feat_len = self.frontend.lfr_cmvn(speech)
            feats.append(feat)
            feats_len.append(feat_len)

        feats = self.pad_feats(feats, np.max(feats_len))
        feats_len = np.array(feats_len).astype(np.int32)
        return feats, feats_len

    @staticmethod
    def pad_feats(feats: List[np.ndarray], max_feat_len: int) -> np.ndarray:
        def pad_feat(feat: np.ndarray, cur_len: int) -> np.ndarray:
            pad_width = ((0, max_feat_len - cur_len), (0, 0))
            return np.pad(feat, pad_width, 'constant', constant_values=0)

        feat_res = [pad_feat(feat, feat.shape[0]) for feat in feats]
        feats = np.array(feat_res).astype(np.float32)
        return feats

    def infer(self, feats: np.ndarray,
              feats_len: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        am_scores, token_nums = self.ort_infer([feats, feats_len])
        return am_scores, token_nums

    def decode(self, am_scores: np.ndarray, token_nums: int) -> List[str]:
        return [self.decode_one(am_score, token_num)
                for am_score, token_num in zip(am_scores, token_nums)]

    def decode_one(self,
                   am_score: np.ndarray,
                   valid_token_num: int) -> List[str]:
        yseq = am_score.argmax(axis=-1)
        score = am_score.max(axis=-1)
        score = np.sum(score, axis=-1)

        # pad with mask tokens to ensure compatibility with sos/eos tokens
        # asr_model.sos:1  asr_model.eos:2
        yseq = np.array([1] + yseq.tolist() + [2])
        hyp = Hypothesis(yseq=yseq, score=score)

        # remove sos/eos and get results
        last_pos = -1
        token_int = hyp.yseq[1:last_pos].tolist()

        # remove blank symbol id, which is assumed to be 0
        token_int = list(filter(lambda x: x not in (0, 2), token_int))

        # Change integer-ids to tokens
        token = self.converter.ids2tokens(token_int)
        text = self.tokenizer.tokens2text(token)
        return text[:valid_token_num - 1]


if __name__ == '__main__':
    project_dir = Path(__file__).resolve().parent.parent
    cfg_path = project_dir / 'resources' / 'config.yaml'
    paraformer = RapidParaformer(cfg_path)

    wav_file = '0478_00017.wav'
    for i in range(1000):
        result = paraformer(wav_file)
        print(result)
