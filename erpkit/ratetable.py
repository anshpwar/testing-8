"""Binary tax/freight rate table.

Layout (little endian): magic 'RTBL', u16 version, u16 count, u32 flags, then count x {4-byte code, u32 rate_bp}.
"""
import struct

HEADER = struct.Struct("<4sHHI")
ROW = struct.Struct("<4sI")


class BadRateTable(ValueError):
    pass


def load(path):
    data = open(path, "rb").read()
    if len(data) < HEADER.size:
        raise BadRateTable("truncated header")
    magic, version, count, flags = HEADER.unpack_from(data)
    if magic != b"RTBL" or version != 1:
        raise BadRateTable("bad magic or version")
    if len(data) != HEADER.size + count * ROW.size:
        raise BadRateTable("length does not match count")
    rates = {}
    for i in range(count):
        code, bp = ROW.unpack_from(data, HEADER.size + i * ROW.size)
        rates[code.rstrip(b"\0").decode("ascii")] = bp
    return {"version": version, "flags": flags, "rates": rates}


def dump(rates, flags=0):
    body = b"".join(ROW.pack(code.encode("ascii"), bp) for code, bp in sorted(rates.items()))
    return HEADER.pack(b"RTBL", 1, len(rates), flags) + body


def freight_bp(table, region, weight_kg):
    from . import rules
    return table["rates"].get(region, 0) + rules.freight_surcharge_bp(weight_kg)
