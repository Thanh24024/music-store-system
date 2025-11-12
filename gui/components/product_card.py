"""
Product Card Component - Hiển thị thông tin sản phẩm
"""
import tkinter as tk
from tkinter import ttk
import sys
sys.path.append('../..')
from gui.styles.theme import Theme

class ProductCard(tk.Frame):
    def __init__(self, parent, product_data, on_add_to_cart=None, on_view_detail=None):
        """
        product_data = {
            'id': 1,
            'name': 'Guitar Acoustic',
            'brand': 'Yamaha',
            'price': 5000000,
            'stock': 10,
            'image': None,
            'category': 'Guitar'
        }
        """
        super().__init__(parent, bg=Theme.BG_PRIMARY, relief="solid", borderwidth=1)
        
        self.product_data = product_data
        self.on_add_to_cart = on_add_to_cart
        self.on_view_detail = on_view_detail
        
        self.configure(highlightbackground=Theme.BORDER, highlightthickness=1)
        self.pack_propagate(False)
        
        self.create_widgets()
        
        # Hover effect
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def create_widgets(self):
        # Container
        container = tk.Frame(self, bg=Theme.BG_PRIMARY)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Image placeholder
        image_frame = tk.Frame(
            container,
            bg=Theme.BG_SECONDARY,
            width=180,
            height=180
        )
        image_frame.pack(fill=tk.X, pady=(0, 10))
        image_frame.pack_propagate(False)
        
        # Icon placeholder (emoji)
        icon_label = tk.Label(
            image_frame,
            text="🎸",
            font=("Segoe UI", 60),
            bg=Theme.BG_SECONDARY
        )
        icon_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Category badge
        category_label = tk.Label(
            image_frame,
            text=self.product_data.get('category', 'N/A'),
            font=(Theme.FONT_FAMILY, 8, "bold"),
            bg=Theme.SECONDARY,
            fg=Theme.TEXT_LIGHT,
            padx=8,
            pady=2
        )
        category_label.place(x=5, y=5)
        
        # Stock badge
        stock = self.product_data.get('stock', 0)
        if stock > 0:
            stock_text = f"Còn {stock}"
            stock_bg = Theme.SUCCESS
        else:
            stock_text = "Hết hàng"
            stock_bg = Theme.DANGER
        
        stock_label = tk.Label(
            image_frame,
            text=stock_text,
            font=(Theme.FONT_FAMILY, 8, "bold"),
            bg=stock_bg,
            fg=Theme.TEXT_LIGHT,
            padx=8,
            pady=2
        )
        stock_label.place(relx=1.0, y=5, anchor=tk.NE, x=-5)
        
        # Product info
        info_frame = tk.Frame(container, bg=Theme.BG_PRIMARY)
        info_frame.pack(fill=tk.X)
        
        # Brand
        brand_label = tk.Label(
            info_frame,
            text=self.product_data.get('brand', 'Unknown'),
            font=(Theme.FONT_FAMILY, 9),
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_PRIMARY,
            anchor=tk.W
        )
        brand_label.pack(fill=tk.X, pady=(0, 3))
        
        # Product name
        name_label = tk.Label(
            info_frame,
            text=self.product_data.get('name', 'Product'),
            font=(Theme.FONT_FAMILY, 12, "bold"),
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_PRIMARY,
            anchor=tk.W,
            wraplength=180,
            justify=tk.LEFT
        )
        name_label.pack(fill=tk.X, pady=(0, 8))
        
        # Price
        price = self.product_data.get('price', 0)
        price_label = tk.Label(
            info_frame,
            text=f"{price:,.0f} ₫",
            font=(Theme.FONT_FAMILY, 14, "bold"),
            fg=Theme.DANGER,
            bg=Theme.BG_PRIMARY,
            anchor=tk.W
        )
        price_label.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(container, bg=Theme.BG_PRIMARY)
        button_frame.pack(fill=tk.X)
        
        # View detail button
        detail_btn = tk.Button(
            button_frame,
            text="Xem chi tiết",
            font=(Theme.FONT_FAMILY, 9),
            bg=Theme.BG_SECONDARY,
            fg=Theme.TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            command=self.view_detail
        )
        detail_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5), ipady=6)
        
        # Add to cart button
        if stock > 0:
            cart_btn = tk.Button(
                button_frame,
                text="🛒",
                font=(Theme.FONT_FAMILY, 12),
                bg=Theme.PRIMARY,
                fg=Theme.TEXT_LIGHT,
                relief="flat",
                cursor="hand2",
                width=3,
                command=self.add_to_cart
            )
            cart_btn.pack(side=tk.LEFT, ipady=6)
        else:
            cart_btn = tk.Button(
                button_frame,
                text="🛒",
                font=(Theme.FONT_FAMILY, 12),
                bg=Theme.TEXT_SECONDARY,
                fg=Theme.TEXT_LIGHT,
                relief="flat",
                state="disabled",
                width=3
            )
            cart_btn.pack(side=tk.LEFT, ipady=6)
    
    def on_enter(self, event):
        """Hover effect"""
        self.configure(highlightbackground=Theme.PRIMARY, highlightthickness=2)
    
    def on_leave(self, event):
        """Leave hover"""
        self.configure(highlightbackground=Theme.BORDER, highlightthickness=1)
    
    def add_to_cart(self):
        """Thêm vào giỏ hàng"""
        if self.on_add_to_cart:
            self.on_add_to_cart(self.product_data)
    
    def view_detail(self):
        """Xem chi tiết sản phẩm"""
        if self.on_view_detail:
            self.on_view_detail(self.product_data)

# Test Component
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Product Card Test")
    root.geometry("250x400")
    root.configure(bg=Theme.BG_SECONDARY)
    
    sample_product = {
        'id': 1,
        'name': 'Yamaha F310 Acoustic Guitar',
        'brand': 'Yamaha',
        'price': 3500000,
        'stock': 15,
        'category': 'Guitar'
    }
    
    def on_add(product):
        print(f"Added to cart: {product['name']}")
    
    def on_view(product):
        print(f"View detail: {product['name']}")
    
    card = ProductCard(root, sample_product, on_add, on_view)
    card.pack(padx=20, pady=20)
    card.configure(width=220, height=360)
    
    root.mainloop()