def caesar_cipher_encrypt(value, shift=15):
    """
    Fungsi untuk mengenkripsi angka menggunakan Caesar Cipher dengan shift tertentu.
    """
    return (value + shift) % 256  # Menggunakan modulus untuk memastikan angka tetap dalam rentang yang valid

def xor_encrypt(value, key=15):
    """
    Fungsi untuk mengenkripsi angka menggunakan XOR dengan kunci tertentu.
    """
    return value ^ key

def super_encrypt(user_id, event_id, caesar_shift=15, xor_key=15):
    """
    Fungsi untuk mengenkripsi user_id dan event_id menggunakan kombinasi Caesar Cipher dan XOR.
    """
    # Enkripsi user_id dan event_id dengan Caesar Cipher terlebih dahulu
    encrypted_user_id = caesar_cipher_encrypt(user_id, caesar_shift)
    encrypted_event_id = caesar_cipher_encrypt(event_id, caesar_shift)

    # Enkripsi hasil Caesar Cipher dengan XOR
    encrypted_user_id = xor_encrypt(encrypted_user_id, xor_key)
    encrypted_event_id = xor_encrypt(encrypted_event_id, xor_key)

    return encrypted_user_id, encrypted_event_id

def super_decrypt(encrypted_user_id, encrypted_event_id, caesar_shift=15, xor_key=15):
    try:
        # Pastikan encrypted_user_id dan encrypted_event_id adalah integer
        encrypted_user_id = int(encrypted_user_id)
        encrypted_event_id = int(encrypted_event_id)
        
        # Pertama, dekripsi dengan XOR
        decrypted_user_id = xor_encrypt(encrypted_user_id, xor_key)
        decrypted_event_id = xor_encrypt(encrypted_event_id, xor_key)

        # Kemudian, dekripsi dengan Caesar Cipher
        decrypted_user_id = (decrypted_user_id - caesar_shift) % 256
        decrypted_event_id = (decrypted_event_id - caesar_shift) % 256

        return decrypted_user_id, decrypted_event_id
    except Exception as e:
        raise ValueError(f"Failed to decrypt: {e}")
