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
function selectRole(role){

    const form =
    document.getElementById("loginForm");

    const roleButtons =
    document.querySelector(".role-buttons");

    // HIDE ROLE BUTTONS
    roleButtons.style.display = "none";

    if(role === "police"){

        form.innerHTML = `

            <button class="back-btn"
            onclick="goBack()">

                ← Back

            </button>

           <input type="text"
            id="policeId"
            placeholder="Employee ID">

            <input type="password"
            id="policePass"
            placeholder="Password">

            <button onclick="loginPolice()">

                Login as Police

            </button>

        `;

    }

    else{

        form.innerHTML = `

            <button class="back-btn"
            onclick="goBack()">

                ← Back

            </button>

            <input type="text"
            id="phoneNumber"
            placeholder="Phone Number">

            <button>

                Send OTP

            </button>

                <input type="text"
                id="otp"
                placeholder="Enter OTP">

            <button onclick="loginUser()">

                Login as User

            </button>

        `;

    }

}
function goBack(){

    document.querySelector(".role-buttons")
    .style.display = "flex";

    document.getElementById("loginForm")
    .innerHTML = "";

}
function loginPolice() {
const policeIdInput =
document.getElementById("policeId");

const policePassInput =
document.getElementById("policePass");

if(!policeIdInput || !policePassInput){
    return;
}

const id = policeIdInput.value;
const pass = policePassInput.value;

    window.location.href = "index.html";
}
function sendOTP() {
    alert("OTP sent");
}
function loginUser() {

    const phoneInput =
    document.getElementById("phoneNumber");

    const otpInput =
    document.getElementById("otp");

    if(!phoneInput || !otpInput){
        return;
    }

    const phone = phoneInput.value;
    const otp = otpInput.value;

    if(phone === "" || otp === "") {
        alert("Enter phone number and OTP");
        return;
    }

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

    if(!panel) return;

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

    if(grid){
    grid.prepend(newCard);
}
}, 6000);