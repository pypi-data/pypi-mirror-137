from collections import deque, OrderedDict
from copy import deepcopy
import joblib
import numpy as np
import pandas as pd
from tqdm import tqdm


class CommonLabelEncoder(object):
    def __init__(self, transform_shift=0):
        """
        此处选择编码移动数量，比如想从1开始则shift=1
        """
        self.hash_dict = OrderedDict()
        self.inverse_dict = OrderedDict()
        self.counter = 0
        self.transform_shift = transform_shift

    @property
    def labels_in_order(self):
        return list(self.hash_dict.keys())

    def fit(self, words, data_type="one", reset=True):
        """
        fit_type代表输入是否是一个嵌套结构
        """
        if reset:
            self.hash_dict = OrderedDict()
            self.inverse_dict = OrderedDict()
        self.counter = 0
        if isinstance(words, np.ndarray) or isinstance(words, pd.Series):
            if words.size == 0:
                return
        else:
            if not words:
                return
        if data_type == "one":
            self._one_depth_fit(words)
        elif data_type == "nested":
            self._nested_fit(words)

    def _one_depth_fit(self, words):
        counter = 0
        for word in words:
            if word not in self.hash_dict:
                self.hash_dict[word] = counter
                self.inverse_dict[counter] = word
                counter += 1
        self.counter = counter

    @classmethod
    def judge_custom_support_iterable(cls, item):
        return (
            isinstance(item, list)
            or isinstance(item, pd.Series)
            or isinstance(item, np.ndarray)
        )

    def _nested_fit(self, words):
        if not self.judge_custom_support_iterable(words):
            raise ValueError(f"输入类型不能为{type(words)}")
        bar = tqdm()
        counter = 0
        cache_queue = deque()
        cache_queue.append(words)
        while cache_queue:
            current_item = cache_queue.popleft()
            if self.judge_custom_support_iterable(current_item):
                for item in current_item:
                    cache_queue.append(item)
            else:
                if current_item not in self.hash_dict:
                    self.hash_dict[current_item] = counter
                    self.inverse_dict[counter] = current_item
                    bar.update(1)
                    counter += 1
        self.counter = counter

    def transform(self, new_words, data_type="one"):
        if data_type == "one":
            return self._common_transform(
                new_words, self.hash_dict, self.transform_shift
            )
        elif data_type == "nested":
            return self._common_nested_transform(
                new_words, self.hash_dict, self.transform_shift
            )
        else:
            raise ValueError(f"data_type不能为{data_type}")

    def inverse_transform(self, encoded_words, data_type="one"):
        if data_type == "one":
            return self._common_transform(
                encoded_words, self.inverse_dict, self.transform_shift, inverse=True
            )
        elif data_type == "nested":
            return self._common_nested_transform(
                encoded_words, self.inverse_dict, self.transform_shift, inverse=True
            )
        else:
            raise ValueError(f"data_type不能为{data_type}")

    @classmethod
    def _common_transform(cls, words, mapping, shift, inverse=False):
        result = []
        for word in words:
            if not inverse:
                code = mapping.get(word, -1)
                code = code if code == -1 else code + shift
            else:
                code = mapping.get(word - shift, -1)
                code = str(code)
            result.append(code)
        return result

    def _common_nested_transform(self, words, mapping, shift, inverse=False):
        bar = tqdm()
        result = deepcopy(words)
        cache = deque()
        cache.append(result)
        while cache:
            current_item = cache.popleft()
            if self.judge_custom_support_iterable(current_item):
                if len(current_item) > 0:
                    current_item_children = (
                        current_item[0]
                        if not isinstance(current_item, pd.Series)
                        else current_item.iloc[0]
                    )
                    if not self.judge_custom_support_iterable(current_item_children):
                        current_item[:] = self._common_transform(
                            current_item, mapping, shift, inverse=inverse
                        )
                        bar.update(1)
                    else:
                        for sub_item in current_item:
                            cache.append(sub_item)
        return result

    def print_encoder(self):
        print(self.hash_dict)

    def save_encoder(self, save_path):
        joblib.dump(self, save_path)

    @classmethod
    def load_encoder(cls, load_path):
        return joblib.load(load_path)
