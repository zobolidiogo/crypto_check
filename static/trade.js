const quantidade_input = document.getElementById("quantidade");
const total = document.getElementById("total");
if (quantidade_input && total) {
    const preco = parseFloat(quantidade_input.dataset.preco);
    quantidade_input.addEventListener("input", () => {
        const quantidade = parseFloat(quantidade_input.value);
        if (!isNaN(quantidade) && quantidade > 0) {
            const valor_total = quantidade * preco;
            total.textContent =
                `Valor estimado: $${valor_total.toFixed(2)}`;
        } else {
            total.textContent = "";
        }
    });
}