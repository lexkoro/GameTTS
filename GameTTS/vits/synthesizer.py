import json
import random

import torch
import numpy as np
import pysbd

from vits import commons, utils
from vits.models import SynthesizerTrn
from vits.text.symbols import symbols
from vits.text import text_to_sequence



class Synthesizer:
    def __init__(self, config_path):
        self.hps_config = self.load_config(config_path)
        self.gen_model = None
        self.speaker_map = None
        self.segmenter = pysbd.Segmenter(language="de", clean=True)
        self.use_cuda = torch.cuda.is_available()

    def enable_disable_cuda(self, use_cuda):
        self.use_cuda = use_cuda

    def to_cuda(self, x):
        if self.use_cuda:
            x.cuda()
        return x

    def init_speaker_map(self, speaker_path):
        with open(speaker_path) as json_file:
            self.speaker_map = json.load(json_file)

    def get_speaker_by_id(self, speaker_id):
        for key, val in self.speaker_map.items():
            if str(speaker_id) == val:
                return key

    def get_text(self, text):
        text_norm = text_to_sequence(text, self.hps_config.data.text_cleaners)
        if self.hps_config.data.add_blank:
            text_norm = commons.intersperse(text_norm, 0)
        text_norm = torch.LongTensor(text_norm)
        return text_norm

    def load_config(self, conf_path):
        return utils.get_hparams_from_file(conf_path)

    def load_model(self, model_path):
        self.gen_model = SynthesizerTrn(
            len(symbols),
            self.hps_config.data.filter_length // 2 + 1,
            self.hps_config.train.segment_size // self.hps_config.data.hop_length,
            n_speakers=self.hps_config.data.n_speakers,
            **self.hps_config.model
        )
        # move model to cuda
        if self.use_cuda:
            self.gen_model.cuda()
            
        _ = self.gen_model.eval()
        _ = utils.load_checkpoint(model_path, self.gen_model)


    def synthesize(self, text, speaker_id=0, speech_param=None):
        wavs = []
        seg_text = self.segmenter.segment(text)

        for idx, text in enumerate(seg_text):
            stn_tst = self.get_text(text)
            with torch.no_grad():
                x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
                sid = torch.LongTensor([int(speaker_id)])
                
                # move objects to cuda
                if self.use_cuda:
                    x_tst_lengths = x_tst_lengths.cuda()
                    sid = sid.cuda()
                    stn_tst = stn_tst.cuda()
                x_tst = stn_tst.unsqueeze(0)

                audio = (
                    self.gen_model.infer(
                        x_tst,
                        x_tst_lengths,
                        sid=sid,
                        noise_scale=float(speech_param["speech_var_a"]),
                        noise_scale_w=float(speech_param["speech_var_b"]),
                        length_scale=float(speech_param["speech_speed"]),
                    )[0][0, 0]
                    .data.cpu()
                    .float()
                    .numpy()
                )

            wavs += list(audio)
            pause_range = random.randrange(6000, 10000)
            if idx < len(seg_text) - 1:
                wavs += [0] * pause_range

        return np.array(wavs, dtype=np.float32)

    def save_audio(self, file_path, audio):
        pass
