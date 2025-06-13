from customtkinter import *
from threading import Thread
import time
from plyer import notification
import json
import os
import ctypes
CONFIG_FILE = "config.json"
city_entry = None
country_entry = None
root = None
# دالة إرسال الإشعار
def notify(prayer_name):
    
    ctypes.windll.user32.LockWorkStation()

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
    global city_entry, country_entry, root
    root = CTk()
    root.geometry("424x340")
    root.title("Select City and Country")
    root.resizable(False, False)
    CTkLabel(root, text="Prayer Reminder", font=("Arial", 32, "bold")).pack(pady=20)
    CTkLabel(root, text="Please enter your city", font=("Arial", 16, "bold")).place(x = 20, y = 100)
    CTkLabel(root, text="Please enter your country", font=("Arial", 16, "bold")).place(x = 20, y = 150)
    city_entry = CTkEntry(root, placeholder_text="City", width=200, height=40, font=("Arial", 16))
    city_entry.place(x=220, y=100)

    country_entry = CTkEntry(root, placeholder_text="Country", width=200, height=40, font=("Arial", 16))
    country_entry.place(x=220, y=150)
    CTkButton(root, text="Submit", command=on_submit, font=("Arial", 16), corner_radius=25, fg_color="#13E52C", text_color="black").place(x = 110, y = 220)
    root.mainloop()

def on_submit():
        global city_entry, country_entry, root
        city = city_entry.get()
        country = country_entry.get()
        if city and country:
            save_config(city, country)
            root.destroy()
            start_app(city, country)

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
