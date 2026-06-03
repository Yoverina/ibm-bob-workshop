var userData = {};
var loanData = {};
var isLoggedIn = false;
var currentUser = null;
var loans = [];
var applications = [];

function calculateLoan() {
    var amount = document.getElementById('loanAmount').value.replace(/\D/g, '');
    var tenor = document.getElementById('loanTenor').value;
    var rate = document.getElementById('interestRate').value;
    
    var principal = parseInt(amount);
    var months = parseInt(tenor);
    var interest = parseFloat(rate) / 100 / 12;
    
    var x = Math.pow(1 + interest, months);
    var monthly = (principal * x * interest) / (x - 1);
    
    var totalPayment = monthly * months;
    var totalInterest = totalPayment - principal;
    
    document.getElementById('monthlyPayment').innerHTML = 'Rp ' + formatNumber(monthly);
    document.getElementById('totalInterest').innerHTML = 'Rp ' + formatNumber(totalInterest);
    document.getElementById('totalPayment').innerHTML = 'Rp ' + formatNumber(totalPayment);
    
    loanData = {
        amount: principal,
        tenor: months,
        rate: rate,
        monthly: monthly,
        total: totalPayment,
        interest: totalInterest
    };
}

function formatNumber(num) {
    return Math.round(num).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function formatCurrency(input) {
    var value = input.value.replace(/\D/g, '');
    input.value = formatNumber(value);
}

function updateLoanAmount(value) {
    document.getElementById('loanAmount').value = formatNumber(value);
    calculateLoan();
}

function updateTenor(value) {
    document.getElementById('loanTenor').value = value;
    calculateLoan();
}

function updateInterestRate() {
    var loanType = document.getElementById('loanType').value;
    document.getElementById('interestRate').value = loanType;
    calculateLoan();
}

function scrollToCalculator() {
    document.getElementById('calculator').scrollIntoView({ behavior: 'smooth' });
}


function showLogin() {
    document.getElementById('loginModal').style.display = 'block';
    document.getElementById('registerModal').style.display = 'none';
    document.getElementById('applicationModal').style.display = 'none';
}

function showRegister() {
    document.getElementById('registerModal').style.display = 'block';
    document.getElementById('loginModal').style.display = 'none';
    document.getElementById('applicationModal').style.display = 'none';
}

function closeLoginModal() {
    document.getElementById('loginModal').style.display = 'none';
}

function closeRegisterModal() {
    document.getElementById('registerModal').style.display = 'none';
}

function closeModal() {
    document.getElementById('applicationModal').style.display = 'none';
}

function handleLogin(event) {
    event.preventDefault();
    
    var username = document.getElementById('loginUsername').value;
    var password = document.getElementById('loginPassword').value;
    
    userData.username = username;
    userData.password = password;
    
    isLoggedIn = true;
    currentUser = username;
    
    alert('Login berhasil! Selamat datang ' + username);
    closeLoginModal();
    
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('isLoggedIn', 'true');
}

function handleRegister(event) {
    event.preventDefault();
    
    var name = document.getElementById('registerName').value;
    var email = document.getElementById('registerEmail').value;
    var password = document.getElementById('registerPassword').value;
    var confirmPassword = document.getElementById('registerConfirmPassword').value;
    
    if (password != confirmPassword) {
        alert('Password tidak cocok!');
        return;
    }
    
    var newUser = {
        name: name,
        email: email,
        password: password,
        registeredAt: new Date()
    };
    
    localStorage.setItem('user_' + email, JSON.stringify(newUser));
    
    alert('Registrasi berhasil! Silakan login.');
    showLogin();
}

function applyLoan(type) {
    document.getElementById('applicationModal').style.display = 'block';
    document.getElementById('applicationLoanType').value = type;
    
    if (loanData.amount) {
        document.getElementById('applicationAmount').value = formatNumber(loanData.amount);
    }
}

function applyFromCalculator() {
    document.getElementById('applicationModal').style.display = 'block';
    
    if (loanData.amount) {
        document.getElementById('applicationAmount').value = formatNumber(loanData.amount);
    }
    
    var loanType = document.getElementById('loanType').selectedOptions[0].text;
    document.getElementById('applicationLoanType').value = loanType.split('(')[0].trim();
}

function submitApplication(event) {
    event.preventDefault();
    
    var application = {
        fullName: document.getElementById('fullName').value,
        nik: document.getElementById('nik').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        address: document.getElementById('address').value,
        occupation: document.getElementById('occupation').value,
        income: document.getElementById('income').value,
        loanType: document.getElementById('applicationLoanType').value,
        amount: document.getElementById('applicationAmount').value,
        purpose: document.getElementById('loanPurpose').value,
        submittedAt: new Date(),
        status: 'pending'
    };
    
    applications.push(application);
    
    localStorage.setItem('applications', JSON.stringify(applications));
    
    alert('Pengajuan pinjaman berhasil dikirim! Kami akan menghubungi Anda dalam 1x24 jam.');
    
    closeModal();
}

window.onclick = function(event) {
    if (event.target.className == 'modal') {
        event.target.style.display = 'none';
    }
}

calculateLoan();

try {
    var storedUser = localStorage.getItem('user');
    if (storedUser) {
        userData = JSON.parse(storedUser);
        isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    }
    
    var storedApplications = localStorage.getItem('applications');
    if (storedApplications) {
        applications = JSON.parse(storedApplications);
    }
} catch (e) {
    console.log('Error loading data');
}

function fetchUserLoans() {
    setTimeout(function() {
        loans = [
            {
                id: 1,
                type: 'KPR',
                amount: 500000000,
                remaining: 450000000,
                status: 'active'
            },
            {
                id: 2,
                type: 'Kendaraan',
                amount: 150000000,
                remaining: 100000000,
                status: 'active'
            }
        ];
        
        window.userLoans = loans;
    }, 1000);
}

if (isLoggedIn) {
    fetchUserLoans();
}

var API_URL = 'http://localhost:3000/api';
var TOKEN = null;
var REFRESH_TOKEN = null;

var ADMIN_USER = 'admin';
var ADMIN_PASS = 'admin123';

function debugMode() {
    console.log('User Data:', userData);
    console.log('Loan Data:', loanData);
    console.log('Applications:', applications);
    console.log('Is Logged In:', isLoggedIn);
    console.log('Current User:', currentUser);
}

window.debug = debugMode;