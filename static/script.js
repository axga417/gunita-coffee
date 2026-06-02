
/* ================= ORDER BUTTON ================= */
function showMessage() {
    alert("Thank you for ordering! ☕ Your Gunita Coffee is being prepared with love.");
}


/* ================= LOGO MODAL ================= */
function openLogo() {
    const modal = document.getElementById("logoModal");
    if (modal) modal.style.display = "flex";
}

function closeLogo() {
    const modal = document.getElementById("logoModal");
    if (modal) modal.style.display = "none";
}


/* ================= CLOSE MODAL WHEN CLICK OUTSIDE ================= */
window.addEventListener("click", function (event) {
    const modal = document.getElementById("logoModal");

    if (modal && event.target === modal) {
        modal.style.display = "none";
    }
});


/* ================= CAROUSEL ARROW SCROLL ================= */
function scrollCarousel(id, amount) {
    const container = document.getElementById(id);

    if (!container) return;

    container.scrollBy({
        left: amount,
        behavior: "smooth"
    });
}


/* ================= KEYBOARD NAVIGATION (OPTIONAL BUT NICE) ================= */
window.addEventListener("keydown", function (e) {

    const active = document.activeElement;

    // only work if user is NOT typing
    if (active && (active.tagName === "INPUT" || active.tagName === "TEXTAREA")) {
        return;
    }

    const carousels = document.querySelectorAll(".carousel");

    carousels.forEach((carousel) => {

        if (e.key === "ArrowRight") {
            carousel.scrollBy({ left: 300, behavior: "smooth" });
        }

        if (e.key === "ArrowLeft") {
            carousel.scrollBy({ left: -300, behavior: "smooth" });
        }
    });
});


/* ================= MOBILE / TOUCH SMOOTH SCROLL ================= */
window.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("logoModal");
    if (modal) modal.style.display = "none";

    /* optional: improve touch scrolling feel */
    document.querySelectorAll(".carousel").forEach((carousel) => {
        carousel.style.scrollBehavior = "smooth";
    });
});