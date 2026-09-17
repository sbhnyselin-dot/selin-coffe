document.addEventListener("DOMContentLoaded", () => {
    const mobileButton = document.getElementById("mobileMenuBtn");
    const nav = document.querySelector(".main-nav");

    if (mobileButton && nav) {
        mobileButton.addEventListener("click", () => {
            nav.classList.toggle("mobile-open");
        });
    }

    const messages = document.querySelectorAll(".message");

    messages.forEach((message) => {
        setTimeout(() => {
            if (message && message.parentElement) {
                message.remove();
            }
        }, 5000);
    });
});