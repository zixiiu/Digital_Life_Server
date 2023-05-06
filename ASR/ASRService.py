import logging
import time

from ASR.rapid_paraformer import RapidParaformer


class ASRService():
    def __init__(self, config_path):
        logging.info('Initializing ASR Service...')
        self.paraformer = RapidParaformer(config_path)

    def infer(self, wav_path):
        stime = time.time()
        result = self.paraformer(wav_path)
        logging.info('ASR Result: %s. time used %.2f.' % (result, time.time() - stime))
        return result[0]

if __name__ == '__main__':
    config_path = 'ASR/resources/config.yaml'

    service = ASRService(config_path)

    # print(wav_path)
    wav_path = 'ASR/test_wavs/0478_00017.wav'
    result = service.infer(wav_path)
    print(result)