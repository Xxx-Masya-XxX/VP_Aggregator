let combinations = [];

fetch('combinations.json')
    .then(response => response.json())
    .then(data => {
        combinations = data;
        console.log("Комбинации загружены:", combinations);
    })
    .catch(error => console.error("Ошибка загрузки JSON:", error));

function findCombination(targetVp) {
    return combinations.find(combo => combo.total_vp >= targetVp);
}


document.getElementById("search-button").addEventListener("click", () => {
    const vpInput = document.getElementById("vp-input").value;
    const targetVp = parseInt(vpInput, 10);

    if (isNaN(targetVp) || targetVp <= 0) {
        alert("Введите корректное число VP.");
        return;
    }

    const result = findCombination(targetVp);
    const resultTable = document.getElementById("result-table");

    resultTable.innerHTML = "";

    if (result) {
        result.combination.forEach(item => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${item.vp}</td>
                <td>${item.price}</td>
                <td><a href="${item.site}" target="_blank">${item.site}</a></td>
            `;
            resultTable.appendChild(row);
        });
    } else {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td colspan="3">Комбинация не найдена</td>
        `;
        resultTable.appendChild(row);
    }
});