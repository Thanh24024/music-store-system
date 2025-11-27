"""
Register Window - Đăng ký tài khoản
"""
import tkinter as tk
from tkinter import messagebox
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.styles.theme import Theme
from database.db_manager import get_db

class RegisterWindow:
    def __init__(self, root, on_register_success=None):
        self.root = root
        self.root.title("Đăng ký - Music Store")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        
        self.on_register_success = on_register_success
        self.db = get_db()
        
        self.center_window()
        self.root.configure(bg=Theme.BG_PRIMARY)
        self.create_widgets()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        main_frame = tk.Frame(self.root, **Theme.get_frame_style())
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Đăng ký tài khoản",
            **Theme.get_label_style("title")
        )
        title_label.pack(pady=(0, 30))
        
        # Form
        form_frame = tk.Frame(main_frame, **Theme.get_frame_style())
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Full Name
        tk.Label(form_frame, text="Họ và tên *", **Theme.get_label_style("normal")).pack(anchor=tk.W, pady=(10, 5))
        self.fullname_entry = tk.Entry(form_frame, **Theme.get_entry_style())
        self.fullname_entry.pack(fill=tk.X, ipady=8)
        
        # Username
        tk.Label(form_frame, text="Tên đăng nhập *", **Theme.get_label_style("normal")).pack(anchor=tk.W, pady=(15, 5))
        self.username_entry = tk.Entry(form_frame, **Theme.get_entry_style())
        self.username_entry.pack(fill=tk.X, ipady=8)
        
        # Email
        tk.Label(form_frame, text="Email *", **Theme.get_label_style("normal")).pack(anchor=tk.W, pady=(15, 5))
        self.email_entry = tk.Entry(form_frame, **Theme.get_entry_style())
        self.email_entry.pack(fill=tk.X, ipady=8)
        
        # Phone
        tk.Label(form_frame, text="Số điện thoại", **Theme.get_label_style("normal")).pack(anchor=tk.W, pady=(15, 5))
        self.phone_entry = tk.Entry(form_frame, **Theme.get_entry_style())
        self.phone_entry.pack(fill=tk.X, ipady=8)
        
        # Address
        tk.Label(form_frame, text="Địa chỉ", **Theme.get_label_style("normal")).pack(anchor=tk.W, pady=(15, 5))
        self.address_entry = tk.Entry(form_frame, **Theme.get_entry_style())
        self.address_entry.pack(fill=tk.X, ipady=8)
        
        # Password
        tk.Label(form_frame, text="Mật khẩu *", **Theme.get_label_style("normal")).pack(anchor=tk.W, pady=(15, 5))
        self.password_entry = tk.Entry(form_frame, show="●", **Theme.get_entry_style())
        self.password_entry.pack(fill=tk.X, ipady=8)
        
        # Confirm Password
        tk.Label(form_frame, text="Xác nhận mật khẩu *", **Theme.get_label_style("normal")).pack(anchor=tk.W, pady=(15, 5))
        self.confirm_password_entry = tk.Entry(form_frame, show="●", **Theme.get_entry_style())
        self.confirm_password_entry.pack(fill=tk.X, ipady=8)
        
        # Terms & Conditions
        terms_frame = tk.Frame(form_frame, **Theme.get_frame_style())
        terms_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.terms_var = tk.BooleanVar()
        terms_check = tk.Checkbutton(
            terms_frame,
            text="Tôi đồng ý với Điều khoản sử dụng",
            variable=self.terms_var,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            bg=Theme.BG_PRIMARY,
            activebackground=Theme.BG_PRIMARY,
            cursor="hand2"
        )
        terms_check.pack(side=tk.LEFT)
        
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
        
        # Focus
        self.fullname_entry.focus()
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        """Validate phone number"""
        if not phone:
            return True  # Optional field
        pattern = r'^0\d{9,10}$'
        return re.match(pattern, phone) is not None
    
    def register(self):
        """Xử lý đăng ký"""
        # Get values
        full_name = self.fullname_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validate
        if not all([full_name, username, email, password, confirm_password]):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ các trường bắt buộc (*)!")
            return
        
        if len(username) < 4:
            messagebox.showerror("Lỗi", "Tên đăng nhập phải có ít nhất 4 ký tự!")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Lỗi", "Email không hợp lệ!")
            return
        
        if phone and not self.validate_phone(phone):
            messagebox.showerror("Lỗi", "Số điện thoại không hợp lệ!\nĐịnh dạng: 0xxxxxxxxx")
            return
        
        if len(password) < 6:
            messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
            return
        
        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
            return
        
        if not self.terms_var.get():
            messagebox.showerror("Lỗi", "Bạn phải đồng ý với Điều khoản sử dụng!")
            return
        
        # Check if username exists
        existing_user = self.db.get_user_by_username(username)
        if existing_user:
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!")
            return
        
        # Create user
        try:
            user_id = self.db.create_user(
                username=username,
                password=password,
                email=email,
                full_name=full_name,
                phone=phone,
                address=address,
                role='customer'
            )
            
            if user_id:
                messagebox.showinfo("Thành công", 
                    f"Đăng ký thành công!\n\nChào mừng {full_name} đến với Music Store!")
                
                if self.on_register_success:
                    user = self.db.get_user_by_id(user_id)
                    self.on_register_success(user)
                
                self.root.destroy()
            else:
                messagebox.showerror("Lỗi", "Không thể tạo tài khoản. Vui lòng thử lại!")
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
    
    def back_to_login(self):
        """Quay lại màn hình đăng nhập"""
        self.root.destroy()

def main():
    root = tk.Tk()
    app = RegisterWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()