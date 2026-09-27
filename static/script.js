document.addEventListener("DOMContentLoaded", function () {

    const buttons = document.querySelectorAll("button");

    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            button.style.transform = "scale(0.97)";

            setTimeout(function () {
                button.style.transform = "";
            }, 120);
        });
    });

    const inputs = document.querySelectorAll("input");

    inputs.forEach(function (input) {

        input.addEventListener("focus", function () {
            input.style.borderColor = "#39d9ff";
        });

        input.addEventListener("blur", function () {
            input.style.borderColor = "";
        });

    });

    const certificateInput =
        document.querySelector("#certificate_id");

    if (certificateInput) {

        certificateInput.addEventListener("input", function () {

            this.value = this.value
                .toUpperCase()
                .replace(/\s/g, "");

        });

    }

    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {

        form.addEventListener("submit", function () {

            const submitButton =
                form.querySelector("button[type='submit']");

            if (submitButton) {
                submitButton.innerHTML = "Verifying...";
                submitButton.style.opacity = "0.7";
            }

        });

    });

    const statusElements =
        document.querySelectorAll(".status");

    statusElements.forEach(function (status) {

        status.style.opacity = "0";

        setTimeout(function () {
            status.style.transition = "opacity 0.6s ease";
            status.style.opacity = "1";
        }, 150);

    });

});