"""
Customer View - Giao diện khách hàng
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
sys.path.append('..')
from gui.styles.theme import Theme
from gui.components.product_card import ProductCard
from database.db_manager import ProductManager, CartManager

class CustomerView:
    def __init__(self, root, username="Customer", user_id=None):
        self.root = root
        self.root.title("Music Store - Khách hàng")
        self.root.geometry("1200x700")
        self.root.state('zoomed')  # Maximize window
        
        self.username = username
        self.user_id = user_id or 1  # Default user ID for demo
        self.cart_items = []
        self.current_category = "Tất cả"
        self.search_query = ""
        
        # Database managers
        self.product_manager = ProductManager()
        self.cart_manager = CartManager()
        
        # Load products from database
        self.products = []
        self.filtered_products = []
        self.load_products_from_db()
        
        self.root.configure(bg=Theme.BG_SECONDARY)
        self.create_widgets()
        self.load_products()
    
    def load_products_from_db(self):
        """Load products from database"""
        try:
            self.products = self.product_manager.get_all_products()
            self.filtered_products = self.products.copy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể load sản phẩm: {e}")
            self.products = []
            self.filtered_products = []
    
    def get_sample_products(self):
        """Dữ liệu sản phẩm mẫu"""
        return [
            {'id': 1, 'name': 'Yamaha F310 Acoustic Guitar', 'brand': 'Yamaha', 'price': 3500000, 'stock': 15, 'category': 'Guitar'},
            {'id': 2, 'name': 'Fender Stratocaster Electric', 'brand': 'Fender', 'price': 12000000, 'stock': 8, 'category': 'Guitar'},
            {'id': 3, 'name': 'Yamaha P-45 Digital Piano', 'brand': 'Yamaha', 'price': 11000000, 'stock': 5, 'category': 'Piano'},
            {'id': 4, 'name': 'Roland FP-30X Digital Piano', 'brand': 'Roland', 'price': 15500000, 'stock': 3, 'category': 'Piano'},
            {'id': 5, 'name': 'Pearl Export Drum Set', 'brand': 'Pearl', 'price': 18000000, 'stock': 2, 'category': 'Drums'},
            {'id': 6, 'name': 'Yamaha Alto Saxophone', 'brand': 'Yamaha', 'price': 25000000, 'stock': 4, 'category': 'Wind'},
            {'id': 7, 'name': 'Ibanez Bass Guitar', 'brand': 'Ibanez', 'price': 8500000, 'stock': 10, 'category': 'Guitar'},
            {'id': 8, 'name': 'Casio CT-S300 Keyboard', 'brand': 'Casio', 'price': 4200000, 'stock': 12, 'category': 'Piano'},
        ]
    
    def create_widgets(self):
        # Header
        self.create_header()
        
        # Main Content Area
        content_frame = tk.Frame(self.root, bg=Theme.BG_SECONDARY)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left Sidebar - Categories
        self.create_sidebar(content_frame)
        
        # Right Content - Products
        self.create_content_area(content_frame)
    
    def create_header(self):
        """Tạo header"""
        header = tk.Frame(self.root, bg=Theme.PRIMARY, height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Logo
        logo_label = tk.Label(
            header,
            text="🎸 Music Store",
            font=(Theme.FONT_FAMILY, 20, "bold"),
            fg=Theme.TEXT_LIGHT,
            bg=Theme.PRIMARY
        )
        logo_label.pack(side=tk.LEFT, padx=30)
        
        # Search Bar
        search_frame = tk.Frame(header, bg=Theme.PRIMARY)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_products())
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=(Theme.FONT_FAMILY, 12),
            relief="flat",
            bg=Theme.BG_PRIMARY
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        
        search_btn = tk.Button(
            search_frame,
            text="🔍 Tìm kiếm",
            font=(Theme.FONT_FAMILY, 11),
            bg=Theme.SECONDARY,
            fg=Theme.TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            padx=20,
            command=self.filter_products
        )
        search_btn.pack(side=tk.LEFT)
        
        # Cart Button
        self.cart_btn = tk.Button(
            header,
            text=f"🛒 Giỏ hàng (0)",
            font=(Theme.FONT_FAMILY, 12, "bold"),
            bg=Theme.SUCCESS,
            fg=Theme.TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            padx=20,
            command=self.show_cart
        )
        self.cart_btn.pack(side=tk.RIGHT, padx=10)
        
        # User Menu
        user_frame = tk.Frame(header, bg=Theme.PRIMARY)
        user_frame.pack(side=tk.RIGHT, padx=20)
        
        user_label = tk.Label(
            user_frame,
            text=f"👤 {self.username}",
            font=(Theme.FONT_FAMILY, 11),
            fg=Theme.TEXT_LIGHT,
            bg=Theme.PRIMARY
        )
        user_label.pack(side=tk.LEFT, padx=(0, 10))
        
        logout_btn = tk.Button(
            user_frame,
            text="Đăng xuất",
            font=(Theme.FONT_FAMILY, 10),
            bg=Theme.DANGER,
            fg=Theme.TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            padx=15,
            command=self.logout
        )
        logout_btn.pack(side=tk.LEFT)
    
    def create_sidebar(self, parent):
        """Tạo sidebar danh mục"""
        sidebar = tk.Frame(parent, bg=Theme.BG_PRIMARY, width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 5), pady=10)
        sidebar.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            sidebar,
            text="Danh mục",
            font=(Theme.FONT_FAMILY, 16, "bold"),
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_PRIMARY
        )
        title_label.pack(pady=20, padx=15, anchor=tk.W)
        
        # Get categories from database
        try:
            db_categories = self.product_manager.get_categories()
            categories = ["Tất cả"] + db_categories
        except:
            categories = ["Tất cả", "Guitar", "Piano", "Drums", "Wind", "Accessories"]
        
        for category in categories:
            btn = tk.Button(
                sidebar,
                text=category,
                font=(Theme.FONT_FAMILY, 11),
                bg=Theme.BG_PRIMARY,
                fg=Theme.TEXT_PRIMARY,
                relief="flat",
                cursor="hand2",
                anchor=tk.W,
                padx=15,
                pady=10,
                command=lambda c=category: self.select_category(c)
            )
            btn.pack(fill=tk.X)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=Theme.HOVER))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=Theme.BG_PRIMARY))
    
    def create_content_area(self, parent):
        """Tạo vùng hiển thị sản phẩm"""
        content = tk.Frame(parent, bg=Theme.BG_SECONDARY)
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=10)
        
        # Title bar
        title_frame = tk.Frame(content, bg=Theme.BG_PRIMARY, height=60)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        self.category_label = tk.Label(
            title_frame,
            text="Tất cả sản phẩm",
            font=(Theme.FONT_FAMILY, 18, "bold"),
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_PRIMARY
        )
        self.category_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        self.result_label = tk.Label(
            title_frame,
            text="",
            font=(Theme.FONT_FAMILY, 11),
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_PRIMARY
        )
        self.result_label.pack(side=tk.LEFT, pady=15)
        
        # Sort options
        sort_frame = tk.Frame(title_frame, bg=Theme.BG_PRIMARY)
        sort_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        tk.Label(
            sort_frame,
            text="Sắp xếp:",
            font=(Theme.FONT_FAMILY, 11),
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_PRIMARY
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.sort_var = tk.StringVar(value="default")
        sort_combo = ttk.Combobox(
            sort_frame,
            textvariable=self.sort_var,
            values=["Mặc định", "Giá tăng dần", "Giá giảm dần", "Tên A-Z"],
            state="readonly",
            width=15,
            font=(Theme.FONT_FAMILY, 10)
        )
        sort_combo.pack(side=tk.LEFT)
        sort_combo.bind('<<ComboboxSelected>>', lambda e: self.sort_products())
        
        # Products container with scrollbar
        products_container = tk.Frame(content, bg=Theme.BG_SECONDARY)
        products_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas and Scrollbar
        canvas = tk.Canvas(products_container, bg=Theme.BG_SECONDARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(products_container, orient="vertical", command=canvas.yview)
        
        self.products_frame = tk.Frame(canvas, bg=Theme.BG_SECONDARY)
        
        canvas.create_window((0, 0), window=self.products_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Update scroll region
        self.products_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Mouse wheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def load_products(self):
        """Load sản phẩm vào grid"""
        # Clear existing products
        for widget in self.products_frame.winfo_children():
            widget.destroy()
        
        # Create grid
        row, col = 0, 0
        max_cols = 4
        
        for product in self.filtered_products:
            # Map database fields to card format
            card_data = {
                'id': product['id'],
                'name': product['name'],
                'brand': product.get('category', 'Unknown'),  # Use category as brand
                'price': product['price'],
                'stock': product['quantity'],
                'category': product['category'],
                'image': product.get('image', 'default.jpg')
            }
            
            card = ProductCard(
                self.products_frame,
                card_data,
                on_add_to_cart=self.add_to_cart,
                on_view_detail=self.view_product_detail
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            card.configure(width=220, height=360)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Update result label
        self.result_label.config(text=f"({len(self.filtered_products)} sản phẩm)")
    
    def select_category(self, category):
        """Chọn danh mục"""
        self.current_category = category
        self.category_label.config(text=f"{category}")
        self.filter_products()
    
    def filter_products(self):
        """Lọc sản phẩm theo danh mục và tìm kiếm"""
        search = self.search_var.get().lower()
        
        self.filtered_products = [
            p for p in self.products
            if (self.current_category == "Tất cả" or p['category'] == self.current_category)
            and (search in p['name'].lower() or search in p['brand'].lower())
        ]
        
        self.load_products()
    
    def sort_products(self):
        """Sắp xếp sản phẩm"""
        sort_type = self.sort_var.get()
        
        if sort_type == "Giá tăng dần":
            self.filtered_products.sort(key=lambda x: x['price'])
        elif sort_type == "Giá giảm dần":
            self.filtered_products.sort(key=lambda x: x['price'], reverse=True)
        elif sort_type == "Tên A-Z":
            self.filtered_products.sort(key=lambda x: x['name'])
        
        self.load_products()
    
    def add_to_cart(self, product):
        """Thêm sản phẩm vào giỏ"""
        # Check if product already in cart
        for item in self.cart_items:
            if item['id'] == product['id']:
                item['quantity'] += 1
                messagebox.showinfo("Giỏ hàng", f"Đã thêm 1 {product['name']} vào giỏ!")
                self.update_cart_button()
                return
        
        # Add new item
        self.cart_items.append({
            **product,
            'quantity': 1
        })
        messagebox.showinfo("Giỏ hàng", f"Đã thêm {product['name']} vào giỏ!")
        self.update_cart_button()
    
    def update_cart_button(self):
        """Cập nhật nút giỏ hàng"""
        total_items = sum(item['quantity'] for item in self.cart_items)
        self.cart_btn.config(text=f"🛒 Giỏ hàng ({total_items})")
    
    def show_cart(self):
        """Hiển thị giỏ hàng"""
        if not self.cart_items:
            messagebox.showinfo("Giỏ hàng", "Giỏ hàng của bạn đang trống!")
            return
        
        # Create cart window
        cart_window = tk.Toplevel(self.root)
        cart_window.title("Giỏ hàng")
        cart_window.geometry("600x500")
        
        messagebox.showinfo("Giỏ hàng", f"Bạn có {len(self.cart_items)} sản phẩm trong giỏ!")
    
    def view_product_detail(self, product):
        """Xem chi tiết sản phẩm"""
        detail_window = tk.Toplevel(self.root)
        detail_window.title(product['name'])
        detail_window.geometry("500x600")
        
        messagebox.showinfo("Chi tiết", f"Xem chi tiết: {product['name']}")
    
    def logout(self):
        """Đăng xuất"""
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc muốn đăng xuất?"):
            self.root.destroy()
            # TODO: Return to login

def main():
    root = tk.Tk()
    app = CustomerView(root, "Nguyễn Văn A")
    root.mainloop()

if __name__ == "__main__":
    main()