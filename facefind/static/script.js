function captureFace() {
    let status = document.getElementById("status");
    status.innerText = "Capturing face... Please wait.";

    // Show loading animation
    document.getElementById("loading").style.display = "block";

    fetch("/capture", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            document.getElementById("loading").style.display = "none"; // Hide animation

            if (data.redirect) {
                status.innerText = "Face recognized! Redirecting...";
                console.log("Redirecting to:", data.redirect); // Debugging
                setTimeout(() => {
                    window.location.href = data.redirect; // Correctly using the provided redirect URL
                }, 1500);
            } else if (data.register) {
                status.innerText = "Face not found! Please register.";
                document.getElementById("registerBtn").style.display = "block";
            } else {
                status.innerText = data.message;
            }
        })
        .catch(error => {
            document.getElementById("loading").style.display = "none";
            status.innerText = "Error capturing face. Try again.";
            console.error(error);
        });
}

function registerFace() {
    let username = document.getElementById("username").value.trim();
    let status = document.getElementById("status");

    if (!username) {
        status.innerText = "Enter a valid username!";
        return;
    }

    status.innerText = "Registering face... Please wait.";
    document.getElementById("loading").style.display = "block";

    fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("loading").style.display = "none";

        if (data.redirect) {
            status.innerText = "Face registered successfully! Redirecting...";
            console.log("Redirecting to:", data.redirect); // Debugging
            setTimeout(() => {
                window.location.href = data.redirect;  // Use the redirect URL from Flask response
            }, 1500);
        } else {
            status.innerText = data.message;
        }
    })
    .catch(error => {
        document.getElementById("loading").style.display = "none";
        status.innerText = "Error registering face. Try again.";
        console.error(error);
    });
}

function showRegister() {
    document.getElementById("registerSection").style.display = "block";
}

