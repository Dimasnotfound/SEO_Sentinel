
# SEO Sentinel

SEO Sentinel adalah alat crawler SEO yang dirancang untuk membantu Anda menganalisis dan memantau elemen-elemen SEO pada sebuah website secara menyeluruh. Dengan antarmuka terminal interaktif yang didukung oleh Rich, SEO Sentinel menyajikan informasi penting seperti judul halaman, meta tags, struktur heading, internal links, dan masih banyak lagi. Alat ini sangat berguna bagi pengembang, pemilik website, dan konsultan SEO untuk mengoptimalkan performa website di mesin pencari.

## Fitur Utama

### Analisis SEO Komprehensif:
- **Judul Halaman:** Mengambil dan menampilkan judul halaman website.
- **Ekstraksi Meta Tags:** Mengidentifikasi dan menampilkan semua meta tags yang ada pada halaman.
- **Analisis Heading:** Menampilkan struktur heading (H1-H6) untuk memeriksa hierarki konten.
- **Deteksi Internal Links:** Menyaring dan menampilkan link internal yang terdapat pada halaman.

### Deteksi Error & Rekomendasi Optimasi:
- Mendeteksi gambar yang missing alt.
- Mengecek adanya broken links pada link internal.
- Menyediakan rekomendasi untuk memperbaiki meta description dan struktur heading.

- **Validasi URL:** Memastikan URL yang dimasukkan valid dengan menambahkan skema (http/https) secara otomatis bila diperlukan.
- **Tampilan Terminal Menarik:** Menggunakan library Rich untuk menampilkan laporan dengan tabel dan animasi loading yang interaktif.
- **Monitoring Berkala:** Opsional, memungkinkan pemantauan berkala untuk mendeteksi perubahan signifikan pada elemen SEO.
- **PDF Report Generation:** Menghasilkan laporan SEO dalam format PDF menggunakan xhtml2pdf dan template Jinja2.

## Instalasi

Pastikan Anda telah menginstal Python 3.6 atau versi yang lebih baru. Clone repository ini dan instal semua dependensi yang diperlukan menggunakan file `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Dependensi Utama
- `requests`: Untuk melakukan HTTP request.
- `beautifulsoup4`: Untuk parsing HTML.
- `rich`: Untuk tampilan output di terminal yang menarik.
- `xhtml2pdf`: Untuk mengonversi laporan HTML ke format PDF.
- `jinja2`: Untuk melakukan templating pada laporan HTML.

## Cara Penggunaan

### Jalankan Program Utama:
Buka terminal dan jalankan perintah berikut:

```bash
python seo_sentinel.py
```

### Masukkan URL:
Saat diminta, masukkan URL website yang ingin dianalisis. SEO Sentinel akan memvalidasi URL dan menambahkan skema jika belum ada.

### Lihat Hasil Analisis:
Program akan menampilkan laporan SEO di terminal yang mencakup informasi seperti judul halaman, meta tags, heading, internal links, dan error SEO (seperti gambar tanpa alt dan broken links) beserta rekomendasi optimasinya.

### Generate PDF Report:
Setelah analisis, Anda akan diberikan opsi untuk membuat laporan PDF. Cukup ketik `y` jika Anda ingin menghasilkan PDF report dari data yang telah dianalisis.

### Monitoring Berkala (Opsional):
Anda juga dapat mengaktifkan fitur monitoring berkala untuk memantau perubahan SEO secara real-time.

## Struktur Proyek

```bash
.
├── seo_sentinel.py         # Program utama: logika crawling, analisa SEO, tampilan terminal, dan monitoring
├── generate_pdf.py         # Modul untuk menghasilkan PDF report menggunakan xhtml2pdf dan Jinja2
├── requirements.txt        # Daftar dependensi proyek
└── README.md               # Dokumentasi proyek
```

## Kontribusi

Kontribusi sangat disambut! Jika Anda memiliki ide perbaikan, fitur baru, atau menemukan bug, silakan:

1. Fork repository ini.
2. Buat branch baru untuk fitur atau perbaikan Anda.
3. Commit perubahan Anda dan kirim pull request.
4. Buka issue jika ada pertanyaan atau saran.

## Lisensi

Proyek ini dilisensikan di bawah MIT License. Silakan lihat file LICENSE untuk informasi lebih lanjut.

## Kontak

Jika ada pertanyaan, saran, atau masukan, jangan ragu untuk menghubungi saya melalui email: dimaaspratama0@gmail.com

Terima kasih telah menggunakan SEO Sentinel. Selamat mengoptimalkan performa website Anda!
