// static/js/script.js
document.getElementById('generateButton').addEventListener('click', () => {
    fetch('/generate_data')
        .then(response => response.json())
        .then(data => {
            // Display the data on the page
            const outputDiv = document.getElementById('output');
            outputDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
        })
        .catch(error => console.error('Error fetching data:', error));
});
document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.querySelector('.start-button');

    startButton.addEventListener('click', () => {
        // You can add more complex logic here if you need
        alert('Starting the Fake Personas Generator...');
    });
});