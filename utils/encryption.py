import base64
from hashlib import pbkdf2_hmac
from Crypto.Cipher import AES


# Fungsi Vigenere
def vigenere_encrypt(text, key):
    encrypted_text = []
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)].lower()) - ord('a')
            if char.islower():
                encrypted_text.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            elif char.isupper():
                encrypted_text.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            key_index += 1
        else:
            encrypted_text.append(char)
    return ''.join(encrypted_text)

def vigenere_decrypt(text, key):
    decrypted_text = []
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)].lower()) - ord('a')
            if char.islower():
                decrypted_text.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            elif char.isupper():
                decrypted_text.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            key_index += 1
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)

# Fungsi AES dengan nonce statis di dalam fungsi
def aes_encrypt(plain_text, password):
    key = derive_key(password)
    nonce = b'\x00' * 16  # Nonce statis didefinisikan di dalam fungsi
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode())
    return base64.b64encode(tag + ciphertext).decode()

def aes_decrypt(encrypted_text, password):
    key = derive_key(password)
    nonce = b'\x00' * 16  # Nonce statis didefinisikan di dalam fungsi
    data = base64.b64decode(encrypted_text)
    tag, ciphertext = data[:16], data[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

# Super Encrypt dan Decrypt dengan nonce dikelola internal
def super_encrypt(data, vigenere_key, aes_password):
    # Langkah 1: Enkripsi menggunakan Vigenere Cipher
    vigenere_encrypted = vigenere_encrypt(data, vigenere_key)
    # Langkah 2: Enkripsi hasil Vigenere menggunakan AES
    aes_encrypted = aes_encrypt(vigenere_encrypted, aes_password)
    return aes_encrypted

def super_decrypt(encrypted_data, vigenere_key, aes_password):
    # Langkah 1: Dekripsi menggunakan AES
    aes_decrypted = aes_decrypt(encrypted_data, aes_password)
    # Langkah 2: Dekripsi hasil AES menggunakan Vigenere Cipher
    vigenere_decrypted = vigenere_decrypt(aes_decrypted, vigenere_key)
    return vigenere_decrypted

def derive_key(password):
    return pbkdf2_hmac('sha256', password.encode(), b'', 1)
