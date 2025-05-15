async function getPrice() {
    const coin = document.getElementById('coinInput').value.trim().toLowerCase();
    const currency = document.getElementById('currencySelect').value;

    if (!coin) {
        alert('Lütfen bir coin adı giriniz.');
        return;
    }

    const resultDiv = document.getElementById('result');
    resultDiv.textContent = "Yükleniyor...";

    try {
        const res = await fetch(`/api/price?coin=${coin}&currency=${currency}`);
        const data = await res.json();

        if (res.ok) {
            const price = data[coin][currency];
            const symbol = currency === 'usd' ? '$' : (currency === 'try' ? '₺' : '€');
            resultDiv.textContent = `${coin.toUpperCase()} fiyatı: ${symbol}${price}`;
        } else {
            resultDiv.textContent = "Hata: " + (data.error || 'Bilinmeyen hata');
        }
    } catch (error) {
        resultDiv.textContent = "Sunucuya erişilemiyor.";
    }
}
