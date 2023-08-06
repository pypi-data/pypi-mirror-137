from ctypes import (
    Structure,
    c_int,
    c_char_p,
)

from lightning_fast.c_structs.uthash import UT_hash_handle


class UniqueWords(Structure):
    pass


UniqueWords._fields_ = [
    ("word", c_char_p),
    ("value", c_int),
    ("hh", UT_hash_handle),
]
