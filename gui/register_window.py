"""
Register Window - Màn hình đăng ký người dùng mới
"""
import tkinter as tk
from tkinter import messagebox
import sys
sys.path.append('..')
from gui.styles.theme import Theme
import re

class RegisterWindow:
    def __init__(self, root, auth_manager=None, on_register_success=None):
        self.root = root
        self.auth_manager = auth_manager
        self.on_register_success = on_register_success
        
        self.root.title("Đăng ký - Music Store")
        self.root.geometry("500x950")
        self.root.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Configure root
        self.root.configure(bg=Theme.BG_PRIMARY)
        
        # Create UI
        self.create_widgets()
        
    def center_window(self):
        """Căn giữa cửa sổ"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        # Main Container
        main_frame = tk.Frame(self.root, **Theme.get_frame_style())
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Title Section
        title_frame = tk.Frame(main_frame, **Theme.get_frame_style())
        title_frame.pack(pady=(0, 15))
        
        # Icon
        icon_label = tk.Label(
            title_frame,
            text="🎸",
            font=("Segoe UI", 40),
            **Theme.get_frame_style()
        )
        icon_label.pack()
        
        title_label = tk.Label(
            title_frame,
            text="Đăng ký tài khoản",
            **Theme.get_label_style("title")
        )
        title_label.pack(pady=(10, 5))
        
        subtitle_label = tk.Label(
            title_frame,
            text="Tạo tài khoản mới để mua sắm",
            **Theme.get_label_style("secondary")
        )
        subtitle_label.pack()
        
        # Register Form
        form_frame = tk.Frame(main_frame, **Theme.get_frame_style())
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Full Name
        self.create_form_field(form_frame, "Họ và tên *", "name")
        
        # Email
        self.create_form_field(form_frame, "Email *", "email")
        
        # Phone Number
        self.create_form_field(form_frame, "Số điện thoại *", "phone")
        
        # Password
        password_label = tk.Label(
            form_frame,
            text="Mật khẩu *",
            **Theme.get_label_style("normal")
        )
        password_label.pack(anchor=tk.W, pady=(15, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            show="●",
            **Theme.get_entry_style()
        )
        self.password_entry.pack(fill=tk.X, ipady=8)
        
        # Confirm Password
        confirm_label = tk.Label(
            form_frame,
            text="Xác nhận mật khẩu *",
            **Theme.get_label_style("normal")
        )
        confirm_label.pack(anchor=tk.W, pady=(15, 5))
        
        self.confirm_entry = tk.Entry(
            form_frame,
            show="●",
            **Theme.get_entry_style()
        )
        self.confirm_entry.pack(fill=tk.X, ipady=8)
        
        # Address
        address_label = tk.Label(
            form_frame,
            text="Địa chỉ",
            **Theme.get_label_style("normal")
        )
        address_label.pack(anchor=tk.W, pady=(15, 5))
        
        self.address_text = tk.Text(
            form_frame,
            height=1,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL),
            relief="solid",
            borderwidth=1
        )
        self.address_text.pack(fill=tk.X)
        
        # Register Button
        register_btn = tk.Button(
            form_frame,
            text="Đăng ký",
            command=self.register,
            **Theme.get_button_style("success")
        )
        register_btn.pack(fill=tk.X, pady=(25, 10), ipady=5)
        
        # Back to login
        back_frame = tk.Frame(form_frame, **Theme.get_frame_style())
        back_frame.pack(pady=(10, 0))
        
        tk.Label(
            back_frame,
            text="Đã có tài khoản?",
            **Theme.get_label_style("secondary")
        ).pack(side=tk.LEFT)
        
        back_btn = tk.Button(
            back_frame,
            text="Đăng nhập ngay",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold"),
            fg=Theme.SECONDARY,
            bg=Theme.BG_PRIMARY,
            border=0,
            cursor="hand2",
            command=self.back_to_login
        )
        back_btn.pack(side=tk.LEFT, padx=5)
    
    def create_form_field(self, parent, label_text, field_name):
        """Tạo form field"""
        label = tk.Label(
            parent,
            text=label_text,
            **Theme.get_label_style("normal")
        )
        label.pack(anchor=tk.W, pady=(15, 5))
        
        entry = tk.Entry(parent, **Theme.get_entry_style())
        entry.pack(fill=tk.X, ipady=8)
        setattr(self, f"{field_name}_entry", entry)
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        """Validate phone number (10 digits)"""
        pattern = r'^0\d{9}$'
        return re.match(pattern, phone) is not None
    
    def validate_form(self):
        """Validate form data"""
        # Check empty fields
        if not self.name_entry.get().strip():
            messagebox.showerror("Lỗi", "Vui lòng nhập họ tên!")
            return False
        
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showerror("Lỗi", "Vui lòng nhập email!")
            return False
        
        if not self.validate_email(email):
            messagebox.showerror("Lỗi", "Email không hợp lệ!")
            return False
        
        phone = self.phone_entry.get().strip()
        if not phone:
            messagebox.showerror("Lỗi", "Vui lòng nhập số điện thoại!")
            return False
        
        if not self.validate_phone(phone):
            messagebox.showerror("Lỗi", "Số điện thoại không hợp lệ! (10 số, bắt đầu bằng 0)")
            return False
        
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập mật khẩu!")
            return False
        
        if len(password) < 6:
            messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
            return False
        
        confirm = self.confirm_entry.get()
        if password != confirm:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
            return False
        
        return True
    
    def register(self):
        """Xử lý đăng ký"""
        if not self.validate_form():
            return
        
        # Check if email exists
        email = self.email_entry.get().strip()
        if self.auth_manager and self.auth_manager.check_email_exists(email):
            messagebox.showerror("Lỗi", "Email đã được sử dụng!")
            return
        
        # Register user
        try:
            user_id = self.auth_manager.register_user(
                name=self.name_entry.get().strip(),
                email=email,
                number=self.phone_entry.get().strip(),
                password=self.password_entry.get(),
                address=self.address_text.get("1.0", tk.END).strip()
            )
            
            if user_id:
                messagebox.showinfo(
                    "Thành công", 
                    "Đăng ký thành công!\nBạn có thể đăng nhập ngay."
                )
                if self.on_register_success:
                    self.on_register_success()
                self.root.destroy()
            else:
                messagebox.showerror("Lỗi", "Không thể đăng ký. Vui lòng thử lại!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi đăng ký: {e}")
    
    def back_to_login(self):
        """Quay lại màn hình đăng nhập"""
        self.root.destroy()

def main():
    """Test register window"""
    from database.db_manager import AuthManager
    
    root = tk.Tk()
    auth = AuthManager()
    
    def on_success():
        print("Registration successful!")
    
    RegisterWindow(root, auth, on_success)
    root.mainloop()

if __name__ == "__main__":
    main()
