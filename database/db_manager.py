"""
Database Manager - Quản lý các thao tác CRUD
"""
from database.models import Database
from datetime import datetime
import hashlib

class AuthManager:
    """Quản lý xác thực người dùng"""
    
    def __init__(self):
        self.db = Database()
    
    def hash_password(self, password):
        """Hash mật khẩu"""
        return hashlib.md5(password.encode()).hexdigest()
    
    def login_admin(self, username, password):
        """Đăng nhập admin"""
        query = "SELECT * FROM admin WHERE name = ? AND password = ?"
        result = self.db.execute_query(query, (username, password), fetch=True)
        return result[0] if result else None
    
    def login_user(self, email, password):
        """Đăng nhập user"""
        query = "SELECT * FROM users WHERE email = ? AND password = ?"
        result = self.db.execute_query(query, (email, password), fetch=True)
        return result[0] if result else None
    
    def register_user(self, name, email, number, password, address=''):
        """Đăng ký user mới"""
        try:
            query = """INSERT INTO users (name, email, number, password, address) 
                      VALUES (?, ?, ?, ?, ?)"""
            user_id = self.db.execute_query(query, (name, email, number, password, address))
            return user_id
        except Exception as e:
            print(f"Register error: {e}")
            return None
    
    def check_email_exists(self, email):
        """Kiểm tra email đã tồn tại"""
        query = "SELECT id FROM users WHERE email = ?"
        result = self.db.execute_query(query, (email,), fetch=True)
        return len(result) > 0

class ProductManager:
    """Quản lý sản phẩm"""
    
    def __init__(self):
        self.db = Database()
    
    def get_all_products(self):
        """Lấy tất cả sản phẩm"""
        query = "SELECT * FROM products ORDER BY id DESC"
        return self.db.execute_query(query, fetch=True)
    
    def get_product_by_id(self, product_id):
        """Lấy sản phẩm theo ID"""
        query = "SELECT * FROM products WHERE id = ?"
        result = self.db.execute_query(query, (product_id,), fetch=True)
        return result[0] if result else None
    
    def get_products_by_category(self, category):
        """Lấy sản phẩm theo danh mục"""
        query = "SELECT * FROM products WHERE category = ? ORDER BY id DESC"
        return self.db.execute_query(query, (category,), fetch=True)
    
    def search_products(self, keyword):
        """Tìm kiếm sản phẩm"""
        query = """SELECT * FROM products 
                  WHERE name LIKE ? OR category LIKE ? OR describe LIKE ?
                  ORDER BY id DESC"""
        search_term = f"%{keyword}%"
        return self.db.execute_query(query, (search_term, search_term, search_term), fetch=True)
    
    def add_product(self, name, category, price, image, quantity, describe):
        """Thêm sản phẩm mới"""
        try:
            query = """INSERT INTO products (name, category, price, image, quantity, describe) 
                      VALUES (?, ?, ?, ?, ?, ?)"""
            product_id = self.db.execute_query(
                query, 
                (name, category, price, image, quantity, describe)
            )
            return product_id
        except Exception as e:
            print(f"Add product error: {e}")
            return None
    
    def update_product(self, product_id, name, category, price, image, quantity, describe):
        """Cập nhật sản phẩm"""
        try:
            query = """UPDATE products 
                      SET name=?, category=?, price=?, image=?, quantity=?, describe=?
                      WHERE id=?"""
            self.db.execute_query(
                query, 
                (name, category, price, image, quantity, describe, product_id)
            )
            return True
        except Exception as e:
            print(f"Update product error: {e}")
            return False
    
    def delete_product(self, product_id):
        """Xóa sản phẩm"""
        try:
            query = "DELETE FROM products WHERE id = ?"
            self.db.execute_query(query, (product_id,))
            return True
        except Exception as e:
            print(f"Delete product error: {e}")
            return False
    
    def update_quantity(self, product_id, quantity):
        """Cập nhật số lượng tồn kho"""
        try:
            query = "UPDATE products SET quantity = ? WHERE id = ?"
            self.db.execute_query(query, (quantity, product_id))
            return True
        except Exception as e:
            print(f"Update quantity error: {e}")
            return False
    
    def get_categories(self):
        """Lấy danh sách categories"""
        query = "SELECT DISTINCT category FROM products ORDER BY category"
        result = self.db.execute_query(query, fetch=True)
        return [row['category'] for row in result]

class CartManager:
    """Quản lý giỏ hàng"""
    
    def __init__(self):
        self.db = Database()
    
    def add_to_cart(self, user_id, product_id, name, price, quantity, image):
        """Thêm vào giỏ hàng"""
        try:
            # Check if product already in cart
            check_query = "SELECT * FROM cart WHERE user_id = ? AND pid = ?"
            existing = self.db.execute_query(check_query, (user_id, product_id), fetch=True)
            
            if existing:
                # Update quantity
                new_quantity = existing[0]['quantity'] + quantity
                update_query = "UPDATE cart SET quantity = ? WHERE id = ?"
                self.db.execute_query(update_query, (new_quantity, existing[0]['id']))
            else:
                # Insert new
                insert_query = """INSERT INTO cart (user_id, pid, name, price, quantity, image) 
                                 VALUES (?, ?, ?, ?, ?, ?)"""
                self.db.execute_query(
                    insert_query,
                    (user_id, product_id, name, price, quantity, image)
                )
            return True
        except Exception as e:
            print(f"Add to cart error: {e}")
            return False
    
    def get_cart_items(self, user_id):
        """Lấy giỏ hàng của user"""
        query = "SELECT * FROM cart WHERE user_id = ?"
        return self.db.execute_query(query, (user_id,), fetch=True)
    
    def update_cart_quantity(self, cart_id, quantity):
        """Cập nhật số lượng trong giỏ"""
        try:
            query = "UPDATE cart SET quantity = ? WHERE id = ?"
            self.db.execute_query(query, (quantity, cart_id))
            return True
        except Exception as e:
            print(f"Update cart error: {e}")
            return False
    
    def remove_from_cart(self, cart_id):
        """Xóa khỏi giỏ hàng"""
        try:
            query = "DELETE FROM cart WHERE id = ?"
            self.db.execute_query(query, (cart_id,))
            return True
        except Exception as e:
            print(f"Remove from cart error: {e}")
            return False
    
    def clear_cart(self, user_id):
        """Xóa toàn bộ giỏ hàng"""
        try:
            query = "DELETE FROM cart WHERE user_id = ?"
            self.db.execute_query(query, (user_id,))
            return True
        except Exception as e:
            print(f"Clear cart error: {e}")
            return False

class OrderManager:
    """Quản lý đơn hàng"""
    
    def __init__(self):
        self.db = Database()
    
    def create_order(self, user_id, name, number, email, method, address, 
                    total_products, total_price, payment_status='pending'):
        """Tạo đơn hàng mới"""
        try:
            query = """INSERT INTO orders 
                      (user_id, name, number, email, method, address, 
                       total_products, total_price, placed_on, payment_status) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            order_id = self.db.execute_query(
                query,
                (user_id, name, number, email, method, address,
                 total_products, total_price, datetime.now().date(), payment_status)
            )
            return order_id
        except Exception as e:
            print(f"Create order error: {e}")
            return None
    
    def get_all_orders(self):
        """Lấy tất cả đơn hàng"""
        query = "SELECT * FROM orders ORDER BY id DESC"
        return self.db.execute_query(query, fetch=True)
    
    def get_orders_by_user(self, user_id):
        """Lấy đơn hàng của user"""
        query = "SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC"
        return self.db.execute_query(query, (user_id,), fetch=True)
    
    def get_order_by_id(self, order_id):
        """Lấy đơn hàng theo ID"""
        query = "SELECT * FROM orders WHERE id = ?"
        result = self.db.execute_query(query, (order_id,), fetch=True)
        return result[0] if result else None
    
    def update_order_status(self, order_id, status):
        """Cập nhật trạng thái đơn hàng"""
        try:
            query = "UPDATE orders SET payment_status = ? WHERE id = ?"
            self.db.execute_query(query, (status, order_id))
            return True
        except Exception as e:
            print(f"Update order status error: {e}")
            return False
    
    def update_received_date(self, order_id):
        """Cập nhật ngày nhận hàng"""
        try:
            query = "UPDATE orders SET received_on = ? WHERE id = ?"
            self.db.execute_query(query, (datetime.now().date(), order_id))
            return True
        except Exception as e:
            print(f"Update received date error: {e}")
            return False
    
    def delete_order(self, order_id):
        """Xóa đơn hàng"""
        try:
            query = "DELETE FROM orders WHERE id = ?"
            self.db.execute_query(query, (order_id,))
            return True
        except Exception as e:
            print(f"Delete order error: {e}")
            return False
    
    def get_orders_by_status(self, status):
        """Lấy đơn hàng theo trạng thái"""
        query = "SELECT * FROM orders WHERE payment_status = ? ORDER BY id DESC"
        return self.db.execute_query(query, (status,), fetch=True)

class UserManager:
    """Quản lý người dùng"""
    
    def __init__(self):
        self.db = Database()
    
    def get_all_users(self):
        """Lấy tất cả users"""
        query = "SELECT * FROM users ORDER BY id DESC"
        return self.db.execute_query(query, fetch=True)
    
    def get_user_by_id(self, user_id):
        """Lấy user theo ID"""
        query = "SELECT * FROM users WHERE id = ?"
        result = self.db.execute_query(query, (user_id,), fetch=True)
        return result[0] if result else None
    
    def update_user(self, user_id, name, email, number, address):
        """Cập nhật thông tin user"""
        try:
            query = """UPDATE users 
                      SET name=?, email=?, number=?, address=?
                      WHERE id=?"""
            self.db.execute_query(query, (name, email, number, address, user_id))
            return True
        except Exception as e:
            print(f"Update user error: {e}")
            return False
    
    def delete_user(self, user_id):
        """Xóa user"""
        try:
            query = "DELETE FROM users WHERE id = ?"
            self.db.execute_query(query, (user_id,))
            return True
        except Exception as e:
            print(f"Delete user error: {e}")
            return False

# Test functions
if __name__ == "__main__":
    print("Testing Database Managers...")
    
    # Test ProductManager
    pm = ProductManager()
    print("\n=== PRODUCTS ===")
    products = pm.get_all_products()
    print(f"Total products: {len(products)}")
    for p in products[:3]:
        print(f"- {p['name']}: {p['price']:,} VND")
    
    # Test categories
    categories = pm.get_categories()
    print(f"\nCategories: {categories}")
    
    # Test AuthManager
    am = AuthManager()
    print("\n=== AUTHENTICATION ===")
    admin = am.login_admin('admin', 'admin123')
    print(f"Admin login: {admin['name'] if admin else 'Failed'}")
    
    # Test OrderManager
    om = OrderManager()
    print("\n=== ORDERS ===")
    orders = om.get_all_orders()
    print(f"Total orders: {len(orders)}")