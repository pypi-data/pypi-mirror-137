import os
from ctypes import CDLL, POINTER, c_int, c_char_p, c_char, cast
from functools import lru_cache

import numpy as np

from lightning_fast.c_structs.custom_structure import UniqueWords
from lightning_fast.encoders.c_encoders.c_utils import DataConverter
from lightning_fast.config import ROOT_PATH


class CEncoderPath(object):
    def __init__(self):
        self.source_dir = ROOT_PATH / "c_dynamic_library"

    @property
    @lru_cache()
    def all_libs(self):
        return os.listdir(self.source_dir)

    @property
    @lru_cache()
    def label_encoder_path(self):
        for file in self.all_libs:
            if file.startswith("liblabel_encoder"):
                return self.source_dir / file
        raise FileNotFoundError(f"Can not find lib file 'liblabel_encoder.*'")


class CLabelEncoder(object):
    """
    必须要自己手动调用free_encoder来释放产生的encoder内存
    """

    def __init__(self):
        self._c_label_encoder = None
        self._c_encoder_module = None
        self.init_c_encoder_module()

    def init_c_encoder_module(self):
        self._c_encoder_module = CDLL(CEncoderPath().label_encoder_path)
        self._c_encoder_module.get_encoder_by_string.argtypes = [c_char_p, c_char]
        self._c_encoder_module.get_encoder_by_string.restype = POINTER(UniqueWords)
        self._c_encoder_module.free_unique_words.argtypes = [
            POINTER(POINTER(UniqueWords))
        ]
        self._c_encoder_module.print_unique_words_summary.argtypes = [
            POINTER(POINTER(UniqueWords))
        ]
        self._c_encoder_module.save_encoder.argtypes = [
            POINTER(POINTER(UniqueWords)),
            c_char_p,
        ]
        self._c_encoder_module.load_encoder.argtypes = [c_char_p]
        self._c_encoder_module.load_encoder.restype = POINTER(UniqueWords)
        self._c_encoder_module.encode_words_by_string.argtypes = [
            POINTER(POINTER(UniqueWords)),
            c_char_p,
            c_int,
            c_char,
        ]
        self._c_encoder_module.encode_words_by_string.restype = POINTER(c_int)

    def fit(self, words):
        c_words = DataConverter.string_list_to_c_string(words)
        self._c_label_encoder = self._c_encoder_module.get_encoder_by_string(
            c_words, c_char("\t".encode("utf-8"))
        )

    def transform(self, words):
        c_words = DataConverter.string_list_to_c_string(words)
        result = self._c_encoder_module.encode_words_by_string(
            self._c_label_encoder, c_words, len(words), c_char("\t".encode("utf-8"))
        )
        buffer_as_ctypes_array = cast(result, POINTER(c_int * len(words)))[0]
        return np.frombuffer(buffer_as_ctypes_array, np.int32)

    def save_encoder(self, save_path):
        self._c_encoder_module.save_encoder(
            self._c_label_encoder, c_char_p(str(save_path).encode("utf-8"))
        )

    def load_encoder(self, load_path):
        self._c_label_encoder = self._c_encoder_module.load_encoder(
            c_char_p(str(load_path).encode("utf-8"))
        )

    def free_encoder(self):
        self._c_encoder_module.free_unique_words(self._c_label_encoder)

    @property
    def c_module_empty(self):
        return not self._c_encoder_module

    @property
    def c_encoder_empty(self):
        return not self._c_label_encoder

    def print_encoder(self):
        self._c_encoder_module.print_unique_words_summary(self._c_label_encoder)
