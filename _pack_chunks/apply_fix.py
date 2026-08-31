from pathlib import Path
import hashlib

OLD = "a868f821baf4729a19e86d5ac2dd3320ac47e83738ed1ee195512ee6dd4b3a1f"
OLD_LEN = 652616
TARGET = "c857bd767d3e7ac08dae2738f3c5baaf9decf8d602997c2a74864ae0da5a4a2b"
TARGET_LEN = 652984


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


p = Path("index.pck")
b = p.read_bytes() if p.exists() else b""
if sha(b) == TARGET and len(b) == TARGET_LEN:
    raise SystemExit(0)

parts = sorted(Path("_pack_chunks").glob("n????"))
if parts and sha(b) == OLD and len(b) == OLD_LEN:
    import bsdiff4
    raw = "".join(part.read_text().replace("\n", "").replace("\r", "") for part in parts)
    b = bsdiff4.patch(bytes(b), bytes.fromhex(raw))
    p.write_bytes(b)

if sha(b) != TARGET or len(b) != TARGET_LEN:
    raise SystemExit("pck hash %s len %s" % (sha(b), len(b)))
