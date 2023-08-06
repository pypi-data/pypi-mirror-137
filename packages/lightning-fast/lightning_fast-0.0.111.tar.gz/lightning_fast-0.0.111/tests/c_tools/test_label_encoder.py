import unittest
from utils.local_c_tools_compiler import LocalCToolsCompiler


class TestLabelEncoder(unittest.TestCase):

    test_strings = ["中文1", "中文2", "中文2", "符号，", "符号。", "符号；", "", "english"]
    test_encode_result = [0, 1, 1, 2, 3, 4, 5, 6]

    def setUp(self) -> None:
        LocalCToolsCompiler().compile_local_c_tools()

    def test_encoder_fit(self):
        # 测试是否能正常生成encoder
        encoders = LocalCToolsCompiler.import_encoders()
        label_encoder = encoders.LabelEncoder()
        one_d_string_vector = encoders.OneDStringVector(self.test_strings)
        label_encoder.encode_1d(one_d_string_vector, 2)
        print(label_encoder)

    def test_encoder_transform(self):
        # 测试是否能正常transform
        encoders = LocalCToolsCompiler.import_encoders()
        label_encoder = encoders.LabelEncoder()
        one_d_string_vector = encoders.OneDStringVector(self.test_strings)
        label_encoder.encode_1d(one_d_string_vector, 2)
        transform_result = label_encoder.transform_1d(one_d_string_vector, 2)
        self.assertListEqual(self.test_encode_result, list(transform_result))


if __name__ == "__main__":
    unittest.main()
