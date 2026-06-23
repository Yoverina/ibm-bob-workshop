import unittest
import os
import tempfile
import sqlite3
from app import app, init_db, get_db
from werkzeug.security import generate_password_hash


class EcommerceTestCase(unittest.TestCase):
    """Test cases for the e-commerce application"""

    def setUp(self):
        """Set up test client and initialize test database"""
        # Create a temporary database file
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['DATABASE'] = self.db_path
        
        # Update the DATABASE constant in app module
        import app as app_module
        app_module.DATABASE = self.db_path
        
        self.client = app.test_client()
        
        # Initialize database
        with app.app_context():
            init_db()

    def tearDown(self):
        """Clean up after tests"""
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def register_user(self, username='testuser', email='test@example.com', 
                     password='testpass123', confirm_password='testpass123'):
        """Helper method to register a user"""
        return self.client.post('/register', data={
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirm_password
        }, follow_redirects=True)

    def login_user(self, username='testuser', password='testpass123'):
        """Helper method to login a user"""
        return self.client.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)

    def logout_user(self):
        """Helper method to logout a user"""
        return self.client.get('/logout', follow_redirects=True)

    # Database Tests
    def test_database_initialization(self):
        """Test that database tables are created properly"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        self.assertIn('users', tables)
        self.assertIn('products', tables)
        self.assertIn('cart', tables)
        
        # Check if sample products were inserted
        cursor.execute('SELECT COUNT(*) FROM products')
        product_count = cursor.fetchone()[0]
        self.assertEqual(product_count, 6)
        
        conn.close()

    def test_get_db(self):
        """Test database connection"""
        conn = get_db()
        self.assertIsNotNone(conn)
        self.assertEqual(conn.row_factory, sqlite3.Row)
        conn.close()

    # Index/Home Page Tests
    def test_index_page(self):
        """Test home page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'E-Commerce', response.data)

    def test_index_shows_products(self):
        """Test that products are displayed on home page"""
        response = self.client.get('/')
        self.assertIn(b'Laptop', response.data)
        self.assertIn(b'Smartphone', response.data)

    # Registration Tests
    def test_register_page_get(self):
        """Test registration page loads"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_register_success(self):
        """Test successful user registration"""
        response = self.register_user()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)

    def test_register_missing_fields(self):
        """Test registration with missing fields"""
        response = self.client.post('/register', data={
            'username': 'testuser',
            'email': '',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        }, follow_redirects=True)
        self.assertIn(b'All fields are required', response.data)

    def test_register_password_mismatch(self):
        """Test registration with mismatched passwords"""
        response = self.register_user(password='pass123', confirm_password='pass456')
        self.assertIn(b'Passwords do not match', response.data)

    def test_register_duplicate_username(self):
        """Test registration with duplicate username"""
        self.register_user()
        response = self.register_user()
        self.assertIn(b'Username or email already exists', response.data)

    def test_register_duplicate_email(self):
        """Test registration with duplicate email"""
        self.register_user(username='user1', email='test@example.com')
        response = self.register_user(username='user2', email='test@example.com')
        self.assertIn(b'Username or email already exists', response.data)

    # Login Tests
    def test_login_page_get(self):
        """Test login page loads"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_login_success(self):
        """Test successful login"""
        self.register_user()
        response = self.login_user()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back', response.data)

    def test_login_missing_fields(self):
        """Test login with missing fields"""
        response = self.client.post('/login', data={
            'username': '',
            'password': 'testpass123'
        }, follow_redirects=True)
        self.assertIn(b'Username and password are required', response.data)

    def test_login_invalid_username(self):
        """Test login with invalid username"""
        response = self.login_user(username='nonexistent')
        self.assertIn(b'Invalid username or password', response.data)

    def test_login_invalid_password(self):
        """Test login with invalid password"""
        self.register_user()
        response = self.login_user(password='wrongpassword')
        self.assertIn(b'Invalid username or password', response.data)

    # Logout Tests
    def test_logout(self):
        """Test user logout"""
        self.register_user()
        self.login_user()
        response = self.logout_user()
        self.assertIn(b'You have been logged out', response.data)

    # Cart Tests
    def test_cart_requires_login(self):
        """Test that cart page requires login"""
        response = self.client.get('/cart', follow_redirects=True)
        self.assertIn(b'Please login to access this page', response.data)

    def test_cart_page_when_logged_in(self):
        """Test cart page loads when logged in"""
        self.register_user()
        self.login_user()
        response = self.client.get('/cart')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Shopping Cart', response.data)

    def test_cart_empty_initially(self):
        """Test that cart is empty for new user"""
        self.register_user()
        self.login_user()
        response = self.client.get('/cart')
        self.assertIn(b'Your cart is empty', response.data)

    def test_add_to_cart_requires_login(self):
        """Test that adding to cart requires login"""
        response = self.client.post('/add_to_cart/1', follow_redirects=True)
        self.assertIn(b'Please login to access this page', response.data)

    def test_add_to_cart_success(self):
        """Test successfully adding product to cart"""
        self.register_user()
        self.login_user()
        response = self.client.post('/add_to_cart/1', follow_redirects=True)
        self.assertIn(b'Product added to cart', response.data)

    def test_add_to_cart_invalid_product(self):
        """Test adding non-existent product to cart"""
        self.register_user()
        self.login_user()
        response = self.client.post('/add_to_cart/999', follow_redirects=True)
        self.assertIn(b'Product not available', response.data)

    def test_add_to_cart_increases_quantity(self):
        """Test that adding same product increases quantity"""
        self.register_user()
        self.login_user()
        
        # Add product twice
        self.client.post('/add_to_cart/1', follow_redirects=True)
        self.client.post('/add_to_cart/1', follow_redirects=True)
        
        # Check cart
        response = self.client.get('/cart')
        self.assertIn(b'Laptop', response.data)

    def test_remove_from_cart(self):
        """Test removing item from cart"""
        self.register_user()
        self.login_user()
        
        # Add product to cart
        self.client.post('/add_to_cart/1', follow_redirects=True)
        
        # Get cart to find cart_id
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM cart WHERE user_id = 1')
        cart_item = cursor.fetchone()
        cart_id = cart_item[0]
        conn.close()
        
        # Remove from cart
        response = self.client.post(f'/remove_from_cart/{cart_id}', follow_redirects=True)
        self.assertIn(b'Item removed from cart', response.data)

    def test_update_cart_quantity(self):
        """Test updating cart item quantity"""
        self.register_user()
        self.login_user()
        
        # Add product to cart
        self.client.post('/add_to_cart/1', follow_redirects=True)
        
        # Get cart_id
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM cart WHERE user_id = 1')
        cart_item = cursor.fetchone()
        cart_id = cart_item[0]
        conn.close()
        
        # Update quantity
        response = self.client.post(f'/update_cart/{cart_id}', data={
            'quantity': 3
        }, follow_redirects=True)
        self.assertIn(b'Cart updated', response.data)

    def test_update_cart_invalid_quantity(self):
        """Test updating cart with invalid quantity"""
        self.register_user()
        self.login_user()
        
        # Add product to cart
        self.client.post('/add_to_cart/1', follow_redirects=True)
        
        # Get cart_id
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM cart WHERE user_id = 1')
        cart_item = cursor.fetchone()
        cart_id = cart_item[0]
        conn.close()
        
        # Try to update with invalid quantity
        response = self.client.post(f'/update_cart/{cart_id}', data={
            'quantity': 0
        }, follow_redirects=True)
        self.assertIn(b'Quantity must be at least 1', response.data)

    # Checkout Tests
    def test_checkout_requires_login(self):
        """Test that checkout requires login"""
        response = self.client.post('/checkout', follow_redirects=True)
        self.assertIn(b'Please login to access this page', response.data)

    def test_checkout_empty_cart(self):
        """Test checkout with empty cart"""
        self.register_user()
        self.login_user()
        response = self.client.post('/checkout', follow_redirects=True)
        self.assertIn(b'Your cart is empty', response.data)

    def test_checkout_success(self):
        """Test successful checkout"""
        self.register_user()
        self.login_user()
        
        # Add product to cart
        self.client.post('/add_to_cart/1', follow_redirects=True)
        
        # Checkout
        response = self.client.post('/checkout', follow_redirects=True)
        self.assertIn(b'Order placed successfully', response.data)

    def test_checkout_updates_stock(self):
        """Test that checkout updates product stock"""
        self.register_user()
        self.login_user()
        
        # Get initial stock
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT stock FROM products WHERE id = 1')
        initial_stock = cursor.fetchone()[0]
        conn.close()
        
        # Add product to cart and checkout
        self.client.post('/add_to_cart/1', follow_redirects=True)
        self.client.post('/checkout', follow_redirects=True)
        
        # Check updated stock
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT stock FROM products WHERE id = 1')
        final_stock = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(final_stock, initial_stock - 1)

    def test_checkout_clears_cart(self):
        """Test that checkout clears the cart"""
        self.register_user()
        self.login_user()
        
        # Add product to cart and checkout
        self.client.post('/add_to_cart/1', follow_redirects=True)
        self.client.post('/checkout', follow_redirects=True)
        
        # Check cart is empty
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM cart WHERE user_id = 1')
        cart_count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(cart_count, 0)

    # Session Tests
    def test_session_persistence(self):
        """Test that session persists across requests"""
        self.register_user()
        self.login_user()
        
        with self.client.session_transaction() as sess:
            self.assertIn('user_id', sess)
            self.assertIn('username', sess)
            self.assertEqual(sess['username'], 'testuser')

    def test_session_cleared_on_logout(self):
        """Test that session is cleared on logout"""
        self.register_user()
        self.login_user()
        self.logout_user()
        
        with self.client.session_transaction() as sess:
            self.assertNotIn('user_id', sess)
            self.assertNotIn('username', sess)


if __name__ == '__main__':
    unittest.main()

# Made with Bob
