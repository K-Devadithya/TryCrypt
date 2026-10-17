// -------------------------------------------------------------------
// SPLASH SCREEN CONTROLLER
// -------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    const splash = document.getElementById("splashScreen");
    if (splash) {
        setTimeout(() => {
            splash.classList.add("fade-out");
        }, 2200);
    }
});


// -------------------------------------------------------------------
// MATRIX CODE RAIN ANIMATION
// -------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("codeRainCanvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    let fontSize = 14;
    let columns = 0;
    let drops = [];

    function initCanvas() {
        canvas.width = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
        canvas.height = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);

        columns = Math.floor(canvas.width / fontSize);
        
        drops = [];
        for (let i = 0; i < columns; i++) {
            drops[i] = Math.floor(Math.random() * -100);
        }
    }

    initCanvas();
    window.addEventListener("resize", initCanvas);

    const chars = "0123456789ABCDEF01<>/{}[];:?#XOR";

    function drawRain() {
        ctx.fillStyle = "rgba(8, 8, 12, 0.12)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.font = `${fontSize}px 'Courier New', monospace`;

        for (let i = 0; i < drops.length; i++) {
            const char = chars[Math.floor(Math.random() * chars.length)];
            
            ctx.fillStyle = Math.random() > 0.95 ? "rgba(0, 255, 204, 0.8)" : "rgba(180, 10, 50, 0.45)";
            ctx.fillText(char, i * fontSize, drops[i] * fontSize);

            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }

            drops[i]++;
        }
    }

    setInterval(drawRain, 40);
});


// -------------------------------------------------------------------
// BACKEND PROCESS EXECUTION
// -------------------------------------------------------------------
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


// -------------------------------------------------------------------
// COPY TO CLIPBOARD WITH HTTP/MOBILE FALLBACK
// -------------------------------------------------------------------
function copyToClipboard(elementId, btnElement) {
    const el = document.getElementById(elementId);
    if (!el) return;

    const textToCopy = el.innerText || el.textContent;

    if (!textToCopy || textToCopy.startsWith("Awaiting") || textToCopy.startsWith("Error")) {
        alert("Nothing valid to copy!");
        return;
    }

    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(textToCopy).then(() => {
            showCopySuccess(btnElement);
        }).catch(() => {
            fallbackCopyTextToClipboard(textToCopy, btnElement);
        });
    } else {
        fallbackCopyTextToClipboard(textToCopy, btnElement);
    }
}

function fallbackCopyTextToClipboard(text, btnElement) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    
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
