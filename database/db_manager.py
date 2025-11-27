"""
Database Manager - Quản lý kết nối và thao tác database
"""
import sqlite3
import os
from typing import List, Dict, Optional, Any
from datetime import datetime
import bcrypt

from database.models import (
    User, Category, Product, Order, OrderItem, Cart, Review, ALL_MODELS
)

class DatabaseManager:
    """Quản lý database"""
    
    def __init__(self, db_path: str = "data/music_store.db"):
        self.db_path = db_path
        self.ensure_data_folder()
        self.connection = None
        self.cursor = None
    
    def ensure_data_folder(self):
        """Tạo thư mục data nếu chưa có"""
        folder = os.path.dirname(self.db_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
    
    def connect(self):
        """Kết nối database"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            # Enable foreign keys
            self.cursor.execute("PRAGMA foreign_keys = ON")
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Ngắt kết nối database"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def create_tables(self):
        """Tạo tất cả các bảng"""
        try:
            self.connect()
            for model in ALL_MODELS:
                self.cursor.execute(model.CREATE_TABLE)
            self.connection.commit()
            print("✅ All tables created successfully!")
            return True
        except sqlite3.Error as e:
            print(f"❌ Error creating tables: {e}")
            return False
        finally:
            self.disconnect()
    
    def drop_tables(self):
        """Xóa tất cả các bảng"""
        try:
            self.connect()
            for model in reversed(ALL_MODELS):
                self.cursor.execute(f"DROP TABLE IF EXISTS {model.TABLE_NAME}")
            self.connection.commit()
            print("✅ All tables dropped successfully!")
            return True
        except sqlite3.Error as e:
            print(f"❌ Error dropping tables: {e}")
            return False
        finally:
            self.disconnect()
    
    def reset_database(self):
        """Reset database - xóa và tạo lại"""
        self.drop_tables()
        self.create_tables()
    
    def execute_query(self, query: str, params: tuple = None, fetch: str = None):
        """
        Thực thi query
        fetch: 'one', 'all', None
        """
        try:
            self.connect()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            if fetch == 'one':
                result = self.cursor.fetchone()
                return dict(result) if result else None
            elif fetch == 'all':
                results = self.cursor.fetchall()
                return [dict(row) for row in results]
            else:
                self.connection.commit()
                return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Query error: {e}")
            return None
        finally:
            self.disconnect()
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, username: str, password: str, email: str,
                    full_name: str, role: str = 'customer', **kwargs) -> Optional[int]:
        """Tạo user mới"""
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        query = """
        INSERT INTO users (username, password_hash, email, full_name, phone, address, role)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            username,
            password_hash.decode('utf-8'),
            email,
            full_name,
            kwargs.get('phone', ''),
            kwargs.get('address', ''),
            role
        )
        return self.execute_query(query, params)
    
    def verify_user(self, username: str, password: str) -> Optional[Dict]:
        """Xác thực user"""
        query = "SELECT * FROM users WHERE username = ? AND is_active = 1"
        user = self.execute_query(query, (username,), fetch='one')
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return user
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Lấy user theo ID"""
        query = "SELECT * FROM users WHERE id = ?"
        return self.execute_query(query, (user_id,), fetch='one')
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Lấy user theo username"""
        query = "SELECT * FROM users WHERE username = ?"
        return self.execute_query(query, (username,), fetch='one')
    
    def get_all_users(self, role: str = None) -> List[Dict]:
        """Lấy danh sách users"""
        if role:
            query = "SELECT * FROM users WHERE role = ? ORDER BY created_at DESC"
            return self.execute_query(query, (role,), fetch='all') or []
        else:
            query = "SELECT * FROM users ORDER BY created_at DESC"
            return self.execute_query(query, fetch='all') or []
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        """Cập nhật thông tin user"""
        allowed_fields = ['email', 'full_name', 'phone', 'address', 'is_active']
        updates = []
        params = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                params.append(value)
        
        if not updates:
            return False
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        result = self.execute_query(query, tuple(params))
        return result is not None
    
    # ==================== CATEGORY OPERATIONS ====================
    
    def create_category(self, name: str, description: str = None, icon: str = None) -> Optional[int]:
        """Tạo danh mục mới"""
        query = "INSERT INTO categories (name, description, icon) VALUES (?, ?, ?)"
        return self.execute_query(query, (name, description, icon))
    
    def get_all_categories(self) -> List[Dict]:
        """Lấy tất cả danh mục"""
        query = "SELECT * FROM categories ORDER BY name"
        return self.execute_query(query, fetch='all') or []
    
    def get_category_by_id(self, category_id: int) -> Optional[Dict]:
        """Lấy danh mục theo ID"""
        query = "SELECT * FROM categories WHERE id = ?"
        return self.execute_query(query, (category_id,), fetch='one')
    
    # ==================== PRODUCT OPERATIONS ====================
    
    def create_product(self, category_id: int, name: str, brand: str,
                      price: float, stock: int, **kwargs) -> Optional[int]:
        """Tạo sản phẩm mới"""
        query = """
        INSERT INTO products (category_id, name, brand, price, stock, image, 
                            description, specifications, discount_percent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            category_id, name, brand, price, stock,
            kwargs.get('image', ''),
            kwargs.get('description', ''),
            kwargs.get('specifications', ''),
            kwargs.get('discount_percent', 0)
        )
        return self.execute_query(query, params)
    
    def get_all_products(self, category_id: int = None, is_active: bool = True) -> List[Dict]:
        """Lấy danh sách sản phẩm"""
        if category_id:
            query = """
            SELECT p.*, c.name as category_name 
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE p.category_id = ? AND p.is_active = ?
            ORDER BY p.created_at DESC
            """
            return self.execute_query(query, (category_id, int(is_active)), fetch='all') or []
        else:
            query = """
            SELECT p.*, c.name as category_name 
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE p.is_active = ?
            ORDER BY p.created_at DESC
            """
            return self.execute_query(query, (int(is_active),), fetch='all') or []
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """Lấy sản phẩm theo ID"""
        query = """
        SELECT p.*, c.name as category_name 
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.id = ?
        """
        return self.execute_query(query, (product_id,), fetch='one')
    
    def search_products(self, keyword: str) -> List[Dict]:
        """Tìm kiếm sản phẩm"""
        query = """
        SELECT p.*, c.name as category_name 
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE (p.name LIKE ? OR p.brand LIKE ? OR p.description LIKE ?)
        AND p.is_active = 1
        ORDER BY p.name
        """
        search_term = f"%{keyword}%"
        return self.execute_query(query, (search_term, search_term, search_term), fetch='all') or []
    
    def update_product(self, product_id: int, **kwargs) -> bool:
        """Cập nhật sản phẩm"""
        allowed_fields = ['name', 'brand', 'price', 'stock', 'image', 
                         'description', 'specifications', 'discount_percent', 'is_active']
        updates = []
        params = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                params.append(value)
        
        if not updates:
            return False
        
        params.append(product_id)
        query = f"UPDATE products SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        result = self.execute_query(query, tuple(params))
        return result is not None
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        """Cập nhật tồn kho"""
        query = "UPDATE products SET stock = stock + ? WHERE id = ?"
        result = self.execute_query(query, (quantity, product_id))
        return result is not None
    
    def delete_product(self, product_id: int) -> bool:
        """Xóa sản phẩm (soft delete)"""
        query = "UPDATE products SET is_active = 0 WHERE id = ?"
        result = self.execute_query(query, (product_id,))
        return result is not None
    
    # ==================== CART OPERATIONS ====================
    
    def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> bool:
        """Thêm vào giỏ hàng"""
        # Check if already in cart
        check_query = "SELECT id, quantity FROM cart WHERE user_id = ? AND product_id = ?"
        existing = self.execute_query(check_query, (user_id, product_id), fetch='one')
        
        if existing:
            # Update quantity
            query = "UPDATE cart SET quantity = quantity + ? WHERE id = ?"
            result = self.execute_query(query, (quantity, existing['id']))
        else:
            # Insert new
            query = "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)"
            result = self.execute_query(query, (user_id, product_id, quantity))
        
        return result is not None
    
    def get_cart_items(self, user_id: int) -> List[Dict]:
        """Lấy danh sách giỏ hàng"""
        query = """
        SELECT c.*, p.name, p.brand, p.price, p.stock, p.image, p.discount_percent,
               (p.price * (1 - p.discount_percent / 100) * c.quantity) as subtotal
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ? AND p.is_active = 1
        ORDER BY c.added_at DESC
        """
        return self.execute_query(query, (user_id,), fetch='all') or []
    
    def update_cart_quantity(self, cart_id: int, quantity: int) -> bool:
        """Cập nhật số lượng trong giỏ"""
        query = "UPDATE cart SET quantity = ? WHERE id = ?"
        result = self.execute_query(query, (quantity, cart_id))
        return result is not None
    
    def remove_from_cart(self, cart_id: int) -> bool:
        """Xóa khỏi giỏ hàng"""
        query = "DELETE FROM cart WHERE id = ?"
        result = self.execute_query(query, (cart_id,))
        return result is not None
    
    def clear_cart(self, user_id: int) -> bool:
        """Xóa toàn bộ giỏ hàng"""
        query = "DELETE FROM cart WHERE user_id = ?"
        result = self.execute_query(query, (user_id,))
        return result is not None
    
    # ==================== ORDER OPERATIONS ====================
    
    def create_order(self, user_id: int, items: List[Dict], 
                    shipping_address: str, phone: str, **kwargs) -> Optional[int]:
        """Tạo đơn hàng mới"""
        try:
            self.connect()
            
            # Generate order number
            order_number = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Calculate total
            total_amount = sum(item['subtotal'] for item in items)
            discount_amount = kwargs.get('discount_amount', 0)
            final_amount = total_amount - discount_amount
            
            # Insert order
            order_query = """
            INSERT INTO orders (user_id, order_number, total_amount, discount_amount,
                              final_amount, payment_method, shipping_address, phone, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            order_params = (
                user_id, order_number, total_amount, discount_amount, final_amount,
                kwargs.get('payment_method', 'cash'),
                shipping_address, phone,
                kwargs.get('note', '')
            )
            self.cursor.execute(order_query, order_params)
            order_id = self.cursor.lastrowid
            
            # Insert order items
            item_query = """
            INSERT INTO order_items (order_id, product_id, product_name, 
                                    product_price, quantity, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            for item in items:
                item_params = (
                    order_id,
                    item['product_id'],
                    item['name'],
                    item['price'],
                    item['quantity'],
                    item['subtotal']
                )
                self.cursor.execute(item_query, item_params)
                
                # Update stock
                self.cursor.execute(
                    "UPDATE products SET stock = stock - ? WHERE id = ?",
                    (item['quantity'], item['product_id'])
                )
            
            self.connection.commit()
            return order_id
            
        except sqlite3.Error as e:
            print(f"Order creation error: {e}")
            if self.connection:
                self.connection.rollback()
            return None
        finally:
            self.disconnect()
    
    def get_order_by_id(self, order_id: int) -> Optional[Dict]:
        """Lấy đơn hàng theo ID"""
        query = """
        SELECT o.*, u.full_name as customer_name, u.email as customer_email
        FROM orders o
        JOIN users u ON o.user_id = u.id
        WHERE o.id = ?
        """
        return self.execute_query(query, (order_id,), fetch='one')
    
    def get_order_items(self, order_id: int) -> List[Dict]:
        """Lấy chi tiết đơn hàng"""
        query = "SELECT * FROM order_items WHERE order_id = ?"
        return self.execute_query(query, (order_id,), fetch='all') or []
    
    def get_user_orders(self, user_id: int) -> List[Dict]:
        """Lấy danh sách đơn hàng của user"""
        query = """
        SELECT * FROM orders 
        WHERE user_id = ? 
        ORDER BY order_date DESC
        """
        return self.execute_query(query, (user_id,), fetch='all') or []
    
    def get_all_orders(self, status: str = None) -> List[Dict]:
        """Lấy tất cả đơn hàng"""
        if status:
            query = """
            SELECT o.*, u.full_name as customer_name
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE o.status = ?
            ORDER BY o.order_date DESC
            """
            return self.execute_query(query, (status,), fetch='all') or []
        else:
            query = """
            SELECT o.*, u.full_name as customer_name
            FROM orders o
            JOIN users u ON o.user_id = u.id
            ORDER BY o.order_date DESC
            """
            return self.execute_query(query, fetch='all') or []
    
    def update_order_status(self, order_id: int, status: str) -> bool:
        """Cập nhật trạng thái đơn hàng"""
        query = "UPDATE orders SET status = ? WHERE id = ?"
        if status == 'completed':
            query = "UPDATE orders SET status = ?, completed_date = CURRENT_TIMESTAMP WHERE id = ?"
        result = self.execute_query(query, (status, order_id))
        return result is not None

# Singleton instance
_db_instance = None

def get_db() -> DatabaseManager:
    """Get database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance