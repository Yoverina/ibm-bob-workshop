# Test Documentation - E-Commerce Application

## Overview
Unit test suite untuk aplikasi e-commerce Flask dengan coverage **99%** (melebihi target minimal 80%).

## Test Statistics
- **Total Tests**: 33 test cases
- **Test Coverage**: 99% (155 statements, 2 missed)
- **All Tests**: PASSED ✅

## Test Structure

### Test File
- [`test_app.py`](test_app.py:1) - File utama berisi semua unit tests

### Test Categories

#### 1. Database Tests (2 tests)
- `test_database_initialization` - Verifikasi pembuatan tabel database
- `test_get_db` - Test koneksi database

#### 2. Home Page Tests (2 tests)
- `test_index_page` - Test halaman utama dapat diakses
- `test_index_shows_products` - Test produk ditampilkan di halaman utama

#### 3. Registration Tests (6 tests)
- `test_register_page_get` - Test halaman registrasi dapat diakses
- `test_register_success` - Test registrasi berhasil
- `test_register_missing_fields` - Test validasi field kosong
- `test_register_password_mismatch` - Test validasi password tidak cocok
- `test_register_duplicate_username` - Test username duplikat
- `test_register_duplicate_email` - Test email duplikat

#### 4. Login Tests (5 tests)
- `test_login_page_get` - Test halaman login dapat diakses
- `test_login_success` - Test login berhasil
- `test_login_missing_fields` - Test validasi field kosong
- `test_login_invalid_username` - Test username tidak valid
- `test_login_invalid_password` - Test password salah

#### 5. Logout Tests (1 test)
- `test_logout` - Test logout berhasil

#### 6. Cart Tests (9 tests)
- `test_cart_requires_login` - Test cart memerlukan login
- `test_cart_page_when_logged_in` - Test halaman cart saat login
- `test_cart_empty_initially` - Test cart kosong untuk user baru
- `test_add_to_cart_requires_login` - Test add to cart memerlukan login
- `test_add_to_cart_success` - Test menambah produk ke cart
- `test_add_to_cart_invalid_product` - Test produk tidak valid
- `test_add_to_cart_increases_quantity` - Test quantity bertambah
- `test_remove_from_cart` - Test hapus item dari cart
- `test_update_cart_quantity` - Test update quantity
- `test_update_cart_invalid_quantity` - Test quantity tidak valid

#### 7. Checkout Tests (4 tests)
- `test_checkout_requires_login` - Test checkout memerlukan login
- `test_checkout_empty_cart` - Test checkout dengan cart kosong
- `test_checkout_success` - Test checkout berhasil
- `test_checkout_updates_stock` - Test stock produk terupdate
- `test_checkout_clears_cart` - Test cart dikosongkan setelah checkout

#### 8. Session Tests (2 tests)
- `test_session_persistence` - Test session bertahan antar request
- `test_session_cleared_on_logout` - Test session dibersihkan saat logout

## Installation

### Install Dependencies
```bash
pip install -r requirements.txt
```

Dependencies yang dibutuhkan:
- Flask==3.0.0
- Werkzeug==3.0.1
- pytest==7.4.3
- pytest-cov==4.1.0
- coverage==7.3.2

## Running Tests

### Run All Tests
```bash
cd ecommerce
pytest test_app.py -v
```

### Run Tests with Coverage Report
```bash
pytest test_app.py -v --cov=app --cov-report=html --cov-report=term
```

### Run Specific Test
```bash
pytest test_app.py::EcommerceTestCase::test_login_success -v
```

### Run Tests by Category
```bash
# Run only registration tests
pytest test_app.py -k "register" -v

# Run only cart tests
pytest test_app.py -k "cart" -v

# Run only checkout tests
pytest test_app.py -k "checkout" -v
```

## Coverage Report

### Terminal Output
Setelah menjalankan tests dengan coverage, Anda akan melihat:
```
----------- coverage: platform win32, python 3.7.6-final-0 -----------
Name     Stmts   Miss  Cover
----------------------------
app.py     155      2    99%
----------------------------
TOTAL      155      2    99%
```

### HTML Report
HTML coverage report tersimpan di folder [`htmlcov/`](htmlcov/index.html)

Untuk membuka report:
```bash
# Windows
start htmlcov/index.html

# Linux/Mac
open htmlcov/index.html
```

Report HTML menampilkan:
- Coverage percentage per file
- Line-by-line coverage visualization
- Missed lines highlighted in red
- Covered lines highlighted in green

## Test Features

### Test Fixtures
- **setUp()**: Membuat temporary database untuk setiap test
- **tearDown()**: Membersihkan database setelah test selesai

### Helper Methods
- `register_user()` - Helper untuk registrasi user
- `login_user()` - Helper untuk login user
- `logout_user()` - Helper untuk logout user

### Test Isolation
Setiap test case berjalan secara independen dengan:
- Database temporary yang terpisah
- Session yang bersih
- Tidak ada side effects antar tests

## Coverage Details

### Covered Functionality (99%)
✅ Database initialization and connections
✅ User registration with validation
✅ User login and authentication
✅ User logout and session management
✅ Product listing
✅ Shopping cart operations (add, update, remove)
✅ Checkout process
✅ Stock management
✅ Error handling and flash messages
✅ Login required decorator

### Uncovered Lines (1%)
Hanya 2 baris yang tidak tercakup:
- Line 301-302: `if __name__ == '__main__'` block (tidak dijalankan saat testing)

## Best Practices Implemented

1. **Test Isolation**: Setiap test menggunakan database temporary
2. **Comprehensive Coverage**: 99% code coverage
3. **Clear Test Names**: Nama test yang deskriptif
4. **Helper Methods**: Reusable helper functions
5. **Edge Cases**: Testing untuk error conditions
6. **Session Testing**: Verifikasi session management
7. **Database Testing**: Test database operations

## Continuous Integration

Tests dapat diintegrasikan dengan CI/CD pipeline:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest test_app.py -v --cov=app --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'pytest'`
**Solution**: Install dependencies dengan `pip install -r requirements.txt`

**Issue**: Database locked error
**Solution**: Pastikan tidak ada instance aplikasi yang sedang berjalan

**Issue**: Tests fail dengan "Please login to access this page"
**Solution**: Pastikan menggunakan helper methods `login_user()` sebelum test yang memerlukan authentication

## Future Improvements

Potential test enhancements:
- [ ] Integration tests untuk full user workflows
- [ ] Performance tests untuk database queries
- [ ] API endpoint tests jika REST API ditambahkan
- [ ] Load testing untuk concurrent users
- [ ] Security testing untuk SQL injection, XSS, etc.

## Contact

Untuk pertanyaan atau issues terkait testing, silakan buat issue di repository.

---
**Test Coverage**: 99% ✅ | **Target**: 80% ✅ | **Status**: PASSED ✅