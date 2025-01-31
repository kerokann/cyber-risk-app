document.addEventListener("DOMContentLoaded", function () {
    fetchRisks();
});

function fetchThreats() {
    fetch("/fetch-threats")
        .then(response => response.json())
        .then(data => {
            console.log("Threat Data:", data);
            alert("Threat data fetched successfully! Check console for details.");
        })
        .catch(error => console.error("Error fetching threats:", error));
}

function fetchRisks() {
    fetch("/get-risks")
        .then(response => response.json())
        .then(data => {
            console.log("Risk Data:", data);
            displayRiskChart(data);
        })
        .catch(error => console.error("Error fetching risks:", error));
}

function displayRiskChart(data) {
    const ctx = document.getElementById("riskChart").getContext("2d");
    const labels = data.map(risk => risk[1]);
    const likelihoods = data.map(risk => risk[2]);
    const impacts = data.map(risk => risk[3]);

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Likelihood",
                    backgroundColor: "#ff69b4",
                    data: likelihoods,
                },
                {
                    label: "Impact",
                    backgroundColor: "#ff1493",
                    data: impacts,
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
