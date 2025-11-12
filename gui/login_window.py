"""
Màn hình đăng nhập - Login Window
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
sys.path.append('..')
from gui.styles.theme import Theme

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng nhập - Music Store")
        self.root.geometry("450x600")
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
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Logo/Title Section
        title_frame = tk.Frame(main_frame, **Theme.get_frame_style())
        title_frame.pack(pady=(0, 30))
        
        # Icon (simulate with text)
        icon_label = tk.Label(
            title_frame,
            text="🎸",
            font=("Segoe UI", 60),
            **Theme.get_frame_style()
        )
        icon_label.pack()
        
        title_label = tk.Label(
            title_frame,
            text="Music Store",
            **Theme.get_label_style("title")
        )
        title_label.pack(pady=(10, 5))
        
        subtitle_label = tk.Label(
            title_frame,
            text="Chào mừng bạn trở lại!",
            **Theme.get_label_style("secondary")
        )
        subtitle_label.pack()
        
        # Login Form
        form_frame = tk.Frame(main_frame, **Theme.get_frame_style())
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Username
        username_label = tk.Label(
            form_frame,
            text="Tên đăng nhập",
            **Theme.get_label_style("normal")
        )
        username_label.pack(anchor=tk.W, pady=(20, 5))
        
        self.username_entry = tk.Entry(
            form_frame,
            **Theme.get_entry_style()
        )
        self.username_entry.pack(fill=tk.X, ipady=8)
        self.username_entry.insert(0, "")
        
        # Password
        password_label = tk.Label(
            form_frame,
            text="Mật khẩu",
            **Theme.get_label_style("normal")
        )
        password_label.pack(anchor=tk.W, pady=(20, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            show="●",
            **Theme.get_entry_style()
        )
        self.password_entry.pack(fill=tk.X, ipady=8)
        
        # Remember Me & Forgot Password
        options_frame = tk.Frame(form_frame, **Theme.get_frame_style())
        options_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.remember_var = tk.BooleanVar()
        remember_check = tk.Checkbutton(
            options_frame,
            text="Ghi nhớ đăng nhập",
            variable=self.remember_var,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            bg=Theme.BG_PRIMARY,
            activebackground=Theme.BG_PRIMARY,
            cursor="hand2"
        )
        remember_check.pack(side=tk.LEFT)
        
        forgot_btn = tk.Button(
            options_frame,
            text="Quên mật khẩu?",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            fg=Theme.SECONDARY,
            bg=Theme.BG_PRIMARY,
            border=0,
            cursor="hand2",
            command=self.forgot_password
        )
        forgot_btn.pack(side=tk.RIGHT)
        
        # Login Button
        login_btn = tk.Button(
            form_frame,
            text="Đăng nhập",
            command=self.login,
            **Theme.get_button_style("primary")
        )
        login_btn.pack(fill=tk.X, pady=(30, 10), ipady=5)
        
        # Divider
        divider_frame = tk.Frame(form_frame, **Theme.get_frame_style())
        divider_frame.pack(fill=tk.X, pady=20)
        
        tk.Frame(divider_frame, bg=Theme.BORDER, height=1).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(
            divider_frame,
            text="HOẶC",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_PRIMARY
        ).pack(side=tk.LEFT, padx=10)
        tk.Frame(divider_frame, bg=Theme.BORDER, height=1).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Register Button
        register_frame = tk.Frame(form_frame, **Theme.get_frame_style())
        register_frame.pack(pady=(10, 0))
        
        tk.Label(
            register_frame,
            text="Chưa có tài khoản?",
            **Theme.get_label_style("secondary")
        ).pack(side=tk.LEFT)
        
        register_btn = tk.Button(
            register_frame,
            text="Đăng ký ngay",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold"),
            fg=Theme.SECONDARY,
            bg=Theme.BG_PRIMARY,
            border=0,
            cursor="hand2",
            command=self.open_register
        )
        register_btn.pack(side=tk.LEFT, padx=5)
        
        # Role Selection (Admin/Customer)
        role_frame = tk.Frame(form_frame, **Theme.get_frame_style())
        role_frame.pack(pady=(20, 0))
        
        tk.Label(
            role_frame,
            text="Vai trò:",
            **Theme.get_label_style("normal")
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.role_var = tk.StringVar(value="customer")
        
        customer_radio = tk.Radiobutton(
            role_frame,
            text="Khách hàng",
            variable=self.role_var,
            value="customer",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL),
            bg=Theme.BG_PRIMARY,
            activebackground=Theme.BG_PRIMARY,
            cursor="hand2"
        )
        customer_radio.pack(side=tk.LEFT, padx=5)
        
        admin_radio = tk.Radiobutton(
            role_frame,
            text="Quản trị",
            variable=self.role_var,
            value="admin",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL),
            bg=Theme.BG_PRIMARY,
            activebackground=Theme.BG_PRIMARY,
            cursor="hand2"
        )
        admin_radio.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
    def login(self):
        """Xử lý đăng nhập"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        # TODO: Kết nối với database để xác thực
        # Tạm thời dùng dữ liệu demo
        if username == "admin" and password == "admin123" and role == "admin":
            messagebox.showinfo("Thành công", "Đăng nhập quản trị thành công!")
            self.open_admin_panel()
        elif username == "customer" and password == "customer123" and role == "customer":
            messagebox.showinfo("Thành công", "Đăng nhập khách hàng thành công!")
            self.open_customer_view()
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
    
    def forgot_password(self):
        """Xử lý quên mật khẩu"""
        messagebox.showinfo("Quên mật khẩu", "Chức năng đang được phát triển!")
    
    def open_register(self):
        """Mở màn hình đăng ký"""
        messagebox.showinfo("Đăng ký", "Màn hình đăng ký sẽ được mở!")
        # TODO: Implement register window
    
    def open_admin_panel(self):
        """Mở giao diện quản trị"""
        self.root.destroy()
        # TODO: Import and open admin panel
        print("Opening Admin Panel...")
    
    def open_customer_view(self):
        """Mở giao diện khách hàng"""
        self.root.destroy()
        # TODO: Import and open customer view
        print("Opening Customer View...")

def main():
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()