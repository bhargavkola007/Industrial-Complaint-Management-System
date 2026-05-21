function toggleNavbar(){
    const nav = document.getElementById("navLinks");
    if(nav){
        nav.classList.toggle("show");
    }
}

function previewImage(event){
    const img = document.getElementById("imagePreview");
    const file = event.target.files[0];

    if(img && file){
        img.src = URL.createObjectURL(file);
        img.style.display = "block";
    }
}

function previewAudioName(event){
    const file = event.target.files[0];
    const el = document.getElementById("audioName");

    if(el){
        el.textContent = file ? "Selected audio: " + file.name : "";
    }
}

function formatDuration(totalSeconds){
    totalSeconds = Math.max(0, Math.floor(totalSeconds));

    const h = String(Math.floor(totalSeconds / 3600)).padStart(2, "0");
    const m = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, "0");
    const s = String(totalSeconds % 60).padStart(2, "0");

    return `${h}:${m}:${s}`;
}

function updateTimers(){
    document.querySelectorAll(".live-timer").forEach(el => {
        if(!el.dataset.start) return;

        const start = new Date(el.dataset.start + "Z");
        const now = new Date();
        const seconds = (now - start) / 1000;

        el.textContent = formatDuration(seconds);
    });
}

function autoHideAlerts(){
    document.querySelectorAll(".alert").forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-8px)";
            setTimeout(() => alert.remove(), 400);
        }, 4500);
    });
}

setInterval(updateTimers, 1000);
updateTimers();
autoHideAlerts();