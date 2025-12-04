'use strict';

document.addEventListener("DOMContentLoaded", () => {
    const emailInput = document.getElementById("id_email");
    const verifyEmail = document.getElementById("verify-email");

    emailInput.addEventListener("input", () => {
        const email = emailInput.value.trim();

        if (!email) {
            verifyEmail.textContent = "";
            emailInput.classList.remove("is-valid", "is-invalid");
            return;
        }

        fetch(`${window.checkEmailUrl}?email=${encodeURIComponent(email)}`)
            .then(r => r.json())
            .then(data => {
                if (data.valid) {
                    emailInput.classList.add("is-valid");
                    emailInput.classList.remove("is-invalid");
                    verifyEmail.textContent = data.message;
                    verifyEmail.style.color = "green";
                } else {
                    emailInput.classList.add("is-invalid");
                    emailInput.classList.remove("is-valid");
                    verifyEmail.textContent = data.message;
                    verifyEmail.style.color = "red";
                }
            });
    });
});
