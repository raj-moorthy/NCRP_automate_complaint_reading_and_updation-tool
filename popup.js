// Show popup
function showPopup() {
    const popup = document.getElementById("popup");
    if (popup) {
        popup.style.display = "flex";
    }
}

// Close popup
function closePopup() {
    const popup = document.getElementById("popup");
    if (popup) {
        popup.style.display = "none";
    }
}

// Auto show popup if prediction data exists
window.onload = function () {
    const fraud = document.getElementById("fraud-level");
    if (fraud && fraud.innerText.trim() !== "") {
        showPopup();
    }
};
