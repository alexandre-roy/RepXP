'use strict'

document.addEventListener("DOMContentLoaded", function () {

    const refreshBtn = document.getElementById("refresh-stats");

    if (refreshBtn) {
        refreshBtn.addEventListener("click", function () {

            fetch(refreshStatsUrl)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("stats-sets").innerText = data.sets;
                    document.getElementById("stats-reps").innerText = data.reps;
                    document.getElementById("stats-ex").innerText = data.exercices;
                    document.getElementById("stats-ent").innerText = data.entrainements;
                    document.getElementById("stats-bad").innerText = data.badges;
                })
                .catch(error => console.error("Erreur AJAX :", error));
        });
    }

});