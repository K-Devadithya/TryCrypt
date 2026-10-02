async function executeProcess() {
    const cipher = document.getElementById('activeCipher').value;
    const action = document.getElementById('activeAction').value;
    const text = document.getElementById('messageInput').value;
    const key = document.getElementById('keyInput').value;

    const resultBox = document.getElementById('resultBox');
    const keyUsedGroup = document.getElementById('keyUsedGroup');
    const keyUsedBox = document.getElementById('keyUsedBox');

    if (!text.trim()) {
        resultBox.innerText = "Error: Input text cannot be empty.";
        return;
    }

    resultBox.innerText = "Processing...";

    try {
        const response = await fetch(`/api/${cipher}/${action}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text, key: key })
        });

        const data = await response.json();

        if (response.ok) {
            resultBox.innerText = data.result;
            
            // Show key used if provided back by server
            if (data.key_used && keyUsedGroup) {
                keyUsedBox.innerText = data.key_used;
                keyUsedGroup.classList.remove('hidden');
            }
        } else {
            resultBox.innerText = `Error: ${data.error || 'Execution failed'}`;
        }
    } catch (err) {
        resultBox.innerText = "Error: System communication failure.";
    }
}

// Universal Copy Function with HTTP/Mobile Fallback
function copyToClipboard(elementId, btnElement) {
    const el = document.getElementById(elementId);
    if (!el) return;

    const textToCopy = el.innerText || el.textContent;

    if (!textToCopy || textToCopy.startsWith("Awaiting") || textToCopy.startsWith("Error")) {
        alert("Nothing valid to copy!");
        return;
    }

    // Try standard Clipboard API first
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(textToCopy).then(() => {
            showCopySuccess(btnElement);
        }).catch(() => {
            fallbackCopyTextToClipboard(textToCopy, btnElement);
        });
    } else {
        // Fallback for HTTP / Mobile local network access
        fallbackCopyTextToClipboard(textToCopy, btnElement);
    }
}

function fallbackCopyTextToClipboard(text, btnElement) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    
    // Avoid scrolling to bottom
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
    textArea.style.opacity = "0";

    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showCopySuccess(btnElement);
        } else {
            alert("Copy failed. Please manually select and copy.");
        }
    } catch (err) {
        alert("Copy failed. Please manually select and copy.");
    }

    document.body.removeChild(textArea);
}

function showCopySuccess(btnElement) {
    if (!btnElement) {
        alert("Copied to clipboard!");
        return;
    }
    const originalText = btnElement.innerText;
    btnElement.innerText = "COPIED!";
    btnElement.style.color = "#00ff66";
    btnElement.style.borderColor = "#00ff66";

    setTimeout(() => {
        btnElement.innerText = originalText;
        btnElement.style.color = "";
        btnElement.style.borderColor = "";
    }, 2000);
}
