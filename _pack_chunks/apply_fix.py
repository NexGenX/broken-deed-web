from pathlib import Path
import hashlib

OLD = "c857bd767d3e7ac08dae2738f3c5baaf9decf8d602997c2a74864ae0da5a4a2b"
OLD_LEN = 652984
TARGET = "d036220ea3862add1181bdbe70cb6092a862a3af0793772b0a775062cb38e7c7"
TARGET_LEN = 652792


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


p = Path("index.pck")
b = p.read_bytes() if p.exists() else b""
if sha(b) == TARGET and len(b) == TARGET_LEN:
    raise SystemExit(0)

parts = sorted(Path("_pack_chunks").glob("o????"))
if parts and sha(b) == OLD and len(b) == OLD_LEN:
    import bsdiff4
    raw = "".join(part.read_text().replace("\n", "").replace("\r", "") for part in parts)
    b = bsdiff4.patch(bytes(b), bytes.fromhex(raw))
    p.write_bytes(b)

if sha(b) != TARGET or len(b) != TARGET_LEN:
    raise SystemExit("pck hash %s len %s" % (sha(b), len(b)))
