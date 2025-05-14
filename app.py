Flask==2.3.3
requests==2.31.0
matplotlib==3.7.5
gunicorn==20.1.0from flask import Flask, render_template, request
import requests
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # GUI olmadan çalışması için
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os  # port için gerekli

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        coin = request.form['coin'].lower()
        price = get_price(coin, 'usd')
        return render_template('index.html', price=price, coin=coin)
    return render_template('index.html')

def get_price(coin_id, currency):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"
        response = requests.get(url)
        data = response.json()
        return data[coin_id][currency]
    except:
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))