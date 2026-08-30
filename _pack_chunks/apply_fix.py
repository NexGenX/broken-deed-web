from pathlib import Path
import base64
import hashlib
import sys

TARGET = "c1f6ca51b9631633ca80918c5e11bed27d8fc5fc415c0e9e84c166650e063844"
TARGET_LEN = 635736


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def assemble() -> bytes:
    parts = sorted(Path("_pack_chunks").glob("c??"))
    if not parts:
        raise SystemExit("no _pack_chunks/c??")
    raw = "".join(part.read_text().replace("\n", "").replace("\r", "") for part in parts)
    return base64.b64decode(raw)


p = Path("index.pck")
b = p.read_bytes() if p.exists() else b""
if sha(b) != TARGET or len(b) != TARGET_LEN:
    b = assemble()
    p.write_bytes(b)
if sha(b) != TARGET or len(b) != TARGET_LEN:
    raise SystemExit("pck hash %s len %s" % (sha(b), len(b)))
