"""
فرم لیست کالا و خدمات - نسخه نهایی
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.forms.base_form import BaseForm
from src.database.database_manager import DatabaseManager
from src.utils.persian_utils import english_to_persian_digits, format_currency

class ProductsListForm(BaseForm):
    """فرم لیست کالا و خدمات"""
    
    def __init__(self, parent, config):
        self.db_manager = DatabaseManager(config)
        super().__init__(parent, config, "لیست کالا و خدمات", 1200, 700)
        self.create_form()
        self.load_data()
        self.selected_product_id = None
    
    def create_form(self):
        """ایجاد فرم"""
        main_frame = tk.Frame(self.window, bg='#F0F0F0')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # بخش فیلترها
        filter_frame = tk.Frame(main_frame, bg='#F0F0F0', height=50)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # فیلد جستجو
        search_frame = tk.Frame(filter_frame, bg='#F0F0F0')
        search_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=20, pady=10)
        
        tk.Label(search_frame, text=": نام کالا یا خدمات", bg='#F0F0F0').pack(side=tk.RIGHT, padx=5)
        
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # جدول محصولات
        table_frame = tk.Frame(main_frame, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_products_table(table_frame)
        
        # دکمه‌ها
        buttons_frame = tk.Frame(main_frame, bg='#F0F0F0', height=60)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(buttons_frame, text="➕ جدید (F1)", command=self.new_product).pack(side=tk.RIGHT, padx=5)
        tk.Button(buttons_frame, text="✏ ویرایش (F2)", command=self.edit_product).pack(side=tk.RIGHT, padx=5)
        tk.Button(buttons_frame, text="🗑 حذف (Del)", command=self.delete_product).pack(side=tk.RIGHT, padx=5)
    
    def create_products_table(self, parent):
        """ایجاد جدول محصولات"""
        columns = ('id', 'title', 'price', 'stock')
        self.products_tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)
        
        # تنظیم ستون‌ها
        self.products_tree.heading('id', text='شناسه')
        self.products_tree.heading('title', text='عنوان')
        self.products_tree.heading('price', text='قیمت')
        self.products_tree.heading('stock', text='موجودی')
        
        self.products_tree.pack(fill=tk.BOTH, expand=True)
    
    def load_data(self):
        """بارگذاری داده‌ها"""
        try:
            products = self.db_manager.get_products()
            for product in products:
                self.products_tree.insert('', 'end', values=(
                    product['id'],
                    product['name'],
                    format_currency(product['price']),
                    english_to_persian_digits(str(product['stock']))
                ))
        except Exception as e:
            self.show_error_message(f"خطا در بارگذاری داده‌ها: {str(e)}")
    
    def new_product(self):
        """محصول جدید"""
        from src.ui.forms.products_form import ProductsForm
        form = ProductsForm(self.window, self.config)
        self.window.wait_window(form.window)
        self.load_data()
    
    def edit_product(self):
        """ویرایش محصول"""
        if not self.selected_product_id:
            self.show_warning_message("لطفاً یک محصول را انتخاب کنید")
            return
        
        from src.ui.forms.products_form import ProductsForm
        product = self.db_manager.get_product(self.selected_product_id)
        form = ProductsForm(self.window, self.config, product)
        self.window.wait_window(form.window)
        self.load_data()
    
    def delete_product(self):
        """حذف محصول"""
        if not self.selected_product_id:
            self.show_warning_message("لطفاً یک محصول را انتخاب کنید")
            return
        
        if messagebox.askyesno("تأیید", "آیا مطمئن هستید؟"):
            try:
                self.db_manager.delete_product(self.selected_product_id)
                self.load_data()
                self.show_success_message("محصول با موفقیت حذف شد")
            except Exception as e:
                self.show_error_message(f"خطا در حذف محصول: {str(e)}")