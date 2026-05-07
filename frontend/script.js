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
function selectRole(role) {
    const form = document.getElementById("loginForm");

    if (role === "police") {
        form.innerHTML = `
            <input type="text" id="policeId" placeholder="Employee ID">
            <input type="password" id="policePass" placeholder="Password">
            <button onclick="loginPolice()">Login as Police</button>
        `;
    } 
    else if (role === "user") {
        form.innerHTML = `
            <input type="text" id="phone" placeholder="Phone Number">
            <button onclick="sendOTP()">Send OTP</button>
            <input type="text" id="otp" placeholder="Enter OTP">
            <button onclick="loginUser()">Login as User</button>
        `;
    }
}
function loginPolice() {
    const id = document.getElementById("policeId").value;
    const pass = document.getElementById("policePass").value;

    if (id === "" || pass === "") {
        alert("Enter credentials");
        return;
    }

    // 👉 Later: connect backend
    window.location.href = "index.html";
}
function sendOTP() {
    alert("OTP sent");
}
function loginUser() {
    const phone = document.getElementById("phone").value;
    const otp = document.getElementById("otp").value;

    if (phone === "" || otp === "") {
        alert("Enter phone and OTP");
        return;
    }

    // 👉 Later: verify OTP from backend
    window.location.href = "user.html";
}
function filterChallans(type) {
    const cards = document.querySelectorAll(".challan-card");

    cards.forEach(card => {
        if (type === "all") {
            card.style.display = "block";
        } else if (card.classList.contains(type)) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}

function logout() {
    window.location.href = "login.html";
}
console.log("JS CONNECTED");
function filterChallans(type) {

    const paidCards = document.querySelectorAll(".paid-card");
    const unpaidCards = document.querySelectorAll(".unpaid-card");

    if(type === "all") {

        paidCards.forEach(card => {
            card.style.display = "block";
        });

        unpaidCards.forEach(card => {
            card.style.display = "block";
        });

    }

    else if(type === "paid") {

        paidCards.forEach(card => {
            card.style.display = "block";
        });

        unpaidCards.forEach(card => {
            card.style.display = "none";
        });

    }

    else if(type === "unpaid") {

        paidCards.forEach(card => {
            card.style.display = "none";
        });

        unpaidCards.forEach(card => {
            card.style.display = "block";
        });

    }
}
function showSection(sectionId) {

    const sections = document.querySelectorAll(".user-section");

    sections.forEach(section => {
        section.style.display = "none";
    });

    document.getElementById(sectionId).style.display = "block";
}
function processPayment() {

    const toast =
    document.getElementById("success-toast");

    const paymentBtn =
    document.getElementById("paymentBtn");

    const paymentText =
    document.getElementById("paymentText");

    // LOADING STATE
    paymentBtn.disabled = true;

    paymentText.innerHTML =
    "⏳ Processing Payment...";

    paymentBtn.style.opacity = "0.7";

    // FAKE PROCESSING
    setTimeout(() => {

        // SUCCESS POPUP
        toast.style.right = "30px";

        // UPDATE COUNTS
        document.getElementById("paidCount")
        .innerText = "3";

        document.getElementById("pendingCount")
        .innerText = "2";

        // CHANGE BUTTON
        paymentText.innerHTML =
        "✅ Payment Successful";

        paymentBtn.style.background =
        "linear-gradient(135deg,#22c55e,#16a34a)";

        setTimeout(() => {

            toast.style.right = "-400px";

            // RESET BUTTON
            paymentText.innerHTML =
            "Pay ₹500";

            paymentBtn.disabled = false;

            paymentBtn.style.opacity = "1";

            paymentBtn.style.background = "";

            // GO TO DOWNLOADS
            showSection('download-section');

        }, 2500);

    }, 2000);

}
function openInvoice() {

    document.getElementById("invoiceModal")
    .style.display = "flex";

}

function closeInvoice() {

    document.getElementById("invoiceModal")
    .style.display = "none";

}
function toggleNotifications() {

    const panel =
    document.getElementById("notificationPanel");

    if(panel.style.display === "block"){

        panel.style.display = "none";

    }

    else{

        panel.style.display = "block";

    }

}
/* LIVE CHALLAN ADD */
setTimeout(() => {

    const grid =
    document.querySelector(".challan-grid");

    const newCard =
    document.createElement("div");

    newCard.className =
    "challan-card unpaid-card live-card";

    newCard.innerHTML = `

        <h3>🚫 Triple Riding</h3>

        <p>Fine: ₹1000</p>

        <p>Status:
        <span class="status unpaid">
        Unpaid
        </span>
        </p>

        <button class="pay-btn"
        onclick="showSection('payment-section')">

            Pay Now

        </button>

    `;

    grid.prepend(newCard);

    // UPDATE NOTIFICATION COUNT
    const count =
    document.getElementById("notificationCount");

    count.innerText =
    parseInt(count.innerText) + 1;

    // ADD NOTIFICATION
    const panel =
    document.getElementById("notificationPanel");

    const item =
    document.createElement("div");

    item.className = "notification-item";

    item.innerHTML =
    "🚫 Triple Riding challan detected";

    panel.prepend(item);

    // UPDATE PENDING COUNT
    document.getElementById("pendingCount")
    .innerText = "4";

}, 6000);