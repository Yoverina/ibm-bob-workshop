from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database configuration
DATABASE = 'ecommerce.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create cart table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Insert sample products if table is empty
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ('Laptop', 'High-performance laptop for work and gaming', 15000000, 10, 'https://via.placeholder.com/300x200?text=Laptop'),
            ('Smartphone', 'Latest smartphone with advanced features', 8000000, 15, 'https://via.placeholder.com/300x200?text=Smartphone'),
            ('Headphones', 'Wireless noise-canceling headphones', 2000000, 20, 'https://via.placeholder.com/300x200?text=Headphones'),
            ('Smartwatch', 'Fitness tracking smartwatch', 3000000, 12, 'https://via.placeholder.com/300x200?text=Smartwatch'),
            ('Tablet', 'Portable tablet for entertainment', 5000000, 8, 'https://via.placeholder.com/300x200?text=Tablet'),
            ('Camera', 'Professional DSLR camera', 12000000, 5, 'https://via.placeholder.com/300x200?text=Camera'),
        ]
        cursor.executemany(
            'INSERT INTO products (name, description, price, stock, image_url) VALUES (?, ?, ?, ?, ?)',
            sample_products
        )
    
    conn.commit()
    conn.close()

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Home page with product listing"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE stock > 0')
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Insert user into database
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                (username, email, hashed_password)
            )
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists', 'danger')
            return redirect(url_for('register'))
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required', 'danger')
            return redirect(url_for('login'))
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/cart')
@login_required
def cart():
    """View shopping cart"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, c.quantity, c.id as cart_id
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    ''', (session['user_id'],))
    cart_items = cursor.fetchall()
    conn.close()
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Add product to cart"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if product exists and has stock
    cursor.execute('SELECT * FROM products WHERE id = ? AND stock > 0', (product_id,))
    product = cursor.fetchone()
    
    if not product:
        flash('Product not available', 'danger')
        return redirect(url_for('index'))
    
    # Check if item already in cart
    cursor.execute(
        'SELECT * FROM cart WHERE user_id = ? AND product_id = ?',
        (session['user_id'], product_id)
    )
    cart_item = cursor.fetchone()
    
    if cart_item:
        # Update quantity
        cursor.execute(
            'UPDATE cart SET quantity = quantity + 1 WHERE id = ?',
            (cart_item['id'],)
        )
    else:
        # Add new item
        cursor.execute(
            'INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, 1)',
            (session['user_id'], product_id)
        )
    
    conn.commit()
    conn.close()
    flash('Product added to cart', 'success')
    return redirect(url_for('index'))

@app.route('/remove_from_cart/<int:cart_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_id):
    """Remove item from cart"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cart WHERE id = ? AND user_id = ?', (cart_id, session['user_id']))
    conn.commit()
    conn.close()
    flash('Item removed from cart', 'info')
    return redirect(url_for('cart'))

@app.route('/update_cart/<int:cart_id>', methods=['POST'])
@login_required
def update_cart(cart_id):
    """Update cart item quantity"""
    quantity = int(request.form.get('quantity', 1))
    
    if quantity < 1:
        flash('Quantity must be at least 1', 'danger')
        return redirect(url_for('cart'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE cart SET quantity = ? WHERE id = ? AND user_id = ?',
        (quantity, cart_id, session['user_id'])
    )
    conn.commit()
    conn.close()
    flash('Cart updated', 'success')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    """Process checkout"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get cart items
    cursor.execute('''
        SELECT p.*, c.quantity
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    ''', (session['user_id'],))
    cart_items = cursor.fetchall()
    
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('cart'))
    
    # Update stock and clear cart
    for item in cart_items:
        cursor.execute(
            'UPDATE products SET stock = stock - ? WHERE id = ?',
            (item['quantity'], item['id'])
        )
    
    cursor.execute('DELETE FROM cart WHERE user_id = ?', (session['user_id'],))
    conn.commit()
    conn.close()
    
    flash('Order placed successfully! Thank you for your purchase.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

# Made with Bob
