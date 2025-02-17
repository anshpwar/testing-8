"""Writes fixtures/rate_table.bin (a deliberate binary test fixture). Run from the repository root."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from erpkit import ratetable  # noqa: E402

RATES = {"EU": 1900, "UK": 2000, "US": 700, "APAC": 1000, "LATAM": 1600, "MEA": 1200}

if __name__ == "__main__":
    (ROOT / "fixtures").mkdir(exist_ok=True)
    (ROOT / "fixtures" / "rate_table.bin").write_bytes(ratetable.dump(RATES, flags=0x00010001))
