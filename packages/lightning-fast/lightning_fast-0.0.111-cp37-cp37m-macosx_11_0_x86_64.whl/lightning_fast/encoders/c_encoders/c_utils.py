from ctypes import create_string_buffer


class DataConverter(object):
    @classmethod
    def string_list_to_c_string(cls, string_list):
        c_string = create_string_buffer("\t".join(string_list).encode("utf-8"))
        return c_string
