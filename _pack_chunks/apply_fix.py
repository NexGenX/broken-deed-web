from pathlib import Path
import base64
import hashlib

OLD = "56f9f47e411bb8135d64441e52719304e7dff943857856bf5f88755f43639768"
OLD_LEN = 637608
TARGET = "14ef14b849b14f50dac9c5fd21027e52173d8098eb0c9f3fc58df1261d2d1c8d"
TARGET_LEN = 637560


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


p = Path("index.pck")
b = p.read_bytes() if p.exists() else b""
if sha(b) == TARGET and len(b) == TARGET_LEN:
    raise SystemExit(0)

parts = sorted(Path("_pack_chunks").glob("w????"))
if parts and sha(b) == OLD and len(b) == OLD_LEN:
    import bsdiff4
    raw = "".join(part.read_text().replace("\n", "").replace("\r", "") for part in parts)
    raw = raw.replace("lz/tvtFmpeyAX9JLm", "lz/tvtFmveyAX9JLm")
    raw = raw.replace("sVQD+M/5povTAhANd", "sVQD+M/5vovTAhANd")
    b = bsdiff4.patch(bytes(b), base64.b64decode(raw))
    p.write_bytes(b)

if sha(b) != TARGET or len(b) != TARGET_LEN:
    raise SystemExit("pck hash %s len %s" % (sha(b), len(b)))
