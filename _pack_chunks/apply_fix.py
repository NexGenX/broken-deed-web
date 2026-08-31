from pathlib import Path
import hashlib

OLD = "3d3d5843d58ec0da3fbbe2f6d1dc22948e915a2e33ad40a1f78ed24339480678"
OLD_LEN = 640488
TARGET = "3919f379467cf911f0d695a3eec8f25a2120341c65af80ff678237795c701ddd"
TARGET_LEN = 644904


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


p = Path("index.pck")
b = p.read_bytes() if p.exists() else b""
if sha(b) == TARGET and len(b) == TARGET_LEN:
    raise SystemExit(0)

parts = sorted(Path("_pack_chunks").glob("j????"))
if parts and sha(b) == OLD and len(b) == OLD_LEN:
    import bsdiff4
    raw = "".join(part.read_text().replace("\n", "").replace("\r", "") for part in parts)
    b = bsdiff4.patch(bytes(b), bytes.fromhex(raw))
    p.write_bytes(b)

if sha(b) != TARGET or len(b) != TARGET_LEN:
    raise SystemExit("pck hash %s len %s" % (sha(b), len(b)))
