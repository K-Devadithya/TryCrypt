import random
import string
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

CIPHERS_INFO = {
    "caesar": {
        "id": "caesar",
        "title": "Caesar Cipher",
        "badge": "SUBSTITUTION",
        "description": "A simple shift cipher where characters are rotated by a fixed numerical value across the alphabet.",
        "key_label": "Shift Amount (0-25)",
        "key_placeholder": "e.g. 3",
        "key_type": "Numeric Shift"
    },
    "substitution": {
        "id": "substitution",
        "title": "Simple Substitution Cipher",
        "badge": "MONOALPHABETIC",
        "description": "Replaces each letter of the alphabet with a unique randomized 26-character mapping key.",
        "key_label": "26-Character Mapping Key",
        "key_placeholder": "e.g. QWERTYUIOPASDFGHJKLZXCVBNM",
        "key_type": "Alphabet Map"
    },
    "otp": {
        "id": "otp",
        "title": "XOR Cipher (OTP)",
        "badge": "SYMMETRIC PAD",
        "description": "Uses a truly random key sequence equal in length to the plaintext for theoretical unbreakability.",
        "key_label": "Secret Key / Pad",
        "key_placeholder": "Leave empty to auto-generate on encryption...",
        "key_type": "Random Pad"
    }
}

# -------------------------------------------------------------------
# CIPHER ALGORITHMS LOGIC
# -------------------------------------------------------------------

def caesar_cipher(text, shift, mode='encrypt'):
    if mode == 'decrypt':
        shift = -shift
    
    result = []
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            result.append(shifted_char)
        else:
            result.append(char)
    return "".join(result)

def substitution_cipher(text, key, mode='encrypt'):
    alphabet = string.ascii_uppercase
    key = key.upper()
    
    if len(key) != 26 or set(key) != set(alphabet):
        raise ValueError("Key must be a valid 26-letter unique alphabet substitution.")

    result = []
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            upper_char = char.upper()
            
            if mode == 'encrypt':
                idx = alphabet.index(upper_char)
                mapped = key[idx]
            else:
                idx = key.index(upper_char)
                mapped = alphabet[idx]
                
            result.append(mapped if is_upper else mapped.lower())
        else:
            result.append(char)
    return "".join(result)

def xor_otp_cipher(text, key=None, mode='encrypt'):
    if mode == 'encrypt':
        # Auto-generate key of EXACT message length if empty
        if not key:
            key = "".join(random.choices(string.ascii_letters + string.digits, k=len(text)))
        
        # Enforce strict OTP length rule for manual override
        if len(key) < len(text):
            raise ValueError(f"OTP Violation: Key length ({len(key)}) must be greater than or equal to message length ({len(text)}).")
        
        # Truncate key if longer than message to maintain 1:1 length ratio
        key = key[:len(text)]
        
        # XOR process -> convert output to HEX string
        encrypted_bytes = [ord(c) ^ ord(k) for c, k in zip(text, key)]
        hex_result = "".join([f"{b:02x}" for b in encrypted_bytes])
        return hex_result, key

    else: # Decrypt
        if not key:
            raise ValueError("A Secret Key is required to decrypt XOR Cipher.")
        
        try:
            bytes_data = [int(text[i:i+2], 16) for i in range(0, len(text), 2)]
        except ValueError:
            raise ValueError("Invalid hex ciphertext format.")

        # Enforce key length check against byte count during decryption
        if len(key) < len(bytes_data):
            raise ValueError(f"OTP Violation: Provided key length ({len(key)}) is shorter than ciphertext byte length ({len(bytes_data)}).")

        key = key[:len(bytes_data)]
        decrypted_chars = [chr(b ^ ord(k)) for b, k in zip(bytes_data, key)]
        return "".join(decrypted_chars), key
# -------------------------------------------------------------------
# FRONTEND PAGE ROUTES
# -------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cipher/<cipher_id>')
def cipher_hub(cipher_id):
    info = CIPHERS_INFO.get(cipher_id)
    if not info:
        return "Cipher not found", 404
    return render_template('cipher.html', info=info)

@app.route('/cipher/<cipher_id>/encrypt')
def encrypt_page(cipher_id):
    info = CIPHERS_INFO.get(cipher_id)
    if not info:
        return "Cipher not found", 404
    return render_template('encrypt.html', info=info)

@app.route('/cipher/<cipher_id>/decrypt')
def decrypt_page(cipher_id):
    info = CIPHERS_INFO.get(cipher_id)
    if not info:
        return "Cipher not found", 404
    return render_template('decrypt.html', info=info)


# -------------------------------------------------------------------
# BACKEND API ROUTE
# -------------------------------------------------------------------

@app.route('/api/<cipher_id>/<action>', methods=['POST'])
def process_cipher(cipher_id, action):
    data = request.get_json() or {}
    text = data.get('text', '')
    key = data.get('key', '').strip()

    if not text:
        return jsonify({"error": "No input text provided"}), 400

    try:
        if cipher_id == 'caesar':
            shift = int(key) if key else 3
            result = caesar_cipher(text, shift, mode=action)
            return jsonify({"result": result, "key_used": str(shift)})

        elif cipher_id == 'substitution':
            if not key:
                if action == 'encrypt':
                    # Auto-generate random 26 letter map
                    key_list = list(string.ascii_uppercase)
                    random.shuffle(key_list)
                    key = "".join(key_list)
                else:
                    return jsonify({"error": "Key is required for decryption"}), 400

            result = substitution_cipher(text, key, mode=action)
            return jsonify({"result": result, "key_used": key})

        elif cipher_id == 'otp':
            result, key_used = xor_otp_cipher(text, key, mode=action)
            return jsonify({"result": result, "key_used": key_used})

        else:
            return jsonify({"error": "Unknown cipher type"}), 400

    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except Exception as err:
        return jsonify({"error": f"Server processing error: {str(err)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
