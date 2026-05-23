const labels = historia.map(p => {
    const date = new Date(p.data);

    const mes = String(date.getMonth() + 1).padStart(2, "0");
    const dia = String(date.getDate()).padStart(2, "0");
    const ano = date.getFullYear();

    return `${mes}.${dia}.${ano}`;
});
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
    },
    options: {
        responsive: true,
        scales: {
            x: {
                ticks: {

                    maxRotation: 0,
                    minRotation: 0,

                    callback: function (value, index) {
                        return index % 5 === 0 ? this.getLabelForValue(value) : '';
                    }
                }                
            },

            y: {
                ticks: {
                    callback: function (value) {
                        return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
                    }
                }
            }
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.raw);
                    }
                }
            }
        }
    }
});