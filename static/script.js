async function getCoin() {
    const coin = document.getElementById("coin").value.toLowerCase();
    const currency = document.getElementById("currency").value.toLowerCase();
    const days = document.getElementById("days").value;

    // API'den fiyat ve grafik verisi çek
    const response = await fetch(`/api/price?coin=${coin}&currency=${currency}&days=${days}`);
    const data = await response.json();

    if (!data.price) {
        alert("Fiyat verisi alınamadı!");
        return;
    }

    // Fiyat gösterimi
    const symbolMap = { usd: "$", try: "₺", usdt: "₮" };
    document.getElementById("price").textContent = `${coin.toUpperCase()} Anlık Fiyat: ${symbolMap[currency]}${data.price}`;

    // Logo yükleme (CoinGecko API coin detaydan alabiliriz)
    try {
        const logoRes = await fetch(`https://api.coingecko.com/api/v3/coins/${coin}`);
        const logoData = await logoRes.json();
        document.getElementById("logo").src = logoData.image.large;
        document.getElementById("logo").alt = coin;
    } catch {
        document.getElementById("logo").src = "";
        document.getElementById("logo").alt = "Logo bulunamadı";
    }

    // Grafik çizimi
    const prices = data.prices;
    const labels = prices.map(p => {
        const date = new Date(p[0]);
        return date.toLocaleDateString();
    });
    const values = prices.map(p => p[1]);

    // Chart.js canvas'ı al ve varsa önceki grafiği sil
    const ctx = document.getElementById('chart').getContext('2d');
    if (window.myChart) window.myChart.destroy();

    window.myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `${coin.toUpperCase()} Fiyat`,
                data: values,
                borderColor: 'blue',
                backgroundColor: 'rgba(0,0,255,0.1)',
                fill: true,
                tension: 0.2,
                pointRadius: 2,
            }]
        },
        options: {
            scales: {
                x: { display: true },
                y: { beginAtZero: false }
            },
            responsive: true,
            plugins: {
                legend: { display: true }
            }
        }
    });
}
