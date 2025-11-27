"""
Customer View - Giao diện khách hàng với Database
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.styles.theme import Theme
from gui.components.product_card import ProductCard
from database.db_manager import get_db

class CustomerView:
    def __init__(self, root, user_data, on_logout=None):
        self.root = root
        self.root.title("Music Store - Khách hàng")
        self.root.geometry("1200x700")
        self.root.state('zoomed')
        
        self.user_data = user_data
        self.user_id = user_data['id']
        self.username = user_data['full_name']
        self.on_logout = on_logout
        
        self.db = get_db()
        self.cart_items = []
        self.current_category_id = None
        self.search_query = ""
        
        # Load data from database
        self.categories = self.db.get_all_categories()
        self.products = self.db.get_all_products()
        self.filtered_products = self.products.copy()
        
        # Load cart
        self.load_cart()
        
        self.root.configure(bg=Theme.BG_SECONDARY)
        self.create_widgets()
        self.load_products()
    
    def load_cart(self):
        """Load giỏ hàng từ database"""
        self.cart_items = self.db.get_cart_items(self.user_id)
        self.update_cart_button()
    
    def create_widgets(self):
        # Header
        self.create_header()
        
        # Main Content
        content_frame = tk.Frame(self.root, bg=Theme.BG_SECONDARY)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.create_sidebar(content_frame)
        
        # Content
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
        
        # Search
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
        
        # Cart
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
        
        # User
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
        """Tạo sidebar"""
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
        
        # All category
        btn = tk.Button(
            sidebar,
            text="Tất cả sản phẩm",
            font=(Theme.FONT_FAMILY, 11),
            bg=Theme.BG_PRIMARY,
            fg=Theme.TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            anchor=tk.W,
            padx=15,
            pady=10,
            command=lambda: self.select_category(None, "Tất cả sản phẩm")
        )
        btn.pack(fill=tk.X)
        btn.bind('<Enter>', lambda e, b=btn: b.config(bg=Theme.HOVER))
        btn.bind('<Leave>', lambda e, b=btn: b.config(bg=Theme.BG_PRIMARY))
        
        # Categories from database
        for category in self.categories:
            cat_text = f"{category.get('icon', '')} {category['name']}"
            btn = tk.Button(
                sidebar,
                text=cat_text,
                font=(Theme.FONT_FAMILY, 11),
                bg=Theme.BG_PRIMARY,
                fg=Theme.TEXT_PRIMARY,
                relief="flat",
                cursor="hand2",
                anchor=tk.W,
                padx=15,
                pady=10,
                command=lambda c=category: self.select_category(c['id'], c['name'])
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
        
        # Sort
        sort_frame = tk.Frame(title_frame, bg=Theme.BG_PRIMARY)
        sort_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        tk.Label(
            sort_frame,
            text="Sắp xếp:",
            font=(Theme.FONT_FAMILY, 11),
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_PRIMARY
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.sort_var = tk.StringVar(value="Mặc định")
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
        
        # Products container
        products_container = tk.Frame(content, bg=Theme.BG_SECONDARY)
        products_container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(products_container, bg=Theme.BG_SECONDARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(products_container, orient="vertical", command=canvas.yview)
        
        self.products_frame = tk.Frame(canvas, bg=Theme.BG_SECONDARY)
        
        canvas.create_window((0, 0), window=self.products_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.products_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def load_products(self):
        """Load sản phẩm"""
        for widget in self.products_frame.winfo_children():
            widget.destroy()
        
        row, col = 0, 0
        max_cols = 4
        
        for product in self.filtered_products:
            # Format product data
            product_data = {
                'id': product['id'],
                'name': product['name'],
                'brand': product['brand'],
                'price': product['price'] * (1 - product['discount_percent'] / 100),
                'stock': product['stock'],
                'category': product.get('category_name', '')
            }
            
            card = ProductCard(
                self.products_frame,
                product_data,
                on_add_to_cart=self.add_to_cart,
                on_view_detail=self.view_product_detail
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            card.configure(width=220, height=360)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        self.result_label.config(text=f"({len(self.filtered_products)} sản phẩm)")
    
    def select_category(self, category_id, category_name):
        """Chọn danh mục"""
        self.current_category_id = category_id
        self.category_label.config(text=category_name)
        self.filter_products()
    
    def filter_products(self):
        """Lọc sản phẩm"""
        search = self.search_var.get().lower()
        
        # Get products from database
        if self.current_category_id:
            all_products = self.db.get_all_products(category_id=self.current_category_id)
        else:
            all_products = self.db.get_all_products()
        
        # Filter by search
        self.filtered_products = [
            p for p in all_products
            if search in p['name'].lower() or search in p['brand'].lower()
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
        """Thêm vào giỏ hàng"""
        # Check stock
        if product['stock'] <= 0:
            messagebox.showwarning("Hết hàng", "Sản phẩm này hiện đã hết hàng!")
            return
        
        # Add to database
        success = self.db.add_to_cart(self.user_id, product['id'], 1)
        
        if success:
            messagebox.showinfo("Thành công", f"Đã thêm {product['name']} vào giỏ hàng!")
            self.load_cart()
        else:
            messagebox.showerror("Lỗi", "Không thể thêm vào giỏ hàng!")
    
    def update_cart_button(self):
        """Cập nhật nút giỏ hàng"""
        total_items = sum(item['quantity'] for item in self.cart_items)
        self.cart_btn.config(text=f"🛒 Giỏ hàng ({total_items})")
    
    def show_cart(self):
        """Hiển thị giỏ hàng"""
        if not self.cart_items:
            messagebox.showinfo("Giỏ hàng", "Giỏ hàng của bạn đang trống!")
            return
        
        from gui.cart_window import CartWindow
        cart_window = tk.Toplevel(self.root)
        CartWindow(cart_window, self.user_data, on_cart_updated=self.load_cart)
    
    def view_product_detail(self, product):
        """Xem chi tiết sản phẩm"""
        # Get full product details
        full_product = self.db.get_product_by_id(product['id'])
        
        if full_product:
            messagebox.showinfo("Chi tiết sản phẩm", 
                f"Tên: {full_product['name']}\n"
                f"Thương hiệu: {full_product['brand']}\n"
                f"Giá: {full_product['price']:,.0f} ₫\n"
                f"Tồn kho: {full_product['stock']}\n"
                f"Mô tả: {full_product.get('description', 'N/A')}"
            )
    
    def logout(self):
        """Đăng xuất"""
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc muốn đăng xuất?"):
            self.root.destroy()
            if self.on_logout:
                self.on_logout()

def main():
    # Demo
    db = get_db()
    user = db.verify_user("customer", "customer123")
    
    if user:
        root = tk.Tk()
        app = CustomerView(root, user)
        root.mainloop()
    else:
        print("Login failed!")

if __name__ == "__main__":
    main()