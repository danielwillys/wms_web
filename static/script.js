document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("scanner");
    const resultado = document.getElementById("resultado");

    input.addEventListener("change", async () => {
        const codigo = input.value;
        const res = await fetch("/scan", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `codigo=${codigo}`
        });
        const data = await res.json();
        resultado.innerHTML = `<p style="color:${data.status === 'correto' ? 'green' : 'red'}">
            ${data.codigo} → ${data.status.toUpperCase()}
        </p>`;
        input.value = "";
        input.focus();
    });
});