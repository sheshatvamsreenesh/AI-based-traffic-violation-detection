// ---------------- LOGIN ----------------
function login() {
    const role = document.getElementById("role").value;
    if (role === "police") {
        window.location.href = "index.html";
    } else {
        window.location.href = "user.html";
    }
}

function logout() {
    window.location.href = "login.html";
}

// ---------------- ROLE SELECT ----------------
function selectRole(role){
    const form = document.getElementById("loginForm");
    const roleButtons = document.querySelector(".role-buttons");

    roleButtons.style.display = "none";

    if(role === "police"){
        form.innerHTML = `
            <button class="back-btn" onclick="goBack()">← Back</button>
            <input type="text" id="policeId" placeholder="Employee ID">
            <input type="password" id="policePass" placeholder="Password">
            <button onclick="loginPolice()">Login as Police</button>
        `;
    } else {
        form.innerHTML = `
            <button class="back-btn" onclick="goBack()">← Back</button>
            <input type="text" id="phoneNumber" placeholder="Phone Number">
            <button onclick="sendOTP()">Send OTP</button>
            <input type="text" id="otp" placeholder="Enter OTP">
            <button onclick="loginUser()">Login as User</button>
        `;
    }
}

function goBack(){
    document.querySelector(".role-buttons").style.display = "flex";
    document.getElementById("loginForm").innerHTML = "";
}

// ---------------- LOGIN HANDLERS ----------------
function loginPolice() {
    window.location.href = "index.html";
}

function sendOTP() {
    alert("OTP sent");
}

function loginUser() {
    const phone = document.getElementById("phoneNumber").value;

    if(phone === "") {
        alert("Enter phone number");
        return;
    }

    // store username (important for backend)
    localStorage.setItem("username", phone);

    window.location.href = "user.html";
}

// ---------------- BACKEND: LOAD CHALLANS ----------------
function loadChallans() {
    const user = localStorage.getItem("username");
    if (!user) return;

    fetch(`http://127.0.0.1:5000/challans/${user}`)
    .then(res => res.json())
    .then(data => {
        console.log("Challans:", data);
    });
}

// ---------------- BACKEND: PAYMENT ----------------
function processPayment() {
    const user = localStorage.getItem("username");

    fetch("http://127.0.0.1:5000/pay", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: user,
            violation: "Signal Jump"
        })
    })
    .then(res => res.json())
    .then(() => {
        alert("Payment Successful");
        loadChallans();
    });
}

// ---------------- BACKEND: UPLOAD VIDEO ----------------
function uploadVideo(file) {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("username", localStorage.getItem("username"));

    fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        alert("Violations detected: " + data.violations.length);
    });
}

// ---------------- UI FUNCTIONS ----------------
function showSection(sectionId) {
    const sections = document.querySelectorAll(".user-section");
    sections.forEach(section => section.style.display = "none");
    document.getElementById(sectionId).style.display = "block";
}

function openInvoice() {
    document.getElementById("invoiceModal").style.display = "flex";
}

function closeInvoice() {
    document.getElementById("invoiceModal").style.display = "none";
}

// ---------------- THEME ----------------
function applyTheme(isDarkMode) {
    document.body.classList.toggle("light-mode", !isDarkMode);
    localStorage.setItem("trafficDashboardTheme", isDarkMode ? "dark" : "light");
}

function initThemeToggle() {
    const toggle = document.getElementById("userDarkMode");
    if(!toggle) return;

    const savedTheme = localStorage.getItem("trafficDashboardTheme");
    const isDarkMode = savedTheme !== "light";

    applyTheme(isDarkMode);
    toggle.checked = isDarkMode;

    toggle.addEventListener("change", () => {
        applyTheme(toggle.checked);
    });
}

// ---------------- FILTER ----------------
function filterChallans(type) {
    const paidCards = document.querySelectorAll(".paid-card");
    const unpaidCards = document.querySelectorAll(".unpaid-card");

    if(type === "all") {
        paidCards.forEach(c => c.style.display = "block");
        unpaidCards.forEach(c => c.style.display = "block");
    }
    else if(type === "paid") {
        paidCards.forEach(c => c.style.display = "block");
        unpaidCards.forEach(c => c.style.display = "none");
    }
    else {
        paidCards.forEach(c => c.style.display = "none");
        unpaidCards.forEach(c => c.style.display = "block");
    }
}

// ---------------- INIT ----------------
document.addEventListener("DOMContentLoaded", () => {
    initThemeToggle();
    loadChallans();
});

console.log("FINAL JS CONNECTED");
