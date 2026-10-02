from flask import Flask, render_template, request, jsonify, redirect, url_for
import random
import string

app = Flask(__name__)

# Cipher Metadata for Dynamic Page Rendering
CIPHERS_INFO = {
    "caesar": {
        "title": "Caesar Cipher",
        "description": "A simple shift cipher where characters are rotated by a fixed numerical value.",
        "difficulty": "Easy",
        "type": "Substitution"
    },
    "substitution": {
        "title": "Simple Substitution Cipher",
        "description": "Replaces each letter of the alphabet with a randomized 26-character mapping key.",
        "difficulty": "Medium",
        "type": "Monoalphabetic"
    },
    "otp": {
        "title": "One-Time Pad (OTP)",
        "description": "Uses a truly random key sequence equal in length to the plaintext for theoretical unbreakability.",
        "difficulty": "Advanced",
        "type": "Symmetric Pad"
    }
}

# --- Cryptographic Logic ---
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def gen_substitution_key():
    alphabet = list(string.ascii_uppercase)
    shuffled = alphabet.copy()
    random.shuffle(shuffled)
    return "".join(shuffled)

def substitution_encrypt(text, key):
    alphabet = string.ascii_uppercase
    key = key.upper()
    result = ""
    for char in text:
        if char.isupper():
            idx = alphabet.find(char)
            result += key[idx] if idx != -1 else char
        elif char.islower():
            idx = alphabet.find(char.upper())
            result += key[idx].lower() if idx != -1 else char
        else:
            result += char
    return result

def substitution_decrypt(text, key):
    alphabet = string.ascii_uppercase
    key = key.upper()
    result = ""
    for char in text:
        if char.isupper():
            idx = key.find(char)
            result += alphabet[idx] if idx != -1 else char
        elif char.islower():
            idx = key.find(char.upper())
            result += alphabet[idx].lower() if idx != -1 else char
        else:
            result += char
    return result

def otp_encrypt(text):
    text_clean = [c.upper() for c in text if c.isalpha()]
    key = [random.randint(0, 25) for _ in text_clean]
    cipher_nums = [(ord(char) - ord('A') + key[i]) % 26 for i, char in enumerate(text_clean)]
    encrypted_text = "".join(chr(n + ord('A')) for n in cipher_nums)
    return encrypted_text, key

def otp_decrypt(text, key_list):
    text_clean = [c.upper() for c in text if c.isalpha()]
    plain_nums = [(ord(char) - ord('A') - key_list[i]) % 26 for i, char in enumerate(text_clean)]
    return "".join(chr(n + ord('A')) for n in plain_nums)


# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html", ciphers=CIPHERS_INFO)

@app.route("/cipher/<cipher_type>")
def cipher_page(cipher_type):
    if cipher_type not in CIPHERS_INFO:
        return redirect(url_for("index"))
    info = CIPHERS_INFO[cipher_type]
    return render_template("cipher.html", cipher_id=cipher_type, info=info)

@app.route("/encrypt", methods=["POST"])
def encrypt():
    data = request.json
    cipher = data.get("cipher")
    message = data.get("message", "")
    key = data.get("key", "")

    if not message:
        return jsonify({"status": "error", "message": "Message cannot be empty."})

    try:
        if cipher == "caesar":
            shift = int(key) if key else 3
            result = caesar_encrypt(message, shift)
            return jsonify({"status": "success", "result": result, "key_used": str(shift)})

        elif cipher == "substitution":
            key_used = key if (key and len(key) == 26) else gen_substitution_key()
            result = substitution_encrypt(message, key_used)
            return jsonify({"status": "success", "result": result, "key_used": key_used})

        elif cipher == "otp":
            result, key_used = otp_encrypt(message)
            return jsonify({"status": "success", "result": result, "key_used": key_used})

        return jsonify({"status": "error", "message": "Invalid cipher selected."})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/decrypt", methods=["POST"])
def decrypt():
    data = request.json
    cipher = data.get("cipher")
    message = data.get("message", "")
    key = data.get("key", "")

    if not message:
        return jsonify({"status": "error", "message": "Message cannot be empty."})

    try:
        if cipher == "caesar":
            shift = int(key) if key else 3
            result = caesar_decrypt(message, shift)
            return jsonify({"status": "success", "result": result})

        elif cipher == "substitution":
            if not key or len(key) != 26:
                return jsonify({"status": "error", "message": "26-character key required for substitution decryption."})
            result = substitution_decrypt(message, key)
            return jsonify({"status": "success", "result": result})

        elif cipher == "otp":
            if not key:
                return jsonify({"status": "error", "message": "Key numbers required for OTP decryption."})
            key_list = [int(k.strip()) for k in key.split(",") if k.strip().isdigit()]
            result = otp_decrypt(message, key_list)
            return jsonify({"status": "success", "result": result})

        return jsonify({"status": "error", "message": "Invalid cipher selected."})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
