# YT Downloader

```
 __   __ _____
 \ \ / /|_   _|   Build Version
  \ V /   | |     2.0.11
   | |    | |     Enjoy.
   |_|    |_|     @kitetsu67
```

**YouTube Video & Shorts Downloader** — sebuah CLI sederhana berbasis Python untuk
mengunduh video dan Shorts dari YouTube ke dalam format **MP4** (berbagai resolusi)
atau **MP3** (berbagai bitrate). Tampilannya dipercantik dengan
[`rich`](https://github.com/Textualize/rich) (banner, tabel menu, dan progress bar),
sedangkan proses unduhnya menggunakan [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).

> Powered by **Iddant ID**

---

## Fitur

- Unduh **YouTube Video** maupun **YouTube Shorts**.
- Format **MP4** dengan pilihan resolusi:
  - `144p`, `240p`, `360p`, `480p`, `720p (HD)`, `1080p (Full HD)`,
    `1440p (2K)`, `2160p (4K)`, atau **Best** (resolusi tertinggi yang tersedia).
- Format **MP3** dengan pilihan kualitas audio:
  - `128 kbps`, `192 kbps`, `256 kbps`, `320 kbps`.
- **Progress bar** real-time (kecepatan, ukuran file, estimasi waktu selesai).
- Output otomatis disimpan ke folder `downloads/` dengan format nama
  `Judul Video [ID].ext`.
- UI terminal yang **responsif** — tampilan menyesuaikan lebar terminal.

---

## Persyaratan

- **Python** 3.8 atau lebih baru
- **pip** (manajer paket Python)
- **FFmpeg** — wajib untuk:
  - menggabungkan video + audio saat mengunduh MP4 dengan resolusi tinggi,
  - mengkonversi audio ke MP3.

### Cek versi
```bash
python --version
pip --version
ffmpeg -version
```

---

## Instalasi

### 1. Clone repository
```bash
git clone https://github.com/ipkzone/YT-Downloader.git
cd YT-Downloader
```

### 2. (Opsional tapi disarankan) Buat virtual environment

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies Python
```bash
pip install -U yt-dlp rich
```

Atau, jika Anda membuat file `requirements.txt` berisi:
```
yt-dlp
rich
```
jalankan:
```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

**Windows**
1. Download dari https://www.gyan.dev/ffmpeg/builds/ (pilih `ffmpeg-release-essentials.zip`).
2. Ekstrak, lalu tambahkan folder `bin` ke **PATH** environment.
3. Verifikasi: `ffmpeg -version`.

**macOS (Homebrew)**
```bash
brew install ffmpeg
```

**Linux (Debian / Ubuntu)**
```bash
sudo apt update
sudo apt install -y ffmpeg
```

**Termux (Android)**
```bash
pkg update && pkg upgrade
pkg install python ffmpeg
pip install -U yt-dlp rich
```

---

## Cara Menjalankan

Dari direktori project, jalankan:
```bash
python main.py
```

Anda akan disambut oleh banner dan menu utama:

```
1. Download YouTube Video
2. Download YouTube Short
3. Keluar
```

### Alur penggunaan
1. Pilih **1** (Video) atau **2** (Short).
2. Masukkan **URL** YouTube saat diminta.
3. Pilih **format**:
   - `1` → MP4 (video)
   - `2` → MP3 (audio saja)
4. Pilih **resolusi** (kalau MP4) atau **kualitas audio** (kalau MP3).
5. Tunggu proses unduhan selesai — progress bar akan menampilkan
   kecepatan, ukuran, dan sisa waktu.
6. File hasil unduhan akan tersimpan otomatis di folder **`downloads/`**.

### Contoh
```bash
$ python main.py
# pilih: 1 (Download YouTube Video)
# URL  : https://www.youtube.com/watch?v=xxxxxxxxxxx
# format: 1 (MP4)
# resolusi: 6 (1080p Full HD)
# -> Selesai. File tersimpan di folder: downloads/
```

---

## Struktur Folder

```
.
├── main.py          # Script utama
├── downloads/       # Folder output (dibuat otomatis)
└── README.md
```

---

## Troubleshooting

| Masalah | Solusi |
|---|---|
| `ERROR: yt-dlp belum terinstall` | Jalankan `pip install -U yt-dlp` |
| `ERROR: rich belum terinstall` | Jalankan `pip install -U rich` |
| MP3 / merge MP4 gagal | Pastikan **FFmpeg** sudah terinstall dan ada di **PATH** |
| Error format / resolusi tidak tersedia | Coba pilih **Best** atau resolusi yang lebih rendah |
| `HTTP Error 403 / 429` | Update `yt-dlp` ke versi terbaru: `pip install -U yt-dlp` |
| URL Shorts gagal dideteksi | Tetap pilih menu **Download YouTube Short** dan tempelkan URL lengkap `https://www.youtube.com/shorts/...` |

> **Tips:** YouTube sering mengubah format internalnya. Kalau tiba-tiba ada yang
> error, langkah pertama biasanya cukup `pip install -U yt-dlp`.

---

## Disclaimer

Tool ini ditujukan untuk **penggunaan pribadi / edukasi**. Pastikan Anda
mematuhi [Terms of Service YouTube](https://www.youtube.com/t/terms) dan hak
cipta konten yang Anda unduh. Pengguna bertanggung jawab penuh atas
penggunaan tool ini.

---

## Credits

- Author: **@kitetsu67** — *Iddant ID*
- Library: [yt-dlp](https://github.com/yt-dlp/yt-dlp), [rich](https://github.com/Textualize/rich)
- Tooling: [FFmpeg](https://ffmpeg.org/)

