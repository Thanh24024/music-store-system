"""
Product Management Dialogs - Thêm/Sửa/Xóa sản phẩm
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
sys.path.append('../..')
from gui.styles.theme import Theme

class AddProductDialog:
    """Dialog thêm sản phẩm mới"""
    
    def __init__(self, parent, on_save=None):
        self.parent = parent
        self.on_save = on_save
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Thêm sản phẩm mới")
        self.dialog.geometry("600x900")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.center_dialog()
        
        self.image_path = "default.jpg"
        self.create_widgets()
    
    def center_dialog(self):
        """Căn giữa dialog"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.dialog, bg=Theme.BG_PRIMARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="➕ Thêm sản phẩm mới",
            **Theme.get_label_style("title")
        )
        title_label.pack(pady=(0, 30))
        
        # Form
        form_frame = tk.Frame(main_frame, bg=Theme.BG_PRIMARY)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Product Name
        self.create_form_field(form_frame, "Tên sản phẩm *", "name")
        
        # Category
        self.create_category_field(form_frame)
        
        # Price
        self.create_form_field(form_frame, "Giá (VND) *", "price", validate="numeric")
        
        # Quantity
        self.create_form_field(form_frame, "Số lượng *", "quantity", validate="numeric")
        
        # Image
        self.create_image_field(form_frame)
        
        # Description
        self.create_text_field(form_frame, "Mô tả *", "describe")
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=Theme.BG_PRIMARY)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Hủy",
            **Theme.get_button_style("secondary"),
            command=self.dialog.destroy
        )
        cancel_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        save_btn = tk.Button(
            button_frame,
            text="Lưu sản phẩm",
            **Theme.get_button_style("success"),
            command=self.save_product
        )
        save_btn.pack(side=tk.RIGHT)
    
    def create_form_field(self, parent, label_text, field_name, validate=None):
        """Tạo field input"""
        field_frame = tk.Frame(parent, bg=Theme.BG_PRIMARY)
        field_frame.pack(fill=tk.X, pady=(0, 15))
        
        label = tk.Label(
            field_frame,
            text=label_text,
            **Theme.get_label_style("normal")
        )
        label.pack(anchor=tk.W, pady=(0, 5))
        
        if validate == "numeric":
            vcmd = (self.dialog.register(self.validate_number), '%P')
            entry = tk.Entry(
                field_frame,
                validate='key',
                validatecommand=vcmd,
                **Theme.get_entry_style()
            )
        else:
            entry = tk.Entry(field_frame, **Theme.get_entry_style())
        
        entry.pack(fill=tk.X, ipady=8)
        setattr(self, f"{field_name}_entry", entry)
    
    def create_category_field(self, parent):
        """Tạo dropdown category"""
        field_frame = tk.Frame(parent, bg=Theme.BG_PRIMARY)
        field_frame.pack(fill=tk.X, pady=(0, 15))
        
        label = tk.Label(
            field_frame,
            text="Danh mục *",
            **Theme.get_label_style("normal")
        )
        label.pack(anchor=tk.W, pady=(0, 5))
        
        self.category_var = tk.StringVar()
        categories = ["Guitar", "Piano", "Drums", "Wind", "Accessories"]
        
        category_combo = ttk.Combobox(
            field_frame,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)
        )
        category_combo.pack(fill=tk.X, ipady=8)
        category_combo.set("Guitar")
    
    def create_image_field(self, parent):
        """Tạo field chọn ảnh"""
        field_frame = tk.Frame(parent, bg=Theme.BG_PRIMARY)
        field_frame.pack(fill=tk.X, pady=(0, 15))
        
        label = tk.Label(
            field_frame,
            text="Hình ảnh",
            **Theme.get_label_style("normal")
        )
        label.pack(anchor=tk.W, pady=(0, 5))
        
        image_frame = tk.Frame(field_frame, bg=Theme.BG_PRIMARY)
        image_frame.pack(fill=tk.X)
        
        self.image_label = tk.Label(
            image_frame,
            text=self.image_path,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL),
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_SECONDARY,
            anchor=tk.W,
            padx=10
        )
        self.image_label.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        
        browse_btn = tk.Button(
            image_frame,
            text="Chọn ảnh",
            **Theme.get_button_style("secondary"),
            command=self.browse_image
        )
        browse_btn.pack(side=tk.LEFT, padx=(10, 0))
    
    def create_text_field(self, parent, label_text, field_name):
        """Tạo text area"""
        field_frame = tk.Frame(parent, bg=Theme.BG_PRIMARY)
        field_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        label = tk.Label(
            field_frame,
            text=label_text,
            **Theme.get_label_style("normal")
        )
        label.pack(anchor=tk.W, pady=(0, 5))
        
        text_widget = tk.Text(
            field_frame,
            height=4,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL),
            relief="solid",
            borderwidth=1
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        setattr(self, f"{field_name}_text", text_widget)
    
    def validate_number(self, value):
        """Validate input là số"""
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False
    
    def browse_image(self):
        """Chọn file ảnh"""
        filename = filedialog.askopenfilename(
            title="Chọn hình ảnh",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.gif"),
                ("All files", "*.*")
            ]
        )
        if filename:
            # Chỉ lấy tên file, không lấy đường dẫn đầy đủ
            import os
            self.image_path = os.path.basename(filename)
            self.image_label.config(text=self.image_path)
    
    def validate_form(self):
        """Kiểm tra dữ liệu nhập"""
        if not self.name_entry.get().strip():
            messagebox.showerror("Lỗi", "Vui lòng nhập tên sản phẩm!")
            return False
        
        if not self.category_var.get():
            messagebox.showerror("Lỗi", "Vui lòng chọn danh mục!")
            return False
        
        if not self.price_entry.get().strip():
            messagebox.showerror("Lỗi", "Vui lòng nhập giá sản phẩm!")
            return False
        
        if not self.quantity_entry.get().strip():
            messagebox.showerror("Lỗi", "Vui lòng nhập số lượng!")
            return False
        
        if not self.describe_text.get("1.0", tk.END).strip():
            messagebox.showerror("Lỗi", "Vui lòng nhập mô tả sản phẩm!")
            return False
        
        return True
    
    def get_data(self):
        """Lấy dữ liệu từ form"""
        return {
            'name': self.name_entry.get().strip(),
            'category': self.category_var.get(),
            'price': int(self.price_entry.get().strip()),
            'image': self.image_path,
            'quantity': int(self.quantity_entry.get().strip()),
            'describe': self.describe_text.get("1.0", tk.END).strip()
        }
    
    def save_product(self):
        """Lưu sản phẩm"""
        if not self.validate_form():
            return
        
        data = self.get_data()
        
        # Show confirmation
        confirm = messagebox.askyesno(
            "Xác nhận",
            f"Bạn có chắc muốn lưu sản phẩm:\n\n{data['name']}?"
        )
        
        if not confirm:
            return
        
        if self.on_save:
            success = self.on_save(data)
            if success:
                messagebox.showinfo("Thành công", "Đã lưu sản phẩm thành công!")
                self.dialog.destroy()
            else:
                messagebox.showerror("Lỗi", "Không thể lưu sản phẩm!")
        else:
            self.dialog.destroy()

class EditProductDialog(AddProductDialog):
    """Dialog sửa sản phẩm"""
    
    def __init__(self, parent, product_data, on_save=None):
        self.product_data = product_data
        super().__init__(parent, on_save)
        self.dialog.title("Chỉnh sửa sản phẩm")
        self.fill_data()
    
    def create_widgets(self):
        super().create_widgets()
        # Change title
        for widget in self.dialog.winfo_children()[0].winfo_children():
            if isinstance(widget, tk.Label) and "Thêm" in widget.cget("text"):
                widget.config(text="✏️ Chỉnh sửa sản phẩm")
                break
    
    def fill_data(self):
        """Điền dữ liệu sản phẩm vào form"""
        self.name_entry.insert(0, self.product_data.get('name', ''))
        self.category_var.set(self.product_data.get('category', 'Guitar'))
        self.price_entry.insert(0, str(self.product_data.get('price', 0)))
        self.quantity_entry.insert(0, str(self.product_data.get('quantity', 0)))
        self.image_path = self.product_data.get('image', 'default.jpg')
        self.image_label.config(text=self.image_path)
        self.describe_text.insert("1.0", self.product_data.get('describe', ''))
    
    def get_data(self):
        """Lấy dữ liệu kèm ID"""
        data = super().get_data()
        data['id'] = self.product_data['id']
        return data

class DeleteConfirmDialog:
    """Dialog xác nhận xóa"""
    
    def __init__(self, parent, product_name, on_confirm=None):
        self.parent = parent
        self.on_confirm = on_confirm
        self.result = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Xác nhận xóa sản phẩm")
        self.dialog.geometry("450x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.center_dialog()
        self.create_widgets(product_name)
    
    def center_dialog(self):
        """Căn giữa dialog"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self, product_name):
        main_frame = tk.Frame(self.dialog, bg=Theme.BG_PRIMARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Icon
        icon_label = tk.Label(
            main_frame,
            text="⚠️",
            font=("Segoe UI", 48),
            bg=Theme.BG_PRIMARY
        )
        icon_label.pack(pady=(0, 20))
        
        # Message
        message_label = tk.Label(
            main_frame,
            text=f"Bạn có chắc chắn muốn xóa sản phẩm:\n\n'{product_name}'?\n\nHành động này không thể hoàn tác!",
            font=(Theme.FONT_FAMILY, 12),
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_PRIMARY,
            justify=tk.CENTER
        )
        message_label.pack(pady=(0, 30))
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=Theme.BG_PRIMARY)
        button_frame.pack()
        
        cancel_btn = tk.Button(
            button_frame,
            text="Hủy bỏ",
            **Theme.get_button_style("secondary"),
            command=self.cancel
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        confirm_btn = tk.Button(
            button_frame,
            text="✓ Xác nhận xóa",
            **Theme.get_button_style("danger"),
            command=self.confirm
        )
        confirm_btn.pack(side=tk.LEFT, padx=5)
    
    def confirm(self):
        """Xác nhận xóa"""
        self.result = True
        if self.on_confirm:
            success = self.on_confirm()
            if success:
                messagebox.showinfo("Thành công", "Đã xóa sản phẩm thành công!")
                self.dialog.destroy()
            else:
                # Don't close dialog if failed
                pass
        else:
            self.dialog.destroy()
    
    def cancel(self):
        """Hủy"""
        self.result = False
        self.dialog.destroy()

# Test dialogs
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    def on_save(data):
        print("Product data:", data)
    
    # Test Add Dialog
    # AddProductDialog(root, on_save)
    
    # Test Edit Dialog
    sample_product = {
        'id': 1,
        'name': 'Yamaha F310',
        'category': 'Guitar',
        'price': 3500000,
        'quantity': 15,
        'image': 'guitar1.jpg',
        'describe': 'Guitar acoustic chất lượng cao'
    }
    EditProductDialog(root, sample_product, on_save)
    
    root.mainloop()