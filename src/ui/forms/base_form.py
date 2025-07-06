"""
کلاس پایه برای تمام فرم‌ها - نسخه نهایی
"""

import tkinter as tk
from tkinter import ttk, messagebox

class BaseForm:
    """کلاس پایه برای فرم‌ها"""
    
    def __init__(self, parent, config, title, width=600, height=400):
        self.parent = parent
        self.config = config
        self.title = title
        self.width = width
        self.height = height
        
        # ایجاد پنجره
        self.window = tk.Toplevel(parent)
        self.setup_window()
        
        # متغیرهای فرم
        self.form_vars = {}
        
    def setup_window(self):
        """تنظیمات پنجره"""
        self.window.title(self.title)
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.configure(bg=self.config.colors['form_bg'])
        self.window.resizable(False, False)
        self.center_window()
        self.window.option_add('*Font', self.config.fonts['persian_text'])
        self.window.focus_set()
        self.window.grab_set()
    
    def center_window(self):
        """وسط صفحه قرار دادن پنجره"""
        self.window.update_idletasks()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.window.geometry(f"+{x}+{y}")
    
    def create_title_frame(self, title_text):
        """ایجاد فریم عنوان"""
        title_frame = tk.Frame(self.window, bg=self.config.colors['primary'], height=50)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text=title_text,
            font=self.config.fonts['title'],
            bg=self.config.colors['primary'],
            fg=self.config.colors['text_light']
        ).pack(expand=True)
        
        return title_frame
    
    def create_form_frame(self):
        """ایجاد فریم فرم"""
        form_frame = tk.Frame(self.window, bg=self.config.colors['form_bg'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        return form_frame
    
    def create_buttons_frame(self):
        """ایجاد فریم دکمه‌ها"""
        buttons_frame = tk.Frame(self.window, bg=self.config.colors['form_bg'])
        buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        return buttons_frame
    
    def create_label_entry(self, parent, label_text, row, column=0, entry_width=30, is_required=False):
        """ایجاد لیبل و ورودی"""
        label_text = f"{label_text} *" if is_required else label_text
        tk.Label(
            parent,
            text=label_text,
            font=self.config.fonts['persian_text'],
            bg=self.config.colors['form_bg'],
            fg=self.config.colors['text_primary'],
            anchor=tk.E
        ).grid(row=row, column=column+1, sticky=tk.E, padx=(0, 5), pady=5)
        
        var = tk.StringVar()
        entry = tk.Entry(
            parent,
            textvariable=var,
            font=self.config.fonts['persian_text'],
            width=entry_width,
            bg=self.config.colors['input_bg'],
            relief=tk.SOLID,
            bd=1,
            justify=tk.RIGHT
        )
        entry.grid(row=row, column=column, sticky=tk.W, padx=(0, 5), pady=5)
        return var, entry
    
    def create_label_text(self, parent, label_text, row, column=0, text_width=30, text_height=4):
        """ایجاد لیبل و متن چندخطی"""
        tk.Label(
            parent,
            text=label_text,
            font=self.config.fonts['persian_text'],
            bg=self.config.colors['form_bg'],
            fg=self.config.colors['text_primary'],
            anchor=tk.E
        ).grid(row=row, column=column+1, sticky=tk.NE, padx=(0, 5), pady=5)
        
        text_widget = tk.Text(
            parent,
            font=self.config.fonts['persian_text'],
            width=text_width,
            height=text_height,
            bg=self.config.colors['input_bg'],
            relief=tk.SOLID,
            bd=1,
            wrap=tk.WORD
        )
        text_widget.grid(row=row, column=column, sticky=tk.W, padx=(0, 5), pady=5)
        return text_widget
    
    def create_label_combobox(self, parent, label_text, values, row, column=0, combo_width=28):
        """ایجاد لیبل و کمبوباکس"""
        tk.Label(
            parent,
            text=label_text,
            font=self.config.fonts['persian_text'],
            bg=self.config.colors['form_bg'],
            fg=self.config.colors['text_primary'],
            anchor=tk.E
        ).grid(row=row, column=column+1, sticky=tk.E, padx=(0, 5), pady=5)
        
        var = tk.StringVar()
        ttk.Combobox(
            parent,
            textvariable=var,
            values=values,
            font=self.config.fonts['persian_text'],
            width=combo_width,
            state="readonly",
            justify=tk.RIGHT
        ).grid(row=row, column=column, sticky=tk.W, padx=(0, 5), pady=5)
        return var
    
    def create_standard_buttons(self, parent, save_command, cancel_command):
        """ایجاد دکمه‌های استاندارد"""
        tk.Button(
            parent,
            text="لغو",
            font=self.config.fonts['button'],
            bg=self.config.colors['error'],
            fg=self.config.colors['text_light'],
            padx=20,
            pady=5,
            command=cancel_command
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            parent,
            text="ذخیره",
            font=self.config.fonts['button'],
            bg=self.config.colors['success'],
            fg=self.config.colors['text_light'],
            padx=20,
            pady=5,
            command=save_command
        ).pack(side=tk.LEFT)
    
    def show_success_message(self, message):
        messagebox.showinfo("موفقیت", message, parent=self.window)
    
    def show_error_message(self, message):
        messagebox.showerror("خطا", message, parent=self.window)
    
    def show_warning_message(self, message):
        messagebox.showwarning("هشدار", message, parent=self.window)
    
    def close_window(self):
        self.window.destroy()