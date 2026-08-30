from pathlib import Path
import hashlib

BLOBS = {
    "fig.00": "f458713ac0c2b3dcf7f38f481ab880bdbf899fcb",
    "fig.01": "4b3d17a62bc86327a86d14bdf2a3194f0f0f26f2",
    "fig.02": "bd718c8fc6a1c22778df67211655c029516c4ec8",
    "fig.03": "3d454e79f7e25fa178bff41db8d7ed16f6aeef34",
    "fig.04": "ba6468bb81ed4c70dc4523e237dd98a34d2b3934",
    "fig.05": "c46e511d543f146d508e4306a0ee049dc2343005",
    "fig.06": "1d9b8a1fda5cf07787f19d72cfbfd839ff2bb856",
    "fig.07": "37e340c77a72cce61b859f11dfe91842c71ec117",
}

FIXES = {
    "fig.00": [("bXa2icp4r4R/a6fJbv", "bXa2icp4r4/a6fJbv")],
    "fig.01": [("whtUdbmBSUhsU+SS8boR", "whtUdbmBSU+SS8boR")],
    "fig.03": [
        ("mpCOX7DG2V4650dC8", "mpCOX7DG2V5650dC8"),
        ("XRbDTirmvfQbtqCI", "XRbDTirmvfbtqCI"),
        ("M29STjzB1NlfUHwv", "M29STjzB1NrfUHwv"),
    ],
    "fig.04": [("egvukLfyR1idzeWfj6", "egvukLfyR1zeWfj6")],
    "fig.05": [
        ("LR4QD/alB0poxtdOz", "LR4QD/alB0voxtdOz"),
        ("HfQQD0bQ7ypoiLzLY", "HfQQD0bQ7yvoiLzLY"),
        ("cn6B0kHVEkpin161d", "cn6B0kHVEkvin161d"),
    ],
    "fig.06": [
        ("QuQHRiNjJtCgFOm+", "QuQHRiIVYjJtCgFOm+"),
        ("c5mE/Ipxo+pozxbJLfa", "c5mE/Ipxo+vozxbJLfa"),
    ],
    "fig.07": [
        ("6Z/jq569YFVx5FCjP", "6Z/jq569YFXx5FCjP"),
        ("sknGzS9ZJrpeaUNqE", "sknGzS9ZJrveaUNqE"),
        ("2QQTzgubR5sSX1qdF", "2QQTzgubR5rSX1qdF"),
    ],
}


def blob_sha(text: str) -> str:
    data = text.encode("ascii")
    return hashlib.sha1(("blob %d\0" % len(data)).encode("ascii") + data).hexdigest()


root = Path("_pack_chunks")
for name, want in BLOBS.items():
    p = root / name
    text = p.read_text()
    if blob_sha(text) == want:
        print(name, "already exact")
        continue
    for old, new in FIXES.get(name, []):
        c = text.count(old)
        if c == 0:
            continue
        if c != 1:
            raise SystemExit("%s replace %r count %s" % (name, old, c))
        text = text.replace(old, new, 1)
    got = blob_sha(text)
    if got != want:
        raise SystemExit("%s blob %s want %s len %s" % (name, got, want, len(text)))
    p.write_text(text)
    print(name, "repaired", len(text))
print("all fig slices match local blobs")
