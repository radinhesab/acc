"""
نرم‌افزار حسابداری حرفه‌ای - نسخه نهایی
"""

import os
import sys
import tkinter as tk
from pathlib import Path

def main():
    try:
        # تنظیم مسیرهای پروژه به صورت قطعی
        BASE_DIR = Path(__file__).parent.absolute()
        src_path = BASE_DIR / "src"
        
        sys.path.insert(0, str(BASE_DIR))
        sys.path.insert(0, str(src_path))
        
        print(f"مسیرهای جستجو:\n{sys.path}")

        from src.ui.main_window import MainWindow
        from src.utils.config import Config
        from src.database.database_manager import DatabaseManager
        
        config = Config()
        db_manager = DatabaseManager(config)
        print("دیتابیس با موفقیت ایجاد شد")
        
        root = tk.Tk()
        app = MainWindow(root, config)
        root.mainloop()

    except Exception as e:
        print(f"خطا در اجرای برنامه: {str(e)}")
        import traceback
        traceback.print_exc()
        input("برای خروج Enter را فشار دهید...")

if __name__ == "__main__":
    main()