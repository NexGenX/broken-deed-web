from pathlib import Path

p = Path("index.pck")
b = bytearray(p.read_bytes())
fix = Path("_pack_chunks/pck.fix")
if not fix.exists():
    raise SystemExit(0)
for line in fix.read_text().splitlines():
    if not line.strip():
        continue
    off, hx = line.split()
    b[int(off)] = int(hx, 16)
p.write_bytes(b)
