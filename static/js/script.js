document.getElementById('bulkEmailForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const emails = document.getElementById('emailsInput').value.split('\n').filter(email => email.trim() !== '');
    const totalEmails = emails.length;
    
    if (totalEmails === 0) {
        alert('Please enter at least one email address.');
        return;
    }

    // Show progress container
    document.getElementById('progressContainer').style.display = 'block';
    let progress = 0;

    // Function to update progress
    function updateProgress(value) {
        progress = Math.min(100, value);
        document.getElementById('progressBar').style.width = progress + '%';
        document.getElementById('progressBar').setAttribute('aria-valuenow', progress);
        document.getElementById('progressText').innerText = `Processing: ${progress}%`;
    }

    // Process emails one by one
    let results = [];
    emails.forEach((email, index) => {
        setTimeout(() => {
            fetch('/validate-single-email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'email=' + encodeURIComponent(email.trim())
            })
            .then(response => response.json())
            .then(data => {
                results.push(data);
                updateProgress(Math.round(((index + 1) / totalEmails) * 100));

                if (results.length === totalEmails) {
                    // Redirect to results page after all emails are processed
                    window.location.href = '/results?data=' + encodeURIComponent(JSON.stringify(results));
                }
            });
        }, index * 500); // Adjust delay based on requirement
    });
});
