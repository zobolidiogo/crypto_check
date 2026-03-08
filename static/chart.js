const labels = historia.map(p => p.data);
const prices = historia.map(p => p.preco);

const grafico = document.getElementById("grafico_precos");

new Chart(grafico, {
    type: "line",
    data: {
        labels: labels,
        datasets: [{
            label: nomeCrypto,
            data: prices,
            borderColor: "blue",
            tension: 0.2
        }]
    }
});