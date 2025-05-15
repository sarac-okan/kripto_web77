import requests
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime
import time

# === Veri Çekme Fonksiyonları ===

def get_price(coin_id, currency):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"
        response = requests.get(url)
        data = response.json()
        return data[coin_id][currency]
    except Exception as e:
        print(f"Error in get_price: {e}")
        return None


def get_price_history(coin_id, days=7, currency="usd"):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency={currency}&days={days}"
        response = requests.get(url)
        data = response.json()
        prices = data["prices"]
        return prices
    except Exception as e:
        print(f"Error in get_price_history: {e}")
        return None


def get_coin_logo(coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        response = requests.get(url)
        data = response.json()
        logo_url = data["image"]["large"]
        image_response = requests.get(logo_url)
        img_data = Image.open(BytesIO(image_response.content))
        img_data = img_data.resize((64, 64), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img_data)
    except Exception as e:
        print(f"Error in get_coin_logo: {e}")
        return None


# === Alarm Fonksiyonu ===

def set_price_alarm(coin_id, target_price, currency):
    global alarms
    alarms.append({"coin": coin_id, "target_price": target_price, "currency": currency})
    messagebox.showinfo("Alarm Ayarlandı", f"{coin_id.upper()} için {target_price} {currency.upper()} alarmı kuruldu.")


# === Favori Kripto Para Yönetimi ===

favorites = []

def toggle_favorite(coin_id):
    global favorites
    if coin_id in favorites:
        favorites.remove(coin_id)
        messagebox.showinfo("Favorilerden Çıkarıldı", f"{coin_id.upper()} favorilerden çıkarıldı.")
    else:
        favorites.append(coin_id)
        messagebox.showinfo("Favorilere Eklendi", f"{coin_id.upper()} favorilere eklendi.")


# === Çoklu Coin Sorgulama Fonksiyonu ===

def fetch_multiple_coins():
    coins = multiple_entry.get().lower().strip().split(",")
    if not coins:
        messagebox.showwarning("Uyarı", "Lütfen bir veya birden fazla coin giriniz!")
        return

    for coin in coins:
        coin = coin.strip()
        if not coin:
            continue
        fetch_and_display_for_coin(coin)


def fetch_and_display_for_coin(coin):
    selected_currency = currency_var.get()
    selected_days = day_range_var.get()
    selected_style = chart_style_var.get()

    price = get_price(coin, selected_currency)
    if price is None:
        messagebox.showerror("Hata", f"{coin} için fiyat verisi alınamadı.")
        return

    currency_symbol = {"usd": "$", "try": "₺", "usdt": "₮"}.get(selected_currency, "")
    price_label.config(text=f"{coin.upper()} Anlık Fiyat: {currency_symbol}{price:.2f}")

    logo = get_coin_logo(coin)
    if logo:
        logo_label.config(image=logo, text="")
        logo_label.image = logo
    else:
        logo_label.config(image='', text='Logo yüklenemedi')

    history = get_price_history(coin, days=selected_days, currency=selected_currency)
    if history:
        timestamps = [datetime.fromtimestamp(p[0] / 1000).strftime('%d-%m') for p in history]
        values = [p[1] for p in history]

        plt.figure(figsize=(10, 4))

        if selected_style == "Çizgi":
            plt.plot(timestamps, values, marker='o')
        elif selected_style == "Çubuk":
            plt.bar(timestamps, values, color='orange')
        elif selected_style == "Alan":
            plt.fill_between(timestamps, values, color='skyblue', alpha=0.5)
            plt.plot(timestamps, values, color='blue')
        elif selected_style == "Nokta":
            plt.scatter(timestamps, values, color='red')

        plt.xticks(rotation=45)
        plt.title(f"{coin.upper()} - Son {selected_days} Gün ({selected_currency.upper()})")
        plt.xlabel("Tarih")
        plt.ylabel(selected_currency.upper())
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    else:
        messagebox.showerror("Hata", "Grafik verisi alınamadı.")


# === Veri Güncelleme Fonksiyonu ===

def update_price():
    coin = entry.get().lower().strip()
    if coin:
        fetch_and_display_for_coin(coin)
    else:
        messagebox.showwarning("Uyarı", "Lütfen bir coin giriniz.")
    root.after(60000, update_price)  # Her 60 saniyede bir güncellemeyi tekrar et


# === Ana Fonksiyon ===

def fetch_and_display():
    coin = entry.get().lower().strip()
    if not coin:
        messagebox.showwarning("Uyarı", "Lütfen bir kripto para adı giriniz!")
        return

    selected_currency = currency_var.get()
    selected_days = day_range_var.get()
    selected_style = chart_style_var.get()

    price = get_price(coin, selected_currency)
    if price is None:
        messagebox.showerror("Hata", f"{coin} için fiyat verisi alınamadı.")
        return

    currency_symbol = {"usd": "$", "try": "₺", "usdt": "₮"}.get(selected_currency, "")
    price_label.config(text=f"{coin.upper()} Anlık Fiyat: {currency_symbol}{price:.2f}")

    logo = get_coin_logo(coin)
    if logo:
        logo_label.config(image=logo, text="")
        logo_label.image = logo
    else:
        logo_label.config(image='', text='Logo yüklenemedi')

    history = get_price_history(coin, days=selected_days, currency=selected_currency)
    if history:
        timestamps = [datetime.fromtimestamp(p[0] / 1000).strftime('%d-%m') for p in history]
        values = [p[1] for p in history]

        plt.figure(figsize=(10, 4))

        if selected_style == "Çizgi":
            plt.plot(timestamps, values, marker='o')
        elif selected_style == "Çubuk":
            plt.bar(timestamps, values, color='orange')
        elif selected_style == "Alan":
            plt.fill_between(timestamps, values, color='skyblue', alpha=0.5)
            plt.plot(timestamps, values, color='blue')
        elif selected_style == "Nokta":
            plt.scatter(timestamps, values, color='red')

        plt.xticks(rotation=45)
        plt.title(f"{coin.upper()} - Son {selected_days} Gün ({selected_currency.upper()})")
        plt.xlabel("Tarih")
        plt.ylabel(selected_currency.upper())
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    else:
        messagebox.showerror("Hata", "Grafik verisi alınamadı.")


# === Tema Uygulama ===

def apply_theme():
    theme = theme_var.get()
    if theme == "Gece":
        bg_color = "#1e1e1e"
        fg_color = "white"
        btn_color = "green"
        price_color = "yellow"
    else:
        bg_color = "white"
        fg_color = "black"
        btn_color = "blue"
        price_color = "darkgreen"

    root.configure(bg=bg_color)
    for widget in root.winfo_children():
        cls = widget._class.name_
        if cls in ["Label", "Button"]:
            widget.configure(bg=bg_color, fg=fg_color)
        elif cls == "Entry":
            widget.configure(bg="white" if theme == "Gündüz" else "#333", fg=fg_color, insertbackground=fg_color)
        elif cls == "OptionMenu":
            widget.configure(bg=bg_color, fg=fg_color)

    price_label.configure(fg=price_color, bg=bg_color)
    logo_label.configure(bg=bg_color)


# === TKINTER Arayüz ===

root = tk.Tk()
root.title("Kripto Para Takip Uygulaması")
root.geometry("540x800")
root.configure(bg="#1e1e1e")

tk.Label(root, text="Kripto Para Adı (örn: bitcoin)", font=("Arial", 14), fg="white", bg="#1e1e1e").pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14), width=30)
entry.pack()

multiple_label = tk.Label(root, text="Birden Fazla Coin Girin (virgülle ayırarak)", font=("Arial", 12), fg="white", bg="#1e1e1e")
multiple_label.pack(pady=5)

multiple_entry = tk.Entry(root, font=("Arial", 14), width=30)
multiple_entry.pack()

# Para birimi seçimi
tk.Label(root, text="Para Birimi Seçin", font=("Arial", 12), fg="white", bg="#1e1e1e").pack(pady=5)
currency_var = tk.StringVar(value="usd")
currency_options = ["usd", "try", "usdt"]
ttk.OptionMenu(root, currency_var, currency_var.get(), *currency_options).pack()

# Gün seçimi
tk.Label(root, text="Tarih Aralığı (Gün)", font=("Arial", 12), fg="white", bg="#1e1e1e").pack(pady=5)
day_range_var = tk.IntVar(value=7)
day_options = [1, 7, 14, 30, 90, 180]
ttk.OptionMenu(root, day_range_var, day_range_var.get(), *day_options).pack()

# Grafik türü seçimi
tk.Label(root, text="Grafik Türü", font=("Arial", 12), fg="white", bg="#1e1e1e").pack(pady=5)
chart_style_var = tk.StringVar(value="Çizgi")
chart_style_options = ["Çizgi", "Çubuk", "Alan", "Nokta"]
ttk.OptionMenu(root, chart_style_var, chart_style_var.get(), *chart_style_options).pack()

# Tema seçimi
tk.Label(root, text="Tema Seçimi", font=("Arial", 12), fg="white", bg="#1e1e1e").pack(pady=5)
theme_var = tk.StringVar(value="Gece")
theme_options = ["Gece", "Gündüz"]
ttk.OptionMenu(root, theme_var, theme_var.get(), *theme_options, command=lambda _: apply_theme()).pack()

# Alarm ayarları
tk.Label(root, text="Fiyat Alarmı", font=("Arial", 12), fg="white", bg="#1e1e1e").pack(pady=5)
alarm_price_entry = tk.Entry(root, font=("Arial", 14), width=15)
alarm_price_entry.pack(pady=5)

def set_alarm():
    coin = entry.get().lower().strip()
    try:
        target_price = float(alarm_price_entry.get())
        if coin and target_price:
            set_price_alarm(coin, target_price, currency_var.get())
        else:
            messagebox.showwarning("Uyarı", "Geçerli bir fiyat giriniz.")
    except ValueError:
        messagebox.showwarning("Hata", "Fiyat geçersiz!")

tk.Button(root, text="Alarm Kur", font=("Arial", 12), command=set_alarm, bg="orange", fg="white").pack(pady=15)

# Favori coin ekleme
tk.Button(root, text="Favorilere Ekle/Kaldır", font=("Arial", 12), command=lambda: toggle_favorite(entry.get().lower().strip()), bg="purple", fg="white").pack(pady=15)

# Fiyat görüntüleme ve grafik çizme
tk.Button(root, text="Fiyatı Göster ve Grafiği Çiz", font=("Arial", 12), command=fetch_multiple_coins, bg="green", fg="white").pack(pady=15)

price_label = tk.Label(root, text="", font=("Arial", 16), fg="yellow", bg="#1e1e1e")
price_label.pack()

logo_label = tk.Label(root, bg="#1e1e1e")
logo_label.pack()

tk.Label(root, text="Veri Kaynağı: CoinGecko API", font=("Arial", 10), fg="gray", bg="#1e1e1e").pack(side="bottom", pady=10)

# Başlangıç teması
apply_theme()

# Güncelleme fonksiyonu
update_price()

root.mainloop()app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
