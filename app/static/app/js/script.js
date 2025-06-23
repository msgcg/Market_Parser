// Get modal and buttons
const modal = document.getElementById('authModal');
const openButton = document.getElementById('startButton');
const closeButton = document.getElementById('closeButton');

// Open modal
openButton.addEventListener('click', () => {
    modal.style.display = 'block';
});

// Close modal
closeButton.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Close modal when clicking outside of it
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});
