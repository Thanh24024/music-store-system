"""
Database Models - SQLite Schema Definition
"""
import sqlite3
from datetime import datetime
import os

class DatabaseSchema:
    """Định nghĩa schema cho SQLite database"""
    
    @staticmethod
    def get_schema():
        """Trả về SQL schema"""
        return """
        -- Admin table
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(20) NOT NULL,
            password VARCHAR(50) NOT NULL
        );
        
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            number VARCHAR(10) NOT NULL,
            password VARCHAR(50) NOT NULL,
            address VARCHAR(500) NOT NULL DEFAULT '',
            create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Products table
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            category VARCHAR(100) NOT NULL,
            price INTEGER NOT NULL,
            image VARCHAR(100) NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            describe VARCHAR(500) NOT NULL DEFAULT ''
        );
        
        -- Cart table
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            pid INTEGER NOT NULL,
            name VARCHAR(100) NOT NULL,
            price INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            image VARCHAR(100) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (pid) REFERENCES products(id) ON DELETE CASCADE
        );
        
        -- Orders table
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name VARCHAR(20) NOT NULL,
            number VARCHAR(10) NOT NULL,
            email VARCHAR(100) NOT NULL,
            method VARCHAR(50) NOT NULL,
            address VARCHAR(500) NOT NULL,
            total_products VARCHAR(1000) NOT NULL,
            total_price VARCHAR(100) NOT NULL,
            placed_on DATE NOT NULL,
            received_on DATE DEFAULT NULL,
            payment_status VARCHAR(20) NOT NULL DEFAULT 'pending',
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        
        -- Create indexes for better performance
        CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
        CREATE INDEX IF NOT EXISTS idx_cart_user ON cart(user_id);
        CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
        CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(payment_status);
        """
    
    @staticmethod
    def get_sample_data():
        """Dữ liệu mẫu để test"""
        return {
            'admin': [
                ('admin', 'admin123'),
                ('manager', 'manager123')
            ],
            'users': [
                ('Nguyễn Văn A', 'nguyenvana@email.com', '0901234567', 'customer123', 'Hà Nội'),
                ('Trần Thị B', 'tranthib@email.com', '0912345678', 'user123', 'Đà Nẵng'),
                ('Lê Văn C', 'levanc@email.com', '0923456789', 'user456', 'TP HCM')
            ],
            'products': [
                ('Yamaha F310 Acoustic Guitar', 'Guitar', 3500000, 'guitar1.jpg', 15, 'Guitar acoustic chất lượng cao cho người mới bắt đầu'),
                ('Fender Stratocaster Electric', 'Guitar', 12000000, 'guitar2.jpg', 8, 'Electric guitar chuyên nghiệp với âm thanh đỉnh cao'),
                ('Yamaha P-45 Digital Piano', 'Piano', 11000000, 'piano1.jpg', 5, 'Đàn piano điện tử 88 phím cho người học'),
                ('Roland FP-30X Digital Piano', 'Piano', 15500000, 'piano2.jpg', 3, 'Piano điện tử cao cấp với công nghệ hiện đại'),
                ('Pearl Export Drum Set', 'Drums', 18000000, 'drums1.jpg', 2, 'Bộ trống chuyên nghiệp 5 trống'),
                ('Yamaha YAS-280 Alto Saxophone', 'Wind', 25000000, 'sax1.jpg', 4, 'Saxophone alto chất lượng cao'),
                ('Ibanez SR300E Bass Guitar', 'Guitar', 8500000, 'bass1.jpg', 10, 'Bass guitar 4 dây chất lượng'),
                ('Casio CT-S300 Keyboard', 'Piano', 4200000, 'keyboard1.jpg', 12, 'Keyboard 61 phím di động'),
                ('Mapex Mars Drum Set', 'Drums', 22000000, 'drums2.jpg', 3, 'Bộ trống cao cấp với shell gỗ'),
                ('Bach TR-650 Trumpet', 'Wind', 15000000, 'trumpet1.jpg', 6, 'Trumpet chuyên nghiệp cho buổi biểu diễn')
            ]
        }

class Database:
    """Base Database class"""
    
    def __init__(self, db_path='data/music_store.db'):
        self.db_path = db_path
        self.ensure_database_exists()
    
    def ensure_database_exists(self):
        """Đảm bảo database và thư mục tồn tại"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def get_connection(self):
        """Tạo kết nối đến database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Trả về dict thay vì tuple
        return conn
    
    def execute_query(self, query, params=None, fetch=False):
        """
        Thực thi câu lệnh SQL
        
        Args:
            query: SQL query string
            params: Tham số cho query
            fetch: True để lấy kết quả, False để chỉ execute
        
        Returns:
            Kết quả query hoặc None
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
                # Convert Row objects to dictionaries
                result = [dict(row) for row in result]
                return result
            else:
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    def execute_many(self, query, params_list):
        """Thực thi nhiều câu lệnh cùng lúc"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
    
    def create_tables(self):
        """Tạo tất cả các bảng"""
        schema = DatabaseSchema.get_schema()
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.executescript(schema)
            conn.commit()
            print("✓ Tables created successfully!")
            return True
        except sqlite3.Error as e:
            print(f"✗ Error creating tables: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def insert_sample_data(self):
        """Thêm dữ liệu mẫu"""
        data = DatabaseSchema.get_sample_data()
        
        try:
            # Insert admins
            query = "INSERT INTO admin (name, password) VALUES (?, ?)"
            self.execute_many(query, data['admin'])
            print("✓ Admin data inserted")
            
            # Insert users
            query = "INSERT INTO users (name, email, number, password, address) VALUES (?, ?, ?, ?, ?)"
            self.execute_many(query, data['users'])
            print("✓ Users data inserted")
            
            # Insert products
            query = """INSERT INTO products (name, category, price, image, quantity, describe) 
                      VALUES (?, ?, ?, ?, ?, ?)"""
            self.execute_many(query, data['products'])
            print("✓ Products data inserted")
            
            return True
        except Exception as e:
            print(f"✗ Error inserting sample data: {e}")
            return False
    
    def reset_database(self):
        """Xóa và tạo lại database"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print("✓ Old database removed")
        
        self.ensure_database_exists()
        self.create_tables()
        self.insert_sample_data()
        print("✓ Database reset completed!")

def initialize_database():
    """Khởi tạo database ban đầu"""
    print("=" * 60)
    print("DATABASE INITIALIZATION")
    print("=" * 60)
    
    db = Database()
    
    # Check if database exists
    if not os.path.exists(db.db_path):
        print("\n→ Creating new database...")
        db.create_tables()
        db.insert_sample_data()
    else:
        print("\n→ Database already exists")
        choice = input("Reset database? (y/n): ")
        if choice.lower() == 'y':
            db.reset_database()
    
    print("\n✓ Database ready!")
    print("=" * 60)

if __name__ == "__main__":
    initialize_database()