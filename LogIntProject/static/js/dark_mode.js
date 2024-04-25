// Get references to DOM elements
var menuContainer = document.querySelector('.navbar-container');
var menuBtn = document.querySelector('.navbar-header .logo .logoImg i');
var body = document.querySelector('body');
var toggleBtn = document.querySelector('.btn-container .button');
var darkModeText = document.querySelector('.dark-light-mode .text');

// Add event listeners
menuBtn.addEventListener('click', menuToggle);
toggleBtn.addEventListener('click', toggleDarkMode);

// Check if dark mode is enabled in local storage
var isDarkModeEnabled = localStorage.getItem('darkModeEnabled') === 'true';
if (isDarkModeEnabled) {
    enableDarkMode();
}

function menuToggle() {
    menuContainer.classList.toggle('active');
}

function toggleDarkMode() {
    var darkModeEnabled = toggleBtn.classList.toggle('active');
    if (darkModeEnabled) {
        enableDarkMode();
    } else {
        disableDarkMode();
    }
}

function enableDarkMode() {
    body.classList.add('active');
    darkModeText.innerHTML = 'Dark Mode';
    localStorage.setItem('darkModeEnabled', 'true');
}

function disableDarkMode() {
    body.classList.remove('active');
    darkModeText.innerHTML = 'Light Mode';
    localStorage.setItem('darkModeEnabled', 'false');
}