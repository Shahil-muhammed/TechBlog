document.addEventListener("DOMContentLoaded", function () {
    const submitBtn = document.getElementById("submit");
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");

    let position = 50;  // starting at 50% (center)
    let direction = 1;  // direction: 1 = right, -1 = left

    function inputsAreValid() {
        return usernameInput.value.trim() !== '' && passwordInput.value.trim() !== '';
    }

    submitBtn.addEventListener("mouseenter", function () {
        if (!inputsAreValid()) {
            // Bounce left and right
            position += 20 * direction;
            if (position > 80 || position < 20) direction *= -1; // stay in bounds
            submitBtn.style.left = position + "%";
        }
    });

    // Reset when inputs are valid
    function resetButtonPosition() {
        if (inputsAreValid()) {
            submitBtn.style.left = "50%";
            submitBtn.style.transform = "translateX(-50%)";
            position = 50;
            direction = 1;
        }
    }

    usernameInput.addEventListener("input", resetButtonPosition);
    passwordInput.addEventListener("input", resetButtonPosition);
});
