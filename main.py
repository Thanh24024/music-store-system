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

class MusicStoreApp:
    def __init__(self):
        self.root = None
        self.current_user = None
        self.user_role = None
        
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
            on_login_success=self.on_login_success
        )
        
        self.root.mainloop()
    
    def on_login_success(self, username, role):
        """Xử lý khi đăng nhập thành công"""
        self.current_user = username
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
            on_logout=self.on_logout
        )
        self.root.mainloop()
    
    def on_logout(self):
        """Xử lý đăng xuất"""
        self.current_user = None
        self.user_role = None
        self.show_login()

# Extended classes with callbacks
class LoginWindowWithCallbacks(LoginWindow):
    def __init__(self, root, on_login_success=None):
        self.on_login_success_callback = on_login_success
        super().__init__(root)
    
    def login(self):
        """Override login method"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        # TODO: Kết nối database để xác thực
        # Demo authentication
        valid_users = {
            "admin": {"password": "admin123", "role": "admin", "name": "Quản trị viên"},
            "customer": {"password": "customer123", "role": "customer", "name": "Nguyễn Văn A"},
            "user1": {"password": "123456", "role": "customer", "name": "Trần Thị B"},
        }
        
        if username in valid_users:
            user_data = valid_users[username]
            if user_data["password"] == password and user_data["role"] == role:
                messagebox.showinfo("Thành công", f"Chào mừng {user_data['name']}!")
                if self.on_login_success_callback:
                    self.on_login_success_callback(user_data['name'], role)
            else:
                messagebox.showerror("Lỗi", "Mật khẩu hoặc vai trò không đúng!")
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập không tồn tại!")

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
    def __init__(self, root, username="Customer", on_logout=None):
        self.on_logout_callback = on_logout
        super().__init__(root, username)
    
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
    print("\nTài khoản demo:")
    print("  Admin: admin / admin123")
    print("  Khách hàng: customer / customer123")
    print("=" * 60)
    
    app = MusicStoreApp()
    app.start()

if __name__ == "__main__":
    main()