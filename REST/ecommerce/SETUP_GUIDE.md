# Setup Guide - E-Commerce Website

## Prerequisites

Python 3.7 atau lebih baru harus sudah terinstal di komputer Anda.

## Instalasi pip (Jika belum ada)

### Cara 1: Download get-pip.py
1. Download get-pip.py dari: https://bootstrap.pypa.io/get-pip.py
2. Jalankan: `python get-pip.py`

### Cara 2: Reinstall Python
1. Download Python dari: https://www.python.org/downloads/
2. Saat instalasi, pastikan centang "Add Python to PATH" dan "Install pip"

## Instalasi Dependencies

Setelah pip terinstal, jalankan salah satu command berikut:

### Windows PowerShell:
```powershell
python -m pip install Flask==3.0.0 Werkzeug==3.0.1
```

### Windows Command Prompt:
```cmd
python -m pip install Flask==3.0.0 Werkzeug==3.0.1
```

### Atau menggunakan requirements.txt:
```powershell
python -m pip install -r requirements.txt
```

## Menjalankan Aplikasi

### Cara 1: Menggunakan Python langsung
```powershell
cd ecommerce
python app.py
```

### Cara 2: Double-click run.bat (Windows)
Double-click file `run.bat` di folder ecommerce

### Cara 3: Menggunakan Flask CLI
```powershell
cd ecommerce
set FLASK_APP=app.py
flask run
```

## Akses Aplikasi

Setelah aplikasi berjalan, buka browser dan akses:
```
http://127.0.0.1:5000
```

atau

```
http://localhost:5000
```

## Troubleshooting

### Error: "No module named 'flask'"
**Solusi**: Install Flask terlebih dahulu
```powershell
python -m pip install Flask Werkzeug
```

### Error: "No module named pip"
**Solusi**: Install pip terlebih dahulu (lihat bagian "Instalasi pip" di atas)

### Error: Port 5000 sudah digunakan
**Solusi**: Ubah port di file app.py, baris terakhir:
```python
app.run(debug=True, port=5001)  # Ganti 5000 ke 5001
```

### Error: "Permission denied"
**Solusi**: Jalankan terminal/command prompt sebagai Administrator

## Verifikasi Instalasi

Untuk memverifikasi bahwa semua dependencies terinstal dengan benar:

```powershell
python -c "import flask; import werkzeug; print('All dependencies installed successfully!')"
```

Jika tidak ada error, berarti instalasi berhasil!

## Struktur Database

Database SQLite akan dibuat otomatis saat pertama kali menjalankan aplikasi dengan nama `ecommerce.db` di folder ecommerce.

Tabel yang dibuat:
- **users**: Menyimpan data pengguna (id, username, email, password, created_at)
- **products**: Menyimpan data produk (id, name, description, price, stock, image_url, created_at)
- **cart**: Menyimpan keranjang belanja (id, user_id, product_id, quantity)

## Testing Aplikasi

1. Buka http://127.0.0.1:5000
2. Klik "Register" dan buat akun baru
3. Login dengan akun yang baru dibuat
4. Coba tambahkan produk ke keranjang
5. Lihat keranjang dan lakukan checkout

## Catatan Penting

- Aplikasi ini menggunakan SQLite database yang disimpan dalam file `ecommerce.db`
- Jangan hapus file `ecommerce.db` jika ingin menyimpan data pengguna dan transaksi
- Untuk reset database, hapus file `ecommerce.db` dan jalankan ulang aplikasi
- Secret key di `app.py` harus diganti untuk production use

## Kontak & Support

Jika mengalami masalah, pastikan:
1. Python versi 3.7+ terinstal
2. pip terinstal dan berfungsi
3. Flask dan Werkzeug terinstal
4. Tidak ada aplikasi lain yang menggunakan port 5000