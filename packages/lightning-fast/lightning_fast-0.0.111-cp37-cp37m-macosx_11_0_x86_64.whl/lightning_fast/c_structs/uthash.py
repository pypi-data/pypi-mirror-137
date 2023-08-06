from ctypes import (
    POINTER,
    c_void_p,
    c_uint,
    Structure,
    c_uint32,
    sizeof,
    c_long,
    c_longlong,
    c_uint8,
)

if sizeof(c_void_p) == 4:
    # ptrdiff_t = c_int32
    ptrdiff_t = c_long
elif sizeof(c_void_p) == 8:
    # ptrdiff_t = c_int64
    ptrdiff_t = c_longlong
else:
    raise ValueError(f"什么乱遭的系统，指针大小为{sizeof(c_void_p)}")


class UT_hash_table(Structure):
    pass


class UT_hash_handle(Structure):
    pass


UT_hash_handle._fields_ = [
    ("tbl", POINTER(UT_hash_table)),
    ("prev", c_void_p),
    ("next", c_void_p),
    ("hh_prev", POINTER(UT_hash_handle)),
    ("hh_next", POINTER(UT_hash_handle)),
    ("key", c_void_p),
    ("keylen", c_uint),
    ("hashv", c_uint),
]


class UT_hash_bucket(Structure):
    _fields_ = [
        ("hh_head", POINTER(UT_hash_handle)),
        ("count", c_uint),
        ("expand_mult", c_uint),
    ]


UT_hash_table._fields_ = [
    ("buckets", POINTER(UT_hash_bucket)),
    ("num_buckets", c_uint),
    ("log2_num_buckets", c_uint),
    ("num_items", c_uint),
    ("tail", POINTER(UT_hash_handle)),
    ("hho", ptrdiff_t),
    ("ideal_chain_maxlen", c_uint),
    ("nonideal_items", c_uint),
    ("ineff_expands", c_uint),
    ("noexpand", c_uint),
    ("signature", c_uint32),
    ("bloom_sig", c_uint32),
    ("bloom_bv", POINTER(c_uint8)),
    ("bloom_nbits", c_uint8),
]
