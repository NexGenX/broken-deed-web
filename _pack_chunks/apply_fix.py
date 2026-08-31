from pathlib import Path
import hashlib

OLD = "2581fe92fa461b9910a7481aa5b07b845608579cd7ba052bf03d1cb02bcab783"
OLD_LEN = 646968
TARGET = "7a029bf7c4bc8d89d669b57db7e60f408f5aae229a0f65153c7bfcb118ebe6ba"
TARGET_LEN = 647176


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


p = Path("index.pck")
b = p.read_bytes() if p.exists() else b""
if sha(b) == TARGET and len(b) == TARGET_LEN:
    raise SystemExit(0)

parts = sorted(Path("_pack_chunks").glob("l????"))
if parts and sha(b) == OLD and len(b) == OLD_LEN:
    import bsdiff4
    raw = "".join(part.read_text().replace("\n", "").replace("\r", "") for part in parts)
    b = bsdiff4.patch(bytes(b), bytes.fromhex(raw))
    p.write_bytes(b)

if sha(b) != TARGET or len(b) != TARGET_LEN:
    raise SystemExit("pck hash %s len %s" % (sha(b), len(b)))
