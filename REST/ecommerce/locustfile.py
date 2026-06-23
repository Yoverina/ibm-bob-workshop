"""
Load Testing Script for E-Commerce Application
Uses Locust for performance and load testing
"""

from locust import HttpUser, task, between, SequentialTaskSet
import random
import string

class UserBehavior(SequentialTaskSet):
    """Simulates realistic user behavior on the e-commerce site"""
    
    def on_start(self):
        """Called when a simulated user starts"""
        # Generate random user credentials
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        self.username = f"loadtest_user_{random_suffix}"
        self.email = f"{self.username}@test.com"
        self.password = "TestPassword123!"
        
        # Register the user
        self.register()
        # Login the user
        self.login()
    
    def register(self):
        """Register a new user"""
        response = self.client.post("/register", data={
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "confirm_password": self.password
        }, name="Register User")
    
    def login(self):
        """Login the user"""
        response = self.client.post("/login", data={
            "username": self.username,
            "password": self.password
        }, name="Login User")
    
    @task(1)
    def view_homepage(self):
        """View the homepage"""
        self.client.get("/", name="View Homepage")
    
    @task(3)
    def view_products(self):
        """View products on homepage (most common action)"""
        self.client.get("/", name="View Products")
    
    @task(2)
    def add_to_cart(self):
        """Add random product to cart"""
        # Product IDs typically range from 1-6 based on default products
        product_id = random.randint(1, 6)
        response = self.client.post("/add_to_cart", data={
            "product_id": product_id
        }, name="Add to Cart")
    
    @task(2)
    def view_cart(self):
        """View shopping cart"""
        self.client.get("/cart", name="View Cart")
    
    @task(1)
    def update_cart(self):
        """Update cart item quantity"""
        # Simulate updating a cart item
        product_id = random.randint(1, 6)
        quantity = random.randint(1, 3)
        self.client.post("/update_cart", data={
            "product_id": product_id,
            "quantity": quantity
        }, name="Update Cart")
    
    @task(1)
    def checkout(self):
        """Perform checkout"""
        response = self.client.post("/checkout", name="Checkout")
    
    def on_stop(self):
        """Called when a simulated user stops"""
        # Logout the user
        self.client.get("/logout", name="Logout User")


class ECommerceUser(HttpUser):
    """Simulated user for load testing"""
    tasks = [UserBehavior]
    
    # Wait between 1 and 5 seconds between tasks (simulating real user behavior)
    wait_time = between(1, 5)
    
    # Set the host (will be overridden by command line)
    host = "http://127.0.0.1:5000"


class QuickTestUser(HttpUser):
    """Quick test user for rapid testing"""
    wait_time = between(0.5, 2)
    host = "http://127.0.0.1:5000"
    
    @task(5)
    def view_homepage(self):
        self.client.get("/", name="Homepage")
    
    @task(3)
    def view_login(self):
        self.client.get("/login", name="Login Page")
    
    @task(2)
    def view_register(self):
        self.client.get("/register", name="Register Page")
    
    @task(1)
    def view_cart(self):
        self.client.get("/cart", name="Cart Page")


class StressTestUser(HttpUser):
    """Stress test user with minimal wait time"""
    tasks = [UserBehavior]
    wait_time = between(0.1, 0.5)
    host = "http://127.0.0.1:5000"

# Made with Bob
