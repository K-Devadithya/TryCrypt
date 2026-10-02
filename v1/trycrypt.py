import string
import random

keyboard_characters = list(string.ascii_lowercase)
caesar_len = len(keyboard_characters)

def print_banner():
    banner = """
  ┌─────────────────────────────────────────────────────────┐
  │                        TRYCRYPT                         │
  │          A Simple & Modular Encryption Toolkit          │
  └─────────────────────────────────────────────────────────┘
    """
    print(banner)

def caesar_encoder():
    key = int(input('Enter the key value for the encoding: '))
    message = input('Enter the message to be encrypted: ')
    encrypted_msg = []

    for i in message:
        is_upper = i.isupper()
        char = i.lower()

        if char in keyboard_characters:
            index = (keyboard_characters.index(char) + key) % caesar_len
            shifted_char = keyboard_characters[index]
            encrypted_msg.append(shifted_char.upper() if is_upper else shifted_char)
        else:
            encrypted_msg.append(i)

    output = "".join(encrypted_msg)
    print('\nThe encrypted message is: ' + output)
    print(f'Key used: {key}\n')

def caesar_decoder():
    key = int(input('Enter the key value used for encoding: '))
    message = input('Enter the encrypted message: ')
    decrypted_msg = []

    for i in message:
        is_upper = i.isupper()
        char = i.lower()

        if char in keyboard_characters:
            index = (keyboard_characters.index(char) - key) % caesar_len
            shifted_char = keyboard_characters[index]
            decrypted_msg.append(shifted_char.upper() if is_upper else shifted_char)
        else:
            decrypted_msg.append(i)

    output = "".join(decrypted_msg)
    print('The decrypted message is: ' + output)

def substitution_encoder():
    shuffled = keyboard_characters.copy()
    random.shuffle(shuffled)
    key = "".join(shuffled)

    message = input('Enter the message to be encrypted: ')
    encrypted_msg = []

    for i in message:
        is_upper = i.isupper()
        char = i.lower()

        if char in keyboard_characters:
            index = keyboard_characters.index(char)
            shifted_char = key[index]
            encrypted_msg.append(shifted_char.upper() if is_upper else shifted_char)
        else:
            encrypted_msg.append(i)

    output = "".join(encrypted_msg)
    print('\nThe encrypted message is: ' + output)
    print(f'Key generated: {key}\n')

def substitution_decoder():
    key = input('Enter the 26-letter key generated during encoding: ').lower().strip()

    if len(key) != 26 or set(key) != set(keyboard_characters):
        print('Invalid key!')
        return

    message = input('Enter the encrypted message: ')
    decrypted_msg = []

    for i in message:
        is_upper = i.isupper()
        char = i.lower()

        if char in key:
            index = key.index(char)
            shifted_char = keyboard_characters[index]
            decrypted_msg.append(shifted_char.upper() if is_upper else shifted_char)
        else:
            decrypted_msg.append(i)

    output = "".join(decrypted_msg)
    print('The decrypted message is: ' + output)

def otp_encoder():
    message = input('Enter the message to be encrypted: ')
    if not message:
        return

    key = [random.randint(0, 255) for _ in range(len(message))]
    encrypted_bytes = []

    for i in range(len(message)):
        char_code = ord(message[i])
        encrypted_bytes.append(char_code ^ key[i])

    msg_str = " ".join(str(b) for b in encrypted_bytes)
    key_str = " ".join(str(k) for k in key)

    print('\nThe encrypted message (numbers): ' + msg_str)
    print(f'Key generated (numbers): {key_str}\n')

def otp_decoder():
    key_input = input('Enter the number key (space-separated): ').strip()
    msg_input = input('Enter the encrypted message (space-separated numbers): ').strip()

    try:
        key = [int(x) for x in key_input.split()]
        encrypted_bytes = [int(x) for x in msg_input.split()]
    except ValueError:
        print('Invalid numbers provided!')
        return

    if len(key) != len(encrypted_bytes):
        print('Key length must match message length!')
        return

    decrypted_chars = []
    for i in range(len(encrypted_bytes)):
        decrypted_chars.append(chr(encrypted_bytes[i] ^ key[i]))

    output = "".join(decrypted_chars)
    print('The decrypted message is: ' + output)

print_banner()

while True:
    print('┌─────────────────────────────────────────────────────────┐')
    print('│                       MAIN MENU                         │')
    print('├─────────────────────────────────────────────────────────┤')
    print('│  [1] Caesar Cipher         --> Encode                   │')
    print('│  [2] Caesar Cipher         --> Decode                   │')
    print('│  [3] Substitution Cipher   --> Encode                   │')
    print('│  [4] Substitution Cipher   --> Decode                   │')
    print('│  [5] XOR One-Time Pad      --> Encode                   │')
    print('│  [6] XOR One-Time Pad      --> Decode                   │')
    print('│  [0] Exit                                               │')
    print('└─────────────────────────────────────────────────────────┘')
    res = input('Select an option (0-6): ').strip()

    if res == '1':
        caesar_encoder()
    elif res == '2':
        caesar_decoder()
    elif res == '3':
        substitution_encoder()
    elif res == '4':
        substitution_decoder()
    elif res == '5':
        otp_encoder()
    elif res == '6':
        otp_decoder()
    elif res == '0':
        print('\nThanks for using TryCrypt. Goodbye!')
        break
    else:
        print('\nInvalid choice! Please choose an option from 0 to 6.')