import tkinter as tk
from tkinter import ttk
from threading import Thread
import time
from plyer import notification
import json
import os

CONFIG_FILE = "config.json"

# دالة إرسال الإشعار
def notify(prayer_name):
    
    notification.notify(
        title="Prayer Time",
        message=f"It's time for {prayer_name} prayer.",
        timeout=10
    )

# دالة اختبار التنبيه بعد 15 ثانية
def start_test_notification():
    def test():
        print("Waiting 15 seconds for test notification...")
        time.sleep(15)
        notify("Test Prayer")
    Thread(target=test, daemon=True).start()

# دالة بدء التطبيق في الخلفية
def start_app(city, country):
    print(f"Selected city: {city}, {country}")
    print("Starting test notification in 15 seconds...")
    start_test_notification()
    while True:
        time.sleep(1)

# حفظ المدينة والدولة في ملف إعدادات
def save_config(city, country):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"city": city, "country": country}, f)

# تحميل الإعدادات من الملف
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# واجهة المستخدم لتحديد المدينة
def show_city_selector():
    root = tk.Tk()
    root.title("Prayer Reminder")
    root.geometry("350x200")

    tk.Label(root, text="City:").pack(pady=5)
    city_entry = tk.Entry(root)
    city_entry.pack(pady=5)

    tk.Label(root, text="Country Code (2 letters):").pack(pady=5)
    country_entry = tk.Entry(root)
    country_entry.pack(pady=5)

    def on_submit():
        city = city_entry.get()
        country = country_entry.get()
        if city and country:
            save_config(city, country)
            root.destroy()
            start_app(city, country)

    ttk.Button(root, text="Start", command=on_submit).pack(pady=10)
    root.mainloop()

# الدالة الرئيسية
def main():
    config = load_config()
    if config:
        city = config["city"]
        country = config["country"]
        start_app(city, country)
    else:
        show_city_selector()

if __name__ == "__main__":
    main()
