# Security Log Analyzer

Aplikasi command-line untuk membaca, memvalidasi, menganalisis, dan membuat laporan dari log keamanan berformat CSV. Dibuat menggunakan Python standard library tanpa dependency eksternal.

## Kebutuhan
- Python 3.9 atau lebih baru
- Tidak membutuhkan instalasi library tambahan

## Struktur folder
```text
security_log_analyzer/
├── main.py
├── README.md
├── security_analyzer/
│   ├── __init__.py
│   ├── loader.py
│   ├── analyzer.py
│   └── reporter.py
├── data/
│   └── security_logs.csv
└── output/
    ├── summary.json
    └── filtered_logs.csv
```

## Cara menjalankan
Buka terminal pada folder project, lalu jalankan:

```bash
python main.py
```

Menggunakan file input atau folder output berbeda:

```bash
python main.py --input data/security_logs.csv --output-dir output
```

Filter berdasarkan IP atau level:

```bash
python main.py --ip 192.168.1.15
python main.py --level HIGH
python main.py --ip 192.168.1.15 --level HIGH
```

Program akan membuat `output/summary.json` dan `output/filtered_logs.csv`.

## Format input
CSV wajib memiliki kolom:
`timestamp, ip_address, username, event, status, level`

Nilai `status` yang diterima adalah `SUCCESS` atau `FAILED`. Nilai `level` yang diterima adalah `LOW`, `MEDIUM`, atau `HIGH`.

## Fitur
1. Membaca dan memvalidasi CSV.
2. Menghapus baris duplikat.
3. Menghitung total log, login gagal, jumlah IP unik, dan rekap level.
4. Menandai IP mencurigakan jika memiliki minimal tiga login gagal.
5. Memfilter log berdasarkan IP dan/atau level.
6. Menyimpan laporan dalam JSON dan CSV.

## Struktur data dan alur module
- **List** menyimpan kumpulan baris log karena data diproses berurutan dan mudah difilter.
- **Dictionary** menyimpan satu baris CSV sebagai pasangan nama kolom dan nilai, serta menyimpan hasil rekap.
- **Set** menyimpan tanda tangan baris yang sudah ditemukan untuk menghapus duplikat secara efisien.
- `main.py` menjadi entry point dan mengatur argumen CLI.
- `loader.py` membaca serta memvalidasi CSV.
- `analyzer.py` membersihkan duplikat dan menghitung statistik.
- `reporter.py` menulis hasil ke file.
- Package `security_analyzer` berisi ketiga module tersebut. `main.py` mengimpor fungsi dari package.

## Penanganan error dan debugging
Program menangani file yang tidak ditemukan, CSV tanpa header/kolom wajib, baris kosong, status atau level yang tidak dikenal, dan batas deteksi yang tidak valid. Contoh uji error: jalankan `python main.py --input data/tidak_ada.csv`. Program menampilkan pesan `ERROR: File input tidak ditemukan...` dan berhenti dengan exit code 1, bukan traceback yang membingungkan.

## Referensi, library, dan bantuan
- Dokumentasi Python: https://docs.python.org/3/
- Modul standard library: `argparse`, `csv`, `json`, `pathlib`, `collections`.
- Dependency eksternal: tidak ada.
- Bantuan AI: ChatGPT digunakan untuk membantu perancangan struktur project, contoh implementasi, dan dokumentasi. Kode perlu dipahami dan diuji kembali oleh mahasiswa sebelum dikumpulkan.
