document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll(".fade-in");
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add("show");
        }, index * 150); // Stagger animations
    });
});
