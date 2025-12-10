"""
Main Entry Point - Hệ thống bán nhạc cụ online
Music Store System - Main Application
"""
import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.styles.theme import Theme
from gui.login_window import LoginWindow
from gui.customer_view import CustomerView
from gui.admin_panel import AdminPanel
from database.models import Database, initialize_database
from database.db_manager import AuthManager

class MusicStoreApp:
    def __init__(self):
        self.root = None
        self.current_user = None
        self.current_user_id = None
        self.user_role = None
        self.auth_manager = AuthManager()
        
        # Initialize database
        self.init_database()
        
    def init_database(self):
        """Khởi tạo database nếu chưa có"""
        db = Database()
        if not os.path.exists(db.db_path):
            print("Initializing database...")
            initialize_database()
        else:
            print("Database already exists.")
    
    def start(self):
        """Khởi động ứng dụng"""
        self.show_login()
    
    def show_login(self):
        """Hiển thị màn hình đăng nhập"""
        if self.root:
            self.root.destroy()
        
        self.root = tk.Tk()
        self.root.title("Music Store - Đăng nhập")
        
        # Create custom login with callbacks
        LoginWindowWithCallbacks(
            self.root,
            auth_manager=self.auth_manager,
            on_login_success=self.on_login_success
        )
        
        self.root.mainloop()
    
    def on_login_success(self, user_data, role):
        """Xử lý khi đăng nhập thành công"""
        self.current_user = user_data.get('name', 'User')
        self.current_user_id = user_data.get('id')
        self.user_role = role
        
        # Đóng màn hình login
        self.root.destroy()
        
        # Mở màn hình tương ứng
        if role == "admin":
            self.show_admin_panel()
        else:
            self.show_customer_view()
    
    def show_admin_panel(self):
        """Hiển thị giao diện quản trị"""
        self.root = tk.Tk()
        AdminPanelWithCallbacks(
            self.root,
            self.current_user,
            on_logout=self.on_logout
        )
        self.root.mainloop()
    
    def show_customer_view(self):
        """Hiển thị giao diện khách hàng"""
        self.root = tk.Tk()
        CustomerViewWithCallbacks(
            self.root,
            self.current_user,
            self.current_user_id,
            on_logout=self.on_logout
        )
        self.root.mainloop()
    
    def on_logout(self):
        """Xử lý đăng xuất"""
        self.current_user = None
        self.current_user_id = None
        self.user_role = None
        self.show_login()

# Extended classes with callbacks
class LoginWindowWithCallbacks(LoginWindow):
    def __init__(self, root, auth_manager=None, on_login_success=None):
        self.auth_manager = auth_manager
        self.on_login_success_callback = on_login_success
        # Set auth_manager as instance variable before calling parent init
        # so it can be accessed in open_register
        super().__init__(root)
        # Make sure auth_manager is accessible to parent class methods
        self.root.auth_manager = auth_manager
    
    def login(self):
        """Override login method with database authentication"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        try:
            if role == "admin":
                # Admin login
                user_data = self.auth_manager.login_admin(username, password)
                if user_data:
                    messagebox.showinfo("Thành công", f"Chào mừng {user_data['name']}!")
                    if self.on_login_success_callback:
                        self.on_login_success_callback(user_data, "admin")
                else:
                    messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
            else:
                # Customer login (using email)
                user_data = self.auth_manager.login_user(username, password)
                if user_data:
                    messagebox.showinfo("Thành công", f"Chào mừng {user_data['name']}!")
                    if self.on_login_success_callback:
                        self.on_login_success_callback(user_data, "customer")
                else:
                    messagebox.showerror("Lỗi", "Email hoặc mật khẩu không đúng!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi đăng nhập: {e}")

class AdminPanelWithCallbacks(AdminPanel):
    def __init__(self, root, admin_name="Admin", on_logout=None):
        self.on_logout_callback = on_logout
        super().__init__(root, admin_name)
    
    def logout(self):
        """Override logout method"""
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc muốn đăng xuất?"):
            self.root.destroy()
            if self.on_logout_callback:
                self.on_logout_callback()

class CustomerViewWithCallbacks(CustomerView):
    def __init__(self, root, username="Customer", user_id=None, on_logout=None):
        self.on_logout_callback = on_logout
        super().__init__(root, username, user_id)
    
    def logout(self):
        """Override logout method"""
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc muốn đăng xuất?"):
            self.root.destroy()
            if self.on_logout_callback:
                self.on_logout_callback()

def main():
    """Entry point"""
    print("=" * 60)
    print("🎸 MUSIC STORE SYSTEM")
    print("Hệ thống bán nhạc cụ online")
    print("=" * 60)
    print("\nĐang khởi động ứng dụng...")
    print("\n📌 Tài khoản demo:")
    print("  ┌─ Admin:")
    print("  │  Username: admin")
    print("  │  Password: admin123")
    print("  │")
    print("  └─ Khách hàng:")
    print("     Email: nguyenvana@email.com")
    print("     Password: customer123")
    print("=" * 60)
    
    app = MusicStoreApp()
    app.start()

if __name__ == "__main__":
    main()