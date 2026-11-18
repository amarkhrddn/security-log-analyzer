"""Entry point for Security Log Analyzer CLI."""
import argparse
from pathlib import Path

from security_analyzer.loader import load_logs
from security_analyzer.analyzer import analyze_logs
from security_analyzer.reporter import save_reports


def build_parser():
    """Build and return the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Analisis log keamanan dari file CSV."
    )
    parser.add_argument(
        "--input", default="data/security_logs.csv",
        help="Path file input CSV (default: data/security_logs.csv)"
    )
    parser.add_argument(
        "--output-dir", default="output",
        help="Folder penyimpanan laporan (default: output)"
    )
    parser.add_argument(
        "--ip", help="Tampilkan ringkasan untuk IP tertentu"
    )
    parser.add_argument(
        "--level", choices=["LOW", "MEDIUM", "HIGH"],
        help="Filter berdasarkan tingkat ancaman"
    )
    return parser


def main():
    """Load, analyze, optionally filter, and save security log reports."""
    args = build_parser().parse_args()
    try:
        logs = load_logs(args.input)
        result = analyze_logs(logs)

        filtered = result["events"]
        if args.ip:
            filtered = [row for row in filtered if row["ip_address"] == args.ip]
        if args.level:
            filtered = [row for row in filtered if row["level"] == args.level]

        save_reports(result, args.output_dir, filtered_events=filtered)
        print("=== SECURITY LOG ANALYZER ===")
        print(f"Total log valid       : {result['total_logs']}")
        print(f"Login gagal           : {result['failed_logins']}")
        print(f"IP unik               : {result['unique_ip_count']}")
        print(f"IP mencurigakan       : {len(result['suspicious_ips'])}")
        print(f"Filter ditampilkan    : {len(filtered)} log")
        if result["suspicious_ips"]:
            print("Daftar IP mencurigakan:")
            for ip, count in result["suspicious_ips"].items():
                print(f" - {ip}: {count} login gagal")
        print(f"Laporan tersimpan di  : {Path(args.output_dir).resolve()}")
    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"ERROR: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
