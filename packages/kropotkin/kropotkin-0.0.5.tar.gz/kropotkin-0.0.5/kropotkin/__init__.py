import zlib
from typing import Any

import hhc
import msgpack


def pack(raw_data):
    packed_bytes = msgpack.packb(raw_data)
    compress_bytes = zlib.compress(packed_bytes)

    if len(compress_bytes) < len(packed_bytes):
        bytes_to_use = compress_bytes
    else:
        bytes_to_use = packed_bytes

    number = int(bytes_to_use.hex(), 16)
    return hhc.hhc(number)


def unpack(packed_data):
    number = hhc.hhc_to_int(packed_data)
    try:
        compressed_bytes = bytes.fromhex("%x" % number)
    except ValueError:
        raise ValueError(f"Packed string is not valid: {packed_data}")
    try:
        packed_bytes = zlib.decompress(compressed_bytes)
    except zlib.error:
        # Looks like they weren't compressed
        packed_bytes = compressed_bytes
    data = msgpack.unpackb(packed_bytes)
    return data


def append(state: list, item: Any):
    return state + item
