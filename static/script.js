document.getElementById('booking-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Collect form data
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const mpesaNumber = document.getElementById('mpesa-number').value;

    // Validate MPesa number format (basic validation)
    if (!/^\d{10}$/.test(mpesaNumber)) {
        alert('Please enter a valid MPesa number.');
        return;
    }

    // Prepare data for MPesa API request
    const requestData = {
        name: name,
        email: email,
        mpesaNumber: mpesaNumber,
        tillNumber: '123456',
        amount: '1000' // Example amount, adjust as needed
    };

    // Simulate MPesa API request
    fetch('https://your-server-endpoint.com/mpesa-payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Payment request sent. Please check your phone to complete the payment.');
        } else {
            alert('Payment failed. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
});
