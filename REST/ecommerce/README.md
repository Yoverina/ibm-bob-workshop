# E-Commerce Website

Website e-commerce sederhana yang dibangun menggunakan Python Flask dengan fitur register dan login.

## Fitur

- ✅ Registrasi pengguna baru
- ✅ Login dan logout
- ✅ Daftar produk
- ✅ Keranjang belanja
- ✅ Checkout
- ✅ Manajemen stok produk
- ✅ Database SQLite

## Struktur Proyek

```
ecommerce/
├── app.py                 # Aplikasi Flask utama
├── requirements.txt       # Dependencies Python
├── ecommerce.db          # Database SQLite (dibuat otomatis)
├── templates/            # Template HTML
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── cart.html
├── static/               # File statis
│   └── css/
│       └── style.css
└── models/               # (untuk ekspansi di masa depan)
```

## Instalasi

1. Pastikan Python 3.7+ sudah terinstal di komputer Anda

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Cara Menjalankan

1. Masuk ke direktori ecommerce:
```bash
cd ecommerce
```

2. Jalankan aplikasi:
```bash
python app.py
```

3. Buka browser dan akses:
```
http://127.0.0.1:5000
```

## Cara Menggunakan

### 1. Registrasi
- Klik tombol "Register" di navbar
- Isi form dengan username, email, dan password
- Klik "Register" untuk membuat akun

### 2. Login
- Klik tombol "Login" di navbar
- Masukkan username dan password
- Klik "Login"

### 3. Belanja
- Setelah login, Anda dapat melihat daftar produk di halaman utama
- Klik "Add to Cart" untuk menambahkan produk ke keranjang
- Klik "Cart" di navbar untuk melihat keranjang belanja
- Atur jumlah produk atau hapus item dari keranjang
- Klik "Checkout" untuk menyelesaikan pembelian

## Produk Default

Aplikasi sudah dilengkapi dengan 6 produk contoh:
- Laptop (Rp 15.000.000)
- Smartphone (Rp 8.000.000)
- Headphones (Rp 2.000.000)
- Smartwatch (Rp 3.000.000)
- Tablet (Rp 5.000.000)
- Camera (Rp 12.000.000)

## Teknologi yang Digunakan

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS
- **Security**: Werkzeug (password hashing)

## Catatan Keamanan

⚠️ **PENTING**: Aplikasi ini adalah contoh sederhana untuk pembelajaran. Untuk production:
- Ganti `app.secret_key` dengan key yang aman
- Gunakan database yang lebih robust (PostgreSQL, MySQL)
- Tambahkan validasi input yang lebih ketat
- Implementasi HTTPS
- Tambahkan CSRF protection
- Implementasi rate limiting
## Testing

### Unit Tests
Proyek ini dilengkapi dengan comprehensive unit tests dengan coverage **99%**.

#### Menjalankan Tests
```bash
# Cara 1: Menggunakan batch script (Windows)
run_tests.bat

# Cara 2: Manual dengan pytest
cd ecommerce
pytest test_app.py -v --cov=app --cov-report=html --cov-report=term
```

#### Test Coverage
- **Total Tests**: 33 test cases
- **Coverage**: 99% (155 statements, 2 missed)
- **Status**: All tests PASSED ✅

#### HTML Coverage Report
Setelah menjalankan tests, buka HTML report:
```bash
start htmlcov/index.html
```

Untuk dokumentasi lengkap tentang testing, lihat [TEST_DOCUMENTATION.md](TEST_DOCUMENTATION.md)


## Pengembangan Lebih Lanjut

Fitur yang bisa ditambahkan:
- [ ] Payment gateway integration
- [ ] Order history
- [ ] Product search dan filter
- [ ] Admin panel untuk manage produk
- [ ] Product reviews dan ratings
- [ ] Email notifications
- [ ] Password reset functionality
- [ ] User profile management

## Lisensi

Proyek ini dibuat untuk tujuan pembelajaran.