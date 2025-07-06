"""
پنجره اصلی برنامه - نسخه تصحیح شده
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import threading
import time
import os

# تغییر importها به صورت مطلق با مسیر کامل
from src.utils.persian_date import PersianDate
from src.utils.persian_utils import english_to_persian_digits
from src.ui.components.top_menu import TopMenu
from src.ui.components.status_bar import StatusBar
from src.ui.components.main_content import MainContent

class MainWindow:
    """کلاس پنجره اصلی برنامه"""
    
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.setup_window()
        self.create_widgets()
        self.start_clock_thread()
        
        # اضافه کردن رویداد کلیک برای بستن منوها
        self.root.bind("<Button-1>", self.on_click)
    
    def setup_window(self):
        """تنظیمات پنجره اصلی"""
        self.root.title(f"{self.config.app_name} نسخه {self.config.version}")
        self.root.geometry(f"{self.config.ui_settings['window_width']}x{self.config.ui_settings['window_height']}")
        self.root.minsize(self.config.ui_settings['min_width'], self.config.ui_settings['min_height'])
        
        try:
            self.root.iconbitmap(os.path.join(self.config.assets_dir, 'icon.ico'))
        except:
            pass
        
        self.root.option_add('*Font', self.config.fonts['persian_text'])
        self.root.configure(bg=self.config.colors['secondary'])
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """ایجاد ویجت‌های رابط کاربری"""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.top_menu = TopMenu(self.main_frame, self.config)
        self.main_content = MainContent(self.main_frame, self.config)
        self.status_bar = StatusBar(self.root, self.config)
    
    def show_form_in_main_content(self, form_class, *args, **kwargs):
        """نمایش فرم در محتوای اصلی"""
        if hasattr(self, 'current_form_frame'):
            self.current_form_frame.destroy()
        
        self.current_form_frame = tk.Frame(self.main_content.canvas)
        self.main_content.canvas.create_window(
            self.main_content.canvas.winfo_width() // 2,
            self.main_content.canvas.winfo_height() // 2,
            window=self.current_form_frame,
            anchor=tk.CENTER
        )
        
        form = form_class(self.current_form_frame, self.config, *args, **kwargs)
        
        if hasattr(self, 'status_bar'):
            self.status_bar.update_status(f"فرم فعال: {form.title}")
        
        return form
    
    def on_click(self, event):
        """رویداد کلیک - برای بستن منوها در صورت کلیک خارج از منو"""
        if hasattr(self.top_menu, 'submenu_frame') and self.top_menu.submenu_frame:
            x, y = event.x_root, event.y_root
            submenu = self.top_menu.submenu_frame
            
            submenu_x = submenu.winfo_rootx()
            submenu_y = submenu.winfo_rooty()
            submenu_width = submenu.winfo_width()
            submenu_height = submenu.winfo_height()
            
            if not (submenu_x <= x <= submenu_x + submenu_width and 
                    submenu_y <= y <= submenu_y + submenu_height):
                if self.top_menu.active_menu:
                    button = self.top_menu.menu_buttons.get(self.top_menu.active_menu)
                    if button:
                        button_x = button.winfo_rootx()
                        button_y = button.winfo_rooty()
                        button_width = button.winfo_width()
                        button_height = button.winfo_height()
                        
                        if not (button_x <= x <= button_x + button_width and 
                                button_y <= y <= button_y + button_height):
                            if submenu.winfo_exists():
                                submenu.destroy()
                            self.top_menu.submenu_frame = None
                            self.top_menu.active_menu = None
    
    def start_clock_thread(self):
        """شروع نخ ساعت"""
        self.clock_running = True
        self.clock_thread = threading.Thread(target=self.update_clock, daemon=True)
        self.clock_thread.start()
    
    def update_clock(self):
        """به‌روزرسانی ساعت"""
        while self.clock_running:
            try:
                now = datetime.datetime.now()
                time_str = now.strftime("%H:%M:%S")
                
                p_year, p_month, p_day = PersianDate.now()
                date_str = PersianDate.format_date(p_year, p_month, p_day)
                weekday = PersianDate.get_weekday_name(now.date())
                
                time_str_persian = english_to_persian_digits(time_str)
                date_str_persian = english_to_persian_digits(date_str)
                
                if hasattr(self, 'status_bar'):
                    self.root.after(0, self.status_bar.update_datetime, f"امروز: {weekday} {date_str_persian} - {time_str_persian}")
                
                time.sleep(1)
            except Exception as e:
                print(f"خطا در به‌روزرسانی ساعت: {e}")
                break
    
    def on_closing(self):
        """رویداد بسته شدن برنامه"""
        if messagebox.askokcancel("خروج", "آیا مطمئن هستید که می‌خواهید از برنامه خارج شوید؟"):
            self.clock_running = False
            self.root.quit()
            self.root.destroy()
