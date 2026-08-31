from pathlib import Path
import hashlib

OLD = "64c812a617872271cac1e892a90fc594ec6da60838a2def4ba206b8868ecc245"
OLD_LEN = 640312
TARGET = "3d3d5843d58ec0da3fbbe2f6d1dc22948e915a2e33ad40a1f78ed24339480678"
TARGET_LEN = 640488


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


p = Path("index.pck")
b = p.read_bytes() if p.exists() else b""
if sha(b) == TARGET and len(b) == TARGET_LEN:
    raise SystemExit(0)

parts = sorted(Path("_pack_chunks").glob("i????"))
if parts and sha(b) == OLD and len(b) == OLD_LEN:
    import bsdiff4
    raw = "".join(part.read_text().replace("\n", "").replace("\r", "") for part in parts)
    b = bsdiff4.patch(bytes(b), bytes.fromhex(raw))
    p.write_bytes(b)

if sha(b) != TARGET or len(b) != TARGET_LEN:
    raise SystemExit("pck hash %s len %s" % (sha(b), len(b)))
