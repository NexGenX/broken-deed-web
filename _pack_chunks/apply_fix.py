from pathlib import Path
import base64
import hashlib
import sys

MID = "e4548a17ada52ee914678453bfcfaaf0b773e727c01599a6fd61bbc81a54bfa2"
OLD = "115d77a22037639cb9e59749ab9b5089cdb50ab1e7bb2f012daabc1b1c81460a"
TARGET = "dc0a602f407e78014526a8fa1732c0e0d2a0ba9a27eef1ed66732733952d71e6"
MID_LEN = 611416
OLD_LEN = 610968
TARGET_LEN = 615240


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


p = Path("index.pck")
b = bytearray(p.read_bytes())
h = sha(b)
if h == TARGET and len(b) == TARGET_LEN:
    raise SystemExit(0)

fix = Path("_pack_chunks/pck.fix")
if fix.exists() and len(b) == OLD_LEN and h != OLD:
    for line in fix.read_text().splitlines():
        if not line.strip():
            continue
        off, hx = line.split()
        b[int(off)] = int(hx, 16)
    h = sha(b)

parts = sorted(Path("_pack_chunks").glob("boot.??"))
if h == OLD and parts:
    raw = "".join(part.read_text().strip() for part in parts)
    if len(raw) > 16849 and raw[16849] == "p" and raw[16840:16849] == "RIMnPBAnB":
        raw = raw[:16849] + "v" + raw[16850:]
    import bsdiff4
    b = bytearray(bsdiff4.patch(bytes(b), base64.b64decode(raw)))
    h = sha(b)

figs = sorted(Path("_pack_chunks").glob("fig.??"))
if h == MID and figs:
    raw = "".join(part.read_text().strip() for part in figs)
    import bsdiff4
    b = bytearray(bsdiff4.patch(bytes(b), base64.b64decode(raw)))
    h = sha(b)

p.write_bytes(b)
if h != TARGET or len(b) != TARGET_LEN:
    raise SystemExit("pck hash %s len %s" % (h, len(b)))
