"""Fungsi penyimpanan hasil analisis ke CSV dan JSON."""
import csv
import json
from pathlib import Path


def save_reports(result, output_dir, filtered_events=None):
    """Simpan ringkasan JSON dan daftar log CSV ke folder keluaran."""
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    events = result["events"] if filtered_events is None else filtered_events

    summary = {key: value for key, value in result.items() if key != "events"}
    with (folder / "summary.json").open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4, ensure_ascii=False)

    columns = ["timestamp", "ip_address", "username", "event", "status", "level"]
    with (folder / "filtered_logs.csv").open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(events)
