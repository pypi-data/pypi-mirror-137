import unittest
from lightning_fast.tools.meta_tools import SingletonMeta


class TestCLabelEncoder(unittest.TestCase):
    def test_singleton(self):
        class TmpClass(metaclass=SingletonMeta):
            def __init__(self, counter):
                counter.append(1)

        # 第一次传参因为此时没有对象创建，所以应该会进入__init__, 此时list长度应该为1
        counter_list_1 = []
        TmpClass(counter_list_1)
        self.assertTrue(len(counter_list_1) == 1)
        # 第二次传参因为此时已经有对象被创建, 所以不会进入__init__, 此时list长度应该为2
        counter_list_2 = []
        TmpClass(counter_list_2)
        self.assertTrue(len(counter_list_2) == 0)


if __name__ == "__main__":
    unittest.main()
