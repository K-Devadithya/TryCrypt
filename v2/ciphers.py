# ciphers.py — TryCrypt Backend Encryption Engine
import random

# Standard alphabet array used for shifts and index mapping
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


# ------------------------------------------
# 1. CAESAR CIPHER MODULE
# ------------------------------------------


def caesar_encrypt(message: str, key: int) -> str:
    result = []

    for char in message:
        lower_char = char.lower()

        if lower_char in ALPHABET:
            # Handle modulo wrap-around for index offset
            new_index = (ALPHABET.index(lower_char) + key) % len(ALPHABET)
            shifted_char = ALPHABET[new_index]

            # Preserve capital letters
            if char.isupper():
                result.append(shifted_char.upper())
            else:
                result.append(shifted_char)
        else:
            # Keep spaces, punctuation, and digits untouched
            result.append(char)

    return "".join(result)


def caesar_decrypt(message: str, key: int) -> str:
    # Decrypting is just shifting in reverse
    return caesar_encrypt(message, -key)


# ------------------------------------------
# 2. SUBSTITUTION CIPHER MODULE
# ------------------------------------------


def substitution_encrypt(message: str, key: str = None) -> tuple[str, str]:
    # If no key was passed in, shuffle the standard alphabet
    if not key:
        char_list = list(ALPHABET)
        random.shuffle(char_list)
        key = "".join(char_list)

    result = []

    for char in message:
        lower_char = char.lower()

        if lower_char in ALPHABET:
            index = ALPHABET.index(lower_char)
            mapped_char = key[index]

            if char.isupper():
                result.append(mapped_char.upper())
            else:
                result.append(mapped_char)
        else:
            result.append(char)

    return "".join(result), key


def substitution_decrypt(message: str, key: str) -> str:
    # Check for valid key length before attempting reverse mapping
    if not key or len(key) != len(ALPHABET):
        return "Error: A valid 26-character key is required for decryption."

    result = []

    for char in message:
        lower_char = char.lower()

        if lower_char in key:
            # Reverse lookup: find position in key, pull original from ALPHABET
            original_index = key.index(lower_char)
            original_char = ALPHABET[original_index]

            if char.isupper():
                result.append(original_char.upper())
            else:
                result.append(original_char)
        else:
            result.append(char)

    return "".join(result)


# ------------------------------------------
# 3. XOR ONE-TIME PAD (OTP) MODULE
# ------------------------------------------


def otp_encrypt(message: str) -> tuple[list[int], list[int]]:
    key = []
    encrypted_bytes = []

    for char in message:
        # Generate a random byte value (0 to 255) for each character
        random_byte = random.randint(0, 255)
        key.append(random_byte)

        # XOR bitwise operation between ASCII char code and random byte
        encrypted_byte = ord(char) ^ random_byte
        encrypted_bytes.append(encrypted_byte)

    return encrypted_bytes, key


def otp_decrypt(encrypted_bytes: list[int], key: list[int]) -> str:
    decrypted_chars = []

    for i in range(len(encrypted_bytes)):
        # Apply XOR again with the matching key byte to recover ASCII character
        char_code = encrypted_bytes[i] ^ key[i]
        decrypted_chars.append(chr(char_code))

    return "".join(decrypted_chars)
