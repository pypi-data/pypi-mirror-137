import os
import pickle

N_BYTES = 2 ** 31
MAX_BYTES = 2 ** 31 - 1


class PickleObject(object):
    """
    这是一个pickle的补充类, 主要用来处理类型过大的时候, 可以用这个类来分批次序列化储存与读取
    """

    @classmethod
    def write_to_file(cls, file_path, data):
        bytes_out = pickle.dumps(data)
        with open(file_path, "wb") as f_out:
            for idx in range(0, len(bytes_out), MAX_BYTES):
                f_out.write(bytes_out[idx : idx + MAX_BYTES])

    @classmethod
    def read_from_file(cls, file_path):
        bytes_in = bytearray(0)
        input_size = os.path.getsize(file_path)
        with open(file_path, "rb") as f_in:
            for _ in range(0, input_size, MAX_BYTES):
                bytes_in += f_in.read(MAX_BYTES)
        data = pickle.loads(bytes_in)
        return data
