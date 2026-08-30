from pathlib import Path
import base64
import hashlib
import sys

OLD = "c1f6ca51b9631633ca80918c5e11bed27d8fc5fc415c0e9e84c166650e063844"
OLD_LEN = 635736
TARGET = "56f9f47e411bb8135d64441e52719304e7dff943857856bf5f88755f43639768"
TARGET_LEN = 637608


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


p = Path("index.pck")
b = p.read_bytes() if p.exists() else b""
if sha(b) == TARGET and len(b) == TARGET_LEN:
    raise SystemExit(0)

parts = sorted(Path("_pack_chunks").glob("u????"))
if parts and sha(b) == OLD and len(b) == OLD_LEN:
    import bsdiff4
    raw = "".join(part.read_text().replace("\n", "").replace("\r", "") for part in parts)
    b = bsdiff4.patch(bytes(b), base64.b64decode(raw))
    p.write_bytes(b)

if sha(b) != TARGET or len(b) != TARGET_LEN:
    raise SystemExit("pck hash %s len %s" % (sha(b), len(b)))
