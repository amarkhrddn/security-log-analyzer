"""Fungsi untuk membaca dan memvalidasi data log CSV."""
import csv
from pathlib import Path

REQUIRED_COLUMNS = {"timestamp", "ip_address", "username", "event", "status", "level"}


def load_logs(file_path):
    """Baca CSV, validasi kolom/baris, dan kembalikan list dictionary."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File input tidak ditemukan: {path}")
    if not path.is_file():
        raise ValueError(f"Path input bukan file: {path}")

    records = []
    with path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError("File CSV kosong atau tidak memiliki header.")
        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Kolom CSV belum lengkap: {', '.join(sorted(missing))}")

        for line_number, row in enumerate(reader, start=2):
            cleaned = {key: (value or "").strip() for key, value in row.items()}
            if not all(cleaned.get(column) for column in REQUIRED_COLUMNS):
                raise ValueError(f"Data tidak lengkap pada baris {line_number}.")
            if cleaned["level"].upper() not in {"LOW", "MEDIUM", "HIGH"}:
                raise ValueError(f"Level ancaman tidak valid pada baris {line_number}.")
            if cleaned["status"].upper() not in {"SUCCESS", "FAILED"}:
                raise ValueError(f"Status tidak valid pada baris {line_number}.")
            cleaned["level"] = cleaned["level"].upper()
            cleaned["status"] = cleaned["status"].upper()
            records.append(cleaned)

    if not records:
        raise ValueError("Tidak ada data log untuk diproses.")
    return records
