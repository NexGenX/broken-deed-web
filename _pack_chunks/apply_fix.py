from pathlib import Path
import base64
import hashlib

OLD = "14ef14b849b14f50dac9c5fd21027e52173d8098eb0c9f3fc58df1261d2d1c8d"
OLD_LEN = 637560
TARGET = "356513ae91fd8232ad08af590d959917bc0d70d003aa79e32f109469813a8036"
TARGET_LEN = 640120


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


p = Path("index.pck")
b = p.read_bytes() if p.exists() else b""
if sha(b) == TARGET and len(b) == TARGET_LEN:
    raise SystemExit(0)

parts = sorted(Path("_pack_chunks").glob("x????"))
if parts and sha(b) == OLD and len(b) == OLD_LEN:
    import bsdiff4
    raw = "".join(part.read_text().replace("\n", "").replace("\r", "") for part in parts)
    b = bsdiff4.patch(bytes(b), base64.b64decode(raw))
    p.write_bytes(b)

if sha(b) != TARGET or len(b) != TARGET_LEN:
    raise SystemExit("pck hash %s len %s" % (sha(b), len(b)))
