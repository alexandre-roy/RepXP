'use strict'

document.addEventListener("DOMContentLoaded", () => {
    const emailInput = document.getElementById("id_email");
    const verifyEmail = document.getElementById("verify-email");

    emailInput.addEventListener("input", () => {
        const email = emailInput.value;

        if (!email) {
            verifyEmail.textContent = "";
            emailInput.classList.remove("is-invalid", "is-valid");
            return;
        }

        fetch(`${window.checkEmailUrl}?email=${encodeURIComponent(email)}`)
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    emailInput.classList.add("is-invalid");
                    emailInput.classList.remove("is-valid");
                    verifyEmail.textContent = "Ce courriel est déjà utilisé.";
                    verifyEmail.style.color = "red";
                } else {
                    emailInput.classList.add("is-valid");
                    emailInput.classList.remove("is-invalid");
                    verifyEmail.textContent = "Courriel disponible.";
                    verifyEmail.style.color = "green";
                }
            });
    });
});
