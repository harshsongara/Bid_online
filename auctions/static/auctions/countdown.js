
const targetDate = new Date("{{ object.timer }}"); // Replace with the actual timer value

function updateCountdown() {
    const now = new Date();
    const timeRemaining = targetDate - now;

    if (timeRemaining <= 0) {
        document.getElementById("countdown-{{ object.id }}").textContent = "Auction ended!";
    } else {
        const hours = Math.floor(timeRemaining / 3600000);
        const minutes = Math.floor((timeRemaining % 3600000) / 60000);
        const seconds = Math.floor((timeRemaining % 60000) / 1000);

//        document.getElementById("countdown-{{ object.id }}").textContent = hours+":"+minutes+":"+seconds;
        document.getElementById("countdown-{{ object.id }}").textContent = "{{ object.timer }}"
    }
}

// Update countdown every second
setInterval(updateCountdown, 1000);
