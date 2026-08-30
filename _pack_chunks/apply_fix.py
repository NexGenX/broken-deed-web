from pathlib import Path
import base64
import hashlib
import sys

TARGET = "e4548a17ada52ee914678453bfcfaaf0b773e727c01599a6fd61bbc81a54bfa2"
OLD = "115d77a22037639cb9e59749ab9b5089cdb50ab1e7bb2f012daabc1b1c81460a"
TARGET_LEN = 611416
OLD_LEN = 610968

p = Path("index.pck")
b = bytearray(p.read_bytes())
h = hashlib.sha256(b).hexdigest()
if h == TARGET and len(b) == TARGET_LEN:
    raise SystemExit(0)

fix = Path("_pack_chunks/pck.fix")
if fix.exists() and len(b) == OLD_LEN and h != OLD:
    for line in fix.read_text().splitlines():
        if not line.strip():
            continue
        off, hx = line.split()
        b[int(off)] = int(hx, 16)
    h = hashlib.sha256(b).hexdigest()

parts = sorted(Path("_pack_chunks").glob("boot.??"))
if h == OLD and parts:
    raw = "".join(part.read_text().strip() for part in parts)
    import bsdiff4
    b = bytearray(bsdiff4.patch(bytes(b), base64.b64decode(raw)))
    h = hashlib.sha256(b).hexdigest()

p.write_bytes(b)
if h != TARGET or len(b) != TARGET_LEN:
    raise SystemExit("pck hash %s len %s" % (h, len(b)))
