





let selectedFile = null;
let stream = null;

/* ================= PAGE NAVIGATION ================= */
function goPage(page){
    document.querySelectorAll(".page").forEach(p=>{
        p.classList.remove("active");
    });

    let target = document.getElementById(page + "Page");

    if(target){
        target.classList.add("active");
    }

    window.scrollTo({
        top:0,
        behavior:"smooth"
    });
}

/* ================= FILE UPLOAD ================= */
function openFile(){
    document.getElementById("imageInput").click();
}

document.addEventListener("DOMContentLoaded", function(){

    const input = document.getElementById("imageInput");

    if(input){
        input.addEventListener("change", function(){

            selectedFile = this.files[0];
            if(!selectedFile) return;

            let img = document.getElementById("preview");

            img.src = URL.createObjectURL(selectedFile);
            img.style.display = "block";

            document.getElementById("predictBtn").style.display = "inline-block";
        });
    }

    /* SEARCH + FILTER */
    const searchInput = document.querySelector(".search");
    const filterButtons = document.querySelectorAll(".filters button");

    let activeFilter = "all";

    function filterDiseases(){

        let searchValue = searchInput ? searchInput.value.toLowerCase() : "";

        document.querySelectorAll(".disease-card").forEach(card=>{

            let text = card.textContent.toLowerCase();

            let matchesSearch = text.includes(searchValue);
            let matchesFilter = (activeFilter === "all") ||
                                card.classList.contains(activeFilter);

            card.style.display = (matchesSearch && matchesFilter) ? "block" : "none";
        });
    }

    if(searchInput){
        searchInput.addEventListener("keyup", filterDiseases);
    }

    filterButtons.forEach(btn=>{
        btn.addEventListener("click", function(){

            filterButtons.forEach(b=>b.classList.remove("active"));
            this.classList.add("active");

            activeFilter = this.innerText.toLowerCase();
            filterDiseases();
        });
    });

});

/* ================= CAMERA ================= */
function openCamera(){

    navigator.mediaDevices.getUserMedia({ video:true })
    .then(s=>{
        stream = s;

        let video = document.getElementById("camera");
        video.srcObject = stream;

        video.style.display = "block";
        document.getElementById("captureBtn").style.display = "inline-block";
    })
    .catch(()=>{
        alert("❌ Camera access denied!");
    });
}

function captureImage(){

    let video = document.getElementById("camera");

    let canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    let ctx = canvas.getContext("2d");
    ctx.drawImage(video,0,0);

    canvas.toBlob(blob => {

        selectedFile = blob;

        let img = document.getElementById("preview");
        img.src = URL.createObjectURL(blob);
        img.style.display = "block";

        document.getElementById("predictBtn").style.display = "inline-block";
    });

    if(stream){
        stream.getTracks().forEach(track => track.stop());
    }

    document.getElementById("camera").style.display = "none";
    document.getElementById("captureBtn").style.display = "none";
}

/* ================= AI PREDICTION ================= */
function predictImage(){

    if(!selectedFile){
        alert("⚠️ Upload image first!");
        return;
    }

    let loader = document.getElementById("loader");
    let resultBox = document.getElementById("result");
    let productContainer = document.getElementById("productContainer");
    let btn = document.getElementById("predictBtn");

    btn.disabled = true;
    btn.innerHTML = "⏳ Analyzing...";

    loader.style.display = "block";
    loader.innerHTML = "Scanning Plant...";

    resultBox.innerHTML = "";
    productContainer.innerHTML = "<h2>Recommended Products</h2>";

    let formData = new FormData();
    formData.append("image", selectedFile);

    fetch("/predict",{
        method:"POST",
        body:formData
    })
    .then(res => res.json())
    .then(data => {

        loader.style.display = "none";

        /* ✅ FIXED HTML STRING */
        resultBox.innerHTML = `
            <div class="result-card">
                <h3>${data.emoji} ${data.title}</h3>

                ${data.image ? `<img src="${data.image}" class="result-img">` : ""}

                <p><b>🎯 Confidence:</b> ${data.confidence}%</p>

                <div class="result-section">
                    <h4>📌 Reason</h4>
                    <p>${data.reason}</p>
                </div>

                <div class="result-section">
                    <h4>💊 Cure</h4>
                    <p>${data.cure}</p>
                </div>
            </div>
        `;

        /* PRODUCTS */
        let html = "<h2>Recommended Products</h2>";

        if(data.products && data.products.length > 0){

            data.products.forEach(p=>{
                html += `
                <div class="product-card">
                    <img src="${p.image}" class="product-img">
                    <a href="${p.link}" target="_blank" class="buy-btn">
                        🌿🛒 Protect Your Plants - Buy Now!
                    </a>
                </div>
                `;
            });

        } else {
            html += "<p>No product needed</p>";
        }

        productContainer.innerHTML = html;

        btn.disabled = false;
        btn.innerHTML = "🔁 Analyze Again";

    })
    .catch(()=>{
        loader.style.display = "none";
        btn.disabled = false;
        btn.innerHTML = "🔍 Analyze Plant";
        alert("❌ Server error!");
    });
}




/* ================= CHATBOT ================= */

/* ================= CHATBOT ================= */

let voiceEnabled = false;
let recognition = null;

/* MEDIA ELEMENTS */
const mediaBox = document.getElementById("mediaBox");
const video = document.getElementById("aiVideo");

/* ================= SEND MESSAGE ================= */
function sendMessage() {
    const input = document.getElementById("userInput");
    const text = input.value.trim();

    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: text })
    })
    .then(res => res.json())
    .then(data => {

        let reply = data.reply || "⚠️ No response from server";

        typeEffect(reply);

        if (voiceEnabled) {
            speak(reply);
            voiceEnabled = false;
        }
    })
    .catch(() => {
        addMessage("❌ Server error. Please try again.", "bot");
    });
}

/* ================= ADD MESSAGE ================= */
function addMessage(text, sender) {

    let chatBox = document.getElementById("chatBox");

    let wrapper = document.createElement("div");
    wrapper.classList.add("message", sender);

    let msg = document.createElement("div");
    msg.className = sender === "user" ? "user-msg" : "bot-msg";

    /* TEXT */
    let messageText = document.createElement("div");
    messageText.className = "text";
    messageText.innerText = text;

    /* TIME */
    let time = document.createElement("div");
    time.className = "time";
    time.innerText = new Date().toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
    });

    /* APPEND TEXT + TIME */
    msg.appendChild(messageText);
    msg.appendChild(time);

    /* ✅ USER SIDE (RIGHT + TICKS) */
    if (sender === "user") {
        let ticks = document.createElement("div");
        msg.appendChild(ticks);
    }

    /* 🤖 BOT SIDE (LEFT + AVATAR) */
    if (sender === "bot") {
        let avatar = document.createElement("img");
        avatar.src = "https://cdn-icons-png.flaticon.com/512/4712/4712109.png";
        avatar.className = "bot-avatar";

        wrapper.appendChild(avatar);
    }

    wrapper.appendChild(msg);
    chatBox.appendChild(wrapper);

    chatBox.scrollTop = chatBox.scrollHeight;
}
/* ================= TYPING EFFECT ================= */
function typeEffect(text) {
    const chatBox = document.getElementById("chatBox");

    const msg = document.createElement("div");
    msg.className = "message bot";
    chatBox.appendChild(msg);

    let i = 0;

    // ✅ Cursor (clean + professional)
    const cursor = document.createElement("span");
    cursor.innerHTML = "|";
    cursor.className = "cursor";
    msg.appendChild(cursor);

    function typing() {
        if (i < text.length) {

            const char = text[i];

            // add character before cursor
            cursor.insertAdjacentText("beforebegin", char);
            i++;

            // auto scroll smooth
            chatBox.scrollTo({
                top: chatBox.scrollHeight,
                behavior: "smooth"
            });

            // ✅ PROFESSIONAL HUMAN SPEED LOGIC
            let speed;

            if (char === " ") {
                speed = 5; // fast space
            }
            else if (char === "." || char === "," || char === ";") {
                speed = 140; // small pause
            }
            else if (char === "?" || char === "!") {
                speed = 200; // longer pause
            }
            else if (char === "\n") {
                speed = 180;
            }
            else {
                speed = Math.random() * 20 + 15; // smooth natural typing
            }

            setTimeout(typing, speed);

        } else {
            // ✅ smooth cursor fade out
            cursor.style.opacity = "0";
            setTimeout(() => cursor.remove(), 300);
        }
    }

    // ✅ slight delay before typing (AI thinking feel)
    setTimeout(typing, 300);
}

/* ================= ENTER KEY ================= */
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("userInput");

    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            sendMessage();
        }
    });
});

/* ================= 🎤 VOICE INPUT ================= */
function startListening() {

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("⚠️ Please use Chrome browser for voice feature");
        return;
    }

    if (recognition) {
        recognition.stop();
    }

    recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    // Show media
    if (mediaBox) mediaBox.classList.remove("hidden");
    if (video) video.play();

    recognition.start();
    voiceEnabled = true;

    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;

        document.getElementById("userInput").value = text;
        sendMessage();
    };

    recognition.onerror = () => {
        addMessage("⚠️ Voice recognition error", "bot");
    };

    recognition.onend = () => {
        if (video) video.pause();
    };
}

/* ================= 🔊 VOICE OUTPUT ================= */
function speak(text) {

    if (!("speechSynthesis" in window)) {
        alert("Speech not supported in this browser");
        return;
    }

    window.speechSynthesis.cancel();

    // ✅ REMOVE EMOJIS + SYMBOLS
    const cleanText = text
        .replace(/[\u{1F600}-\u{1F6FF}]/gu, '')   // emojis
        .replace(/[\u{2600}-\u{27BF}]/gu, '')     // symbols
        .replace(/[^\w\s.,?!]/g, '');             // extra symbols

    const speech = new SpeechSynthesisUtterance(cleanText);

    speech.rate = 0.95;
    speech.pitch = 1;
    speech.volume = 1;

    setTimeout(() => {

        const voices = speechSynthesis.getVoices();

        const selectedVoice =
            voices.find(v => v.lang === "hi-IN") ||
            voices.find(v => v.lang === "en-IN") ||
            voices.find(v => v.lang === "en-GB") ||
            voices[0];

        if (selectedVoice) {
            speech.voice = selectedVoice;
            speech.lang = selectedVoice.lang;
        }

        speechSynthesis.speak(speech);

    }, 200);
}
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
    });
}

/* Apply to all messages */
function setAllTimes() {
    document.querySelectorAll(".time").forEach(t => {
        t.innerText = getCurrentTime();
    });
}

/* Run after message added */
setAllTimes();




// ================= FILTER BUTTONS =================
const filterButtons = document.querySelectorAll(".filters button");
const allCards = document.querySelectorAll(".disease-card");

filterButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        // Remove active class from all buttons
        filterButtons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        const filter = btn.textContent.toLowerCase();

        allCards.forEach(card => {
            if (filter === "all") {
                card.style.display = "block";
            } else if (card.classList.contains(filter)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    });
});

// ================= SEARCH FUNCTIONALITY =================

document.getElementById("userInput").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});