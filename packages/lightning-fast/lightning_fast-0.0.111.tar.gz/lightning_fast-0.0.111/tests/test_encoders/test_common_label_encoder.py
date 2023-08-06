import os
import unittest
from lightning_fast.config import ROOT_PATH
from lightning_fast.encoders.common_encoders.common_label_encoder import (
    CommonLabelEncoder,
)


class TestCommonLabelEncoder(unittest.TestCase):

    test_strings = ["中文1", "中文2", "中文2", "符号，", "符号。", "符号；", "", "english"]
    test_encode_result = [0, 1, 1, 2, 3, 4, 5, 6]
    tmp_encoder_path = ROOT_PATH / "tmp" / "test_common_label_encoder.tpl"

    def test_encoder_fit(self):
        # 测试是否能正常生成encoder
        encoder = CommonLabelEncoder()
        encoder.fit(self.test_strings)
        encoder.print_encoder()

    def test_encoder_transform(self):
        # 测试是否能正常transform
        encoder = CommonLabelEncoder()
        encoder.fit(self.test_strings)
        transform_result = encoder.transform(self.test_strings)
        self.assertListEqual(self.test_encode_result, transform_result)

    def test_encoder_save(self):
        # 测试能够正常保存
        self.assertFalse(os.path.exists(self.tmp_encoder_path))
        encoder = CommonLabelEncoder()
        encoder.save_encoder(self.tmp_encoder_path)
        self.assertTrue(os.path.exists(self.tmp_encoder_path))
        os.remove(self.tmp_encoder_path)
        self.assertFalse(os.path.exists(self.tmp_encoder_path))

    def test_encoder_load(self):
        # 测试能否正常加载
        encoder = CommonLabelEncoder()
        encoder.save_encoder(self.tmp_encoder_path)
        self.assertTrue(self.tmp_encoder_path)
        encoder = CommonLabelEncoder()
        encoder.load_encoder(self.tmp_encoder_path)
        encoder.fit(self.test_strings)
        transform_result = encoder.transform(self.test_strings)
        self.assertListEqual(self.test_encode_result, transform_result)
        os.remove(self.tmp_encoder_path)


if __name__ == "__main__":
    unittest.main()
