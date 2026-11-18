"""Fungsi analisis dan transformasi data log keamanan."""
from collections import Counter


def remove_duplicates(logs):
    """Hapus baris duplikat dengan mempertahankan urutan data."""
    seen = set()
    unique_logs = []
    for row in logs:
        signature = tuple(sorted(row.items()))
        if signature not in seen:
            seen.add(signature)
            unique_logs.append(row)
    return unique_logs


def analyze_logs(logs, failed_threshold=3):
    """Hitung statistik, pengelompokan IP, dan deteksi IP mencurigakan."""
    if failed_threshold < 1:
        raise ValueError("Batas login gagal minimal 1.")

    unique_logs = remove_duplicates(logs)
    failed = [row for row in unique_logs
              if row["event"].upper() == "LOGIN" and row["status"] == "FAILED"]

    ip_counts = Counter(row["ip_address"] for row in unique_logs)
    level_counts = Counter(row["level"] for row in unique_logs)
    failed_by_ip = Counter(row["ip_address"] for row in failed)

    # Dictionary comprehension untuk ringkasan tingkat ancaman.
    level_summary = {level: level_counts.get(level, 0)
                     for level in ("LOW", "MEDIUM", "HIGH")}

    suspicious_ips = {
        ip: count for ip, count in failed_by_ip.items()
        if count >= failed_threshold
    }

    return {
        "events": unique_logs,
        "total_logs": len(unique_logs),
        "duplicate_count": len(logs) - len(unique_logs),
        "failed_logins": len(failed),
        "unique_ip_count": len(set(row["ip_address"] for row in unique_logs)),
        "ip_event_counts": dict(ip_counts),
        "level_summary": level_summary,
        "suspicious_ips": suspicious_ips,
    }
