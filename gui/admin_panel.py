"""
Admin Panel - Giao diện quản trị hệ thống
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
sys.path.append('..')
from gui.styles.theme import Theme
from database.db_manager import ProductManager, OrderManager, UserManager
from gui.components.product_dialogs import AddProductDialog, EditProductDialog, DeleteConfirmDialog

class AdminPanel:
    def __init__(self, root, admin_name="Admin"):
        self.root = root
        self.root.title("Music Store - Quản trị")
        self.root.geometry("1400x800")
        self.root.state('zoomed')
        
        self.admin_name = admin_name
        self.current_section = "dashboard"
        
        # Database managers
        self.product_manager = ProductManager()
        self.order_manager = OrderManager()
        self.user_manager = UserManager()
        
        # Load data from database
        self.products = []
        self.orders = []
        self.load_data()
        
        self.root.configure(bg=Theme.BG_SECONDARY)
        self.create_widgets()
        self.show_dashboard()
    
    def load_data(self):
        """Load data from database"""
        try:
            self.products = self.product_manager.get_all_products()
            self.orders = self.order_manager.get_all_orders()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể load dữ liệu: {e}")
    
    def get_sample_products(self):
        """Deprecated - now using database"""
        return self.products
    
    def get_sample_orders(self):
        return [
            {'id': 1, 'customer': 'Nguyễn Văn A', 'total': 15500000, 'status': 'Đang xử lý', 'date': '2024-01-15'},
            {'id': 2, 'customer': 'Trần Thị B', 'total': 3500000, 'status': 'Hoàn thành', 'date': '2024-01-14'},
            {'id': 3, 'customer': 'Lê Văn C', 'total': 23000000, 'status': 'Đang giao', 'date': '2024-01-13'},
        ]
    
    def create_widgets(self):
        # Header
        self.create_header()
        
        # Main container
        main_container = tk.Frame(self.root, bg=Theme.BG_SECONDARY)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.create_sidebar(main_container)
        
        # Content area
        self.content_frame = tk.Frame(main_container, bg=Theme.BG_SECONDARY)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_header(self):
        header = tk.Frame(self.root, bg=Theme.PRIMARY, height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Logo
        logo_label = tk.Label(
            header,
            text="🎸 Music Store Admin",
            font=(Theme.FONT_FAMILY, 20, "bold"),
            fg=Theme.TEXT_LIGHT,
            bg=Theme.PRIMARY
        )
        logo_label.pack(side=tk.LEFT, padx=30)
        
        # Admin info
        admin_frame = tk.Frame(header, bg=Theme.PRIMARY)
        admin_frame.pack(side=tk.RIGHT, padx=30)
        
        admin_label = tk.Label(
            admin_frame,
            text=f"👤 {self.admin_name}",
            font=(Theme.FONT_FAMILY, 12),
            fg=Theme.TEXT_LIGHT,
            bg=Theme.PRIMARY
        )
        admin_label.pack(side=tk.LEFT, padx=(0, 15))
        
        logout_btn = tk.Button(
            admin_frame,
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
        sidebar = tk.Frame(parent, bg=Theme.BG_DARK, width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Menu items
        menu_items = [
            ("📊", "Dashboard", "dashboard"),
            ("📦", "Quản lý sản phẩm", "products"),
            ("🛍️", "Quản lý đơn hàng", "orders"),
            ("👥", "Quản lý khách hàng", "customers"),
            ("📈", "Thống kê & Báo cáo", "analytics"),
            ("⚙️", "Cài đặt", "settings"),
        ]
        
        tk.Label(
            sidebar,
            text="MENU",
            font=(Theme.FONT_FAMILY, 11, "bold"),
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_DARK
        ).pack(pady=(30, 20), padx=20, anchor=tk.W)
        
        for icon, text, section in menu_items:
            btn = tk.Button(
                sidebar,
                text=f"{icon}  {text}",
                font=(Theme.FONT_FAMILY, 11),
                bg=Theme.BG_DARK,
                fg=Theme.TEXT_LIGHT,
                relief="flat",
                cursor="hand2",
                anchor=tk.W,
                padx=25,
                pady=15,
                command=lambda s=section: self.switch_section(s)
            )
            btn.pack(fill=tk.X)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=Theme.PRIMARY))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=Theme.BG_DARK))
    
    def switch_section(self, section):
        self.current_section = section
        
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Show appropriate section
        if section == "dashboard":
            self.show_dashboard()
        elif section == "products":
            self.show_products()
        elif section == "orders":
            self.show_orders()
        elif section == "customers":
            self.show_customers()
        elif section == "analytics":
            self.show_analytics()
        elif section == "settings":
            self.show_settings()
    
    def show_dashboard(self):
        """Dashboard với các thống kê tổng quan"""
        # Title
        title = tk.Label(
            self.content_frame,
            text="Dashboard",
            font=(Theme.FONT_FAMILY, 24, "bold"),
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_SECONDARY
        )
        title.pack(anchor=tk.W, pady=(0, 20))
        
        # Stats cards
        stats_frame = tk.Frame(self.content_frame, bg=Theme.BG_SECONDARY)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        stats = [
            ("💰", "Doanh thu hôm nay", "42,500,000 ₫", Theme.SUCCESS),
            ("📦", "Sản phẩm", "127", Theme.INFO),
            ("🛍️", "Đơn hàng", "48", Theme.WARNING),
            ("👥", "Khách hàng", "1,234", Theme.PRIMARY),
        ]
        
        for icon, label, value, color in stats:
            self.create_stat_card(stats_frame, icon, label, value, color).pack(
                side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5
            )
        
        # Charts area
        charts_container = tk.Frame(self.content_frame, bg=Theme.BG_SECONDARY)
        charts_container.pack(fill=tk.BOTH, expand=True)
        
        # Revenue chart placeholder
        chart_frame = tk.Frame(charts_container, bg=Theme.BG_PRIMARY)
        chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(
            chart_frame,
            text="📈 Biểu đồ doanh thu",
            font=(Theme.FONT_FAMILY, 14, "bold"),
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_PRIMARY
        ).pack(pady=20)
        
        tk.Label(
            chart_frame,
            text="(Biểu đồ sẽ được vẽ bằng Matplotlib)",
            font=(Theme.FONT_FAMILY, 11),
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_PRIMARY
        ).pack(pady=50)
        
        # Recent orders
        orders_frame = tk.Frame(charts_container, bg=Theme.BG_PRIMARY, width=400)
        orders_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(5, 0))
        orders_frame.pack_propagate(False)
        
        tk.Label(
            orders_frame,
            text="🛍️ Đơn hàng gần đây",
            font=(Theme.FONT_FAMILY, 14, "bold"),
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_PRIMARY
        ).pack(pady=20, padx=20, anchor=tk.W)
        
        for order in self.orders[:5]:
            self.create_order_item(orders_frame, order).pack(fill=tk.X, padx=20, pady=5)
    
    def create_stat_card(self, parent, icon, label, value, color):
        card = tk.Frame(parent, bg=Theme.BG_PRIMARY, relief="flat", borderwidth=1)
        card.configure(highlightbackground=Theme.BORDER, highlightthickness=1)
        
        tk.Label(
            card,
            text=icon,
            font=("Segoe UI", 36),
            bg=Theme.BG_PRIMARY
        ).pack(pady=(20, 10))
        
        tk.Label(
            card,
            text=label,
            font=(Theme.FONT_FAMILY, 11),
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_PRIMARY
        ).pack()
        
        tk.Label(
            card,
            text=value,
            font=(Theme.FONT_FAMILY, 18, "bold"),
            fg=color,
            bg=Theme.BG_PRIMARY
        ).pack(pady=(5, 20))
        
        return card
    
    def create_order_item(self, parent, order):
        item = tk.Frame(parent, bg=Theme.BG_SECONDARY, relief="flat")
        
        info_frame = tk.Frame(item, bg=Theme.BG_SECONDARY)
        info_frame.pack(fill=tk.X, padx=10, pady=8)
        
        tk.Label(
            info_frame,
            text=f"#{order['id']} - {order['customer']}",
            font=(Theme.FONT_FAMILY, 10, "bold"),
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_SECONDARY
        ).pack(side=tk.LEFT)
        
        status_colors = {
            'Đang xử lý': Theme.WARNING,
            'Đang giao': Theme.INFO,
            'Hoàn thành': Theme.SUCCESS
        }
        
        tk.Label(
            info_frame,
            text=order['status'],
            font=(Theme.FONT_FAMILY, 9),
            fg=Theme.TEXT_LIGHT,
            bg=status_colors.get(order['status'], Theme.TEXT_SECONDARY),
            padx=8,
            pady=2
        ).pack(side=tk.RIGHT)
        
        tk.Label(
            item,
            text=f"{order['total']:,.0f} ₫",
            font=(Theme.FONT_FAMILY, 10),
            fg=Theme.DANGER,
            bg=Theme.BG_SECONDARY
        ).pack(side=tk.LEFT, padx=10, pady=(0, 8))
        
        return item
    
    def show_products(self):
        """Quản lý sản phẩm với database"""
        # Title bar
        title_frame = tk.Frame(self.content_frame, bg=Theme.BG_SECONDARY)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="Quản lý sản phẩm",
            font=(Theme.FONT_FAMILY, 24, "bold"),
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_SECONDARY
        ).pack(side=tk.LEFT)
        
        # Refresh button
        refresh_btn = tk.Button(
            title_frame,
            text="🔄 Làm mới",
            **Theme.get_button_style("secondary"),
            command=self.refresh_products
        )
        refresh_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        add_btn = tk.Button(
            title_frame,
            text="➕ Thêm sản phẩm",
            **Theme.get_button_style("success"),
            command=self.add_product
        )
        add_btn.pack(side=tk.RIGHT)
        
        # Table frame
        table_frame = tk.Frame(self.content_frame, bg=Theme.BG_PRIMARY)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview
        columns = ("ID", "Tên sản phẩm", "Danh mục", "Giá", "Tồn kho", "Thao tác")
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Define headings and columns
        column_widths = {
            "ID": 60,
            "Tên sản phẩm": 300,
            "Danh mục": 150,
            "Giá": 150,
            "Tồn kho": 100,
            "Thao tác": 150
        }
        
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=column_widths.get(col, 120))
        
        # Load data from database
        self.refresh_product_table()
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscroll=scrollbar.set)
        
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=(0, 20))
        
        # Bind events
        self.products_tree.bind('<Double-1>', lambda e: self.edit_product())
        self.products_tree.bind('<Button-3>', self.show_product_context_menu)
    
    def refresh_product_table(self):
        """Refresh product table from database"""
        # Clear existing items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Load fresh data
        self.products = self.product_manager.get_all_products()
        
        # Insert data
        for product in self.products:
            self.products_tree.insert("", tk.END, values=(
                product['id'],
                product['name'],
                product['category'],
                f"{product['price']:,} ₫",
                product['quantity'],
                "Sửa | Xóa"
            ), tags=(product['id'],))
    
    def refresh_products(self):
        """Refresh button handler"""
        self.refresh_product_table()
        messagebox.showinfo("Thành công", "Đã làm mới danh sách sản phẩm!")
    
    def show_product_context_menu(self, event):
        """Show context menu on right click"""
        item = self.products_tree.identify_row(event.y)
        if item:
            self.products_tree.selection_set(item)
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="✏️ Sửa", command=self.edit_product)
            menu.add_command(label="🗑️ Xóa", command=self.delete_product)
            menu.post(event.x_root, event.y_root)
    
    def show_orders(self):
        """Quản lý đơn hàng"""
        title = tk.Label(
            self.content_frame,
            text="Quản lý đơn hàng",
            font=(Theme.FONT_FAMILY, 24, "bold"),
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_SECONDARY
        )
        title.pack(anchor=tk.W, pady=(0, 20))
        
        # Filter buttons
        filter_frame = tk.Frame(self.content_frame, bg=Theme.BG_SECONDARY)
        filter_frame.pack(fill=tk.X, pady=(0, 20))
        
        filters = ["Tất cả", "Đang xử lý", "Đang giao", "Hoàn thành", "Đã hủy"]
        for f in filters:
            tk.Button(
                filter_frame,
                text=f,
                **Theme.get_button_style("secondary")
            ).pack(side=tk.LEFT, padx=5)
        
        # Orders table
        table_frame = tk.Frame(self.content_frame, bg=Theme.BG_PRIMARY)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Khách hàng", "Ngày đặt", "Tổng tiền", "Trạng thái", "Thao tác")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        
        for order in self.orders:
            tree.insert("", tk.END, values=(
                order['id'],
                order['customer'],
                order['date'],
                f"{order['total']:,.0f} ₫",
                order['status'],
                "Chi tiết"
            ))
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=(0, 20))
    
    def show_customers(self):
        title = tk.Label(
            self.content_frame,
            text="Quản lý khách hàng",
            font=(Theme.FONT_FAMILY, 24, "bold"),
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_SECONDARY
        )
        title.pack(anchor=tk.W, pady=20)
        
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển!")
    
    def show_analytics(self):
        title = tk.Label(
            self.content_frame,
            text="Thống kê & Báo cáo",
            font=(Theme.FONT_FAMILY, 24, "bold"),
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_SECONDARY
        )
        title.pack(anchor=tk.W, pady=20)
        
        tk.Label(
            self.content_frame,
            text="📊 Dashboard với Matplotlib sẽ được hiển thị ở đây",
            font=(Theme.FONT_FAMILY, 14),
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_SECONDARY
        ).pack(pady=50)
    
    def show_settings(self):
        title = tk.Label(
            self.content_frame,
            text="Cài đặt hệ thống",
            font=(Theme.FONT_FAMILY, 24, "bold"),
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_SECONDARY
        )
        title.pack(anchor=tk.W, pady=20)
        
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển!")
    
    def add_product(self):
        """Mở dialog thêm sản phẩm"""
        def on_save(data):
            try:
                # Save to database
                product_id = self.product_manager.add_product(
                    name=data['name'],
                    category=data['category'],
                    price=data['price'],
                    image=data['image'],
                    quantity=data['quantity'],
                    describe=data['describe']
                )
                
                if product_id:
                    # Refresh table
                    self.refresh_product_table()
                    return True
                else:
                    return False
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi thêm sản phẩm: {e}")
                return False
        
        AddProductDialog(self.root, on_save=on_save)
    
    def edit_product(self):
        """Mở dialog sửa sản phẩm"""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm cần sửa!")
            return
        
        # Get product ID from selected item
        item_values = self.products_tree.item(selected[0])['values']
        product_id = item_values[0]
        
        # Get product data from database
        product_data = self.product_manager.get_product_by_id(product_id)
        
        if not product_data:
            messagebox.showerror("Lỗi", "Không tìm thấy sản phẩm!")
            return
        
        def on_save(data):
            try:
                # Update in database
                success = self.product_manager.update_product(
                    product_id=data['id'],
                    name=data['name'],
                    category=data['category'],
                    price=data['price'],
                    image=data['image'],
                    quantity=data['quantity'],
                    describe=data['describe']
                )
                
                if success:
                    # Refresh table
                    self.refresh_product_table()
                    return True
                else:
                    return False
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi cập nhật: {e}")
                return False
        
        EditProductDialog(self.root, product_data, on_save=on_save)
    
    def delete_product(self):
        """Xóa sản phẩm"""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm cần xóa!")
            return
        
        # Get product info
        item_values = self.products_tree.item(selected[0])['values']
        product_id = item_values[0]
        product_name = item_values[1]
        
        def on_confirm():
            try:
                success = self.product_manager.delete_product(product_id)
                if success:
                    self.refresh_product_table()
                    return True
                else:
                    messagebox.showerror("Lỗi", "Không thể xóa sản phẩm!")
                    return False
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi xóa sản phẩm: {e}")
                return False
        
        DeleteConfirmDialog(self.root, product_name, on_confirm=on_confirm)
    
    def logout(self):
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc muốn đăng xuất?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    app = AdminPanel(root, "Quản trị viên")
    root.mainloop()

if __name__ == "__main__":
    main()