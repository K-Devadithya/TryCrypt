document.addEventListener("DOMContentLoaded", () => {
    const activeCipherInput = document.getElementById("activeCipher");
    if (activeCipherInput) {
        setupKeyPlaceholder(activeCipherInput.value);
    }
});

function setupKeyPlaceholder(cipher) {
    const keyInput = document.getElementById("keyInput");
    if (!keyInput) return;

    if (cipher === "caesar") {
        keyInput.placeholder = "Enter shift number (e.g., 3)";
    } else if (cipher === "substitution") {
        keyInput.placeholder = "Enter 26-char key (or leave blank to auto-generate)";
    } else if (cipher === "otp") {
        keyInput.placeholder = "Comma-separated key numbers (needed for decrypt)";
    }
}

async function processCipher(action) {
    const cipher = document.getElementById("activeCipher").value;
    const message = document.getElementById("messageInput").value;
    const key = document.getElementById("keyInput").value;

    const endpoint = action === "encrypt" ? "/encrypt" : "/decrypt";

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cipher: cipher, message: message, key: key })
        });

        const data = await response.json();

        const resultBox = document.getElementById("resultBox");
        const keyUsedGroup = document.getElementById("keyUsedGroup");
        const keyUsedBox = document.getElementById("keyUsedBox");

        if (data.status === "success") {
            resultBox.innerText = Array.isArray(data.result) ? data.result.join(", ") : data.result;
            
            if (data.key_used) {
                keyUsedGroup.classList.remove("hidden");
                keyUsedBox.innerText = Array.isArray(data.key_used) ? data.key_used.join(", ") : data.key_used;
            } else {
                keyUsedGroup.classList.add("hidden");
            }
        } else {
            resultBox.innerText = "Error: " + data.message;
            keyUsedGroup.classList.add("hidden");
        }
    } catch (err) {
        document.getElementById("resultBox").innerText = "Error: Server connection failed.";
    }
}

function copyToClipboard(elementId) {
    const textToCopy = document.getElementById(elementId).innerText;
    
    if (!textToCopy || textToCopy === "Awaiting input..." || textToCopy === "---") {
        return;
    }

    navigator.clipboard.writeText(textToCopy).then(() => {
        const box = document.getElementById(elementId);
        const copyBtn = box.parentElement.querySelector('.copy-btn');
        const originalText = copyBtn.innerText;
        
        copyBtn.innerText = "COPIED!";
        copyBtn.style.color = "#00FF66";
        
        setTimeout(() => {
            copyBtn.innerText = originalText;
            copyBtn.style.color = "";
        }, 1500);
    });
}
