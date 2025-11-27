"""
Database Models - Định nghĩa cấu trúc bảng
"""
from datetime import datetime
from typing import Optional, List, Dict
import sqlite3

class BaseModel:
    """Base model cho tất cả các models"""
    
    @staticmethod
    def dict_factory(cursor, row):
        """Convert tuple to dict"""
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

class User:
    """Model User - Người dùng"""
    
    TABLE_NAME = "users"
    
    CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        phone TEXT,
        address TEXT,
        role TEXT NOT NULL CHECK(role IN ('admin', 'customer')),
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    def __init__(self, id=None, username=None, password_hash=None, email=None,
                 full_name=None, phone=None, address=None, role='customer',
                 is_active=1, created_at=None, updated_at=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.full_name = full_name
        self.phone = phone
        self.address = address
        self.role = role
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }

class Category:
    """Model Category - Danh mục sản phẩm"""
    
    TABLE_NAME = "categories"
    
    CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        icon TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    def __init__(self, id=None, name=None, description=None, icon=None, created_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'created_at': str(self.created_at)
        }

class Product:
    """Model Product - Sản phẩm"""
    
    TABLE_NAME = "products"
    
    CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        brand TEXT NOT NULL,
        price REAL NOT NULL CHECK(price >= 0),
        stock INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0),
        image TEXT,
        description TEXT,
        specifications TEXT,
        discount_percent REAL DEFAULT 0 CHECK(discount_percent >= 0 AND discount_percent <= 100),
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
    )
    """
    
    def __init__(self, id=None, category_id=None, name=None, brand=None,
                 price=0, stock=0, image=None, description=None,
                 specifications=None, discount_percent=0, is_active=1,
                 created_at=None, updated_at=None):
        self.id = id
        self.category_id = category_id
        self.name = name
        self.brand = brand
        self.price = price
        self.stock = stock
        self.image = image
        self.description = description
        self.specifications = specifications
        self.discount_percent = discount_percent
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def get_final_price(self):
        """Tính giá sau khi giảm"""
        return self.price * (1 - self.discount_percent / 100)
    
    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'name': self.name,
            'brand': self.brand,
            'price': self.price,
            'stock': self.stock,
            'image': self.image,
            'description': self.description,
            'specifications': self.specifications,
            'discount_percent': self.discount_percent,
            'final_price': self.get_final_price(),
            'is_active': self.is_active,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }

class Order:
    """Model Order - Đơn hàng"""
    
    TABLE_NAME = "orders"
    
    CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        order_number TEXT UNIQUE NOT NULL,
        total_amount REAL NOT NULL CHECK(total_amount >= 0),
        discount_amount REAL DEFAULT 0,
        final_amount REAL NOT NULL CHECK(final_amount >= 0),
        status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'processing', 'shipping', 'completed', 'cancelled')),
        payment_method TEXT CHECK(payment_method IN ('cash', 'card', 'transfer', 'e-wallet')),
        shipping_address TEXT NOT NULL,
        phone TEXT NOT NULL,
        note TEXT,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_date TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """
    
    def __init__(self, id=None, user_id=None, order_number=None,
                 total_amount=0, discount_amount=0, final_amount=0,
                 status='pending', payment_method=None, shipping_address=None,
                 phone=None, note=None, order_date=None, completed_date=None):
        self.id = id
        self.user_id = user_id
        self.order_number = order_number
        self.total_amount = total_amount
        self.discount_amount = discount_amount
        self.final_amount = final_amount
        self.status = status
        self.payment_method = payment_method
        self.shipping_address = shipping_address
        self.phone = phone
        self.note = note
        self.order_date = order_date or datetime.now()
        self.completed_date = completed_date
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'order_number': self.order_number,
            'total_amount': self.total_amount,
            'discount_amount': self.discount_amount,
            'final_amount': self.final_amount,
            'status': self.status,
            'payment_method': self.payment_method,
            'shipping_address': self.shipping_address,
            'phone': self.phone,
            'note': self.note,
            'order_date': str(self.order_date),
            'completed_date': str(self.completed_date) if self.completed_date else None
        }

class OrderItem:
    """Model OrderItem - Chi tiết đơn hàng"""
    
    TABLE_NAME = "order_items"
    
    CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        product_price REAL NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        subtotal REAL NOT NULL CHECK(subtotal >= 0),
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    """
    
    def __init__(self, id=None, order_id=None, product_id=None,
                 product_name=None, product_price=0, quantity=1, subtotal=0):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.product_name = product_name
        self.product_price = product_price
        self.quantity = quantity
        self.subtotal = subtotal
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_price': self.product_price,
            'quantity': self.quantity,
            'subtotal': self.subtotal
        }

class Cart:
    """Model Cart - Giỏ hàng"""
    
    TABLE_NAME = "cart"
    
    CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0),
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
        UNIQUE(user_id, product_id)
    )
    """
    
    def __init__(self, id=None, user_id=None, product_id=None,
                 quantity=1, added_at=None):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.added_at = added_at or datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'added_at': str(self.added_at)
        }

class Review:
    """Model Review - Đánh giá sản phẩm"""
    
    TABLE_NAME = "reviews"
    
    CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """
    
    def __init__(self, id=None, product_id=None, user_id=None,
                 rating=5, comment=None, created_at=None):
        self.id = id
        self.product_id = product_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': str(self.created_at)
        }

# Danh sách tất cả các models
ALL_MODELS = [
    User,
    Category,
    Product,
    Order,
    OrderItem,
    Cart,
    Review
]