from pathlib import Path
import base64
import hashlib
import sys

OLD = "dc0a602f407e78014526a8fa1732c0e0d2a0ba9a27eef1ed66732733952d71e6"
OLD_LEN = 615240
TARGET = "c1f6ca51b9631633ca80918c5e11bed27d8fc5fc415c0e9e84c166650e063844"
TARGET_LEN = 635736


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


p = Path("index.pck")
b = p.read_bytes() if p.exists() else b""
if sha(b) == TARGET and len(b) == TARGET_LEN:
    raise SystemExit(0)

parts = sorted(Path("_pack_chunks").glob("n??"))
if parts and sha(b) == OLD and len(b) == OLD_LEN:
    import bsdiff4
    raw = "".join(part.read_text().replace("\n", "").replace("\r", "") for part in parts)
    b = bsdiff4.patch(bytes(b), base64.b64decode(raw))
    p.write_bytes(b)

cparts = sorted(Path("_pack_chunks").glob("c??"))
if (sha(b) != TARGET or len(b) != TARGET_LEN) and cparts:
    raw = "".join(part.read_text().replace("\n", "").replace("\r", "") for part in cparts)
    b = base64.b64decode(raw)
    p.write_bytes(b)

if sha(b) != TARGET or len(b) != TARGET_LEN:
    raise SystemExit("pck hash %s len %s" % (sha(b), len(b)))
