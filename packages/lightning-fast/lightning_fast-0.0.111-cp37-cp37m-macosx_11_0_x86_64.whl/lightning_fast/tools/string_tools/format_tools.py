import string


class FormatTools:
    @classmethod
    def clear_punctuation(cls, sentence):
        """
        此方法用于去除所有标点符号
        :param sentence: 欲处理字符串
        :return: 处理后字符串
        """
        return sentence.translate(str.maketrans("", "", string.punctuation))
