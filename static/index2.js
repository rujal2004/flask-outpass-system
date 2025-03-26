function login() {
    const enrollment = document.getElementById("loginEnrollment").value;
    const password = document.getElementById("loginPassword").value;
    
    if (enrollment && password) {
        alert("Login successful");
    } else {
        alert("Please fill in both fields");
    }
}

/*function register() {
    const fullName = document.getElementById("fullName").value;
    const enrollment = document.getElementById("registerEnrollment").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("registerPassword").value;
    const hostel = document.getElementById("hostel").value;
    
    if (fullName && enrollment && email && password && hostel) {
        alert("Registration successful");
    } else {
        alert("Please fill in all fields");
    }
}*/
function toggleRegisterForm() {
    const registerBox = document.getElementById("registerBox");
    registerBox.classList.toggle("hidden");
}
