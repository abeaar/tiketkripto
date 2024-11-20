import hashlib
from cryptography.hazmat.primitives import hashes

# Fungsi untuk mengenkripsi password dengan SHA-256
def encrypt_password(password: str) -> str:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(password.encode('utf-8'))
    return digest.finalize().hex()

# Fungsi untuk memverifikasi login dan mengembalikan role pengguna
def verify_login(username: str, password: str, conn) -> str or None:
    cursor = conn.cursor()
    
    # Menyesuaikan query untuk mencocokkan username dan mengambil role
    cursor.execute("SELECT password_hash, role FROM users WHERE username = %s", (username,))
    user_data = cursor.fetchone()
    
    # Jika username ditemukan, periksa kecocokan password
    if user_data:
        stored_password_hash, role = user_data
        if encrypt_password(password) == stored_password_hash:
            return role  # Kembalikan role jika password cocok
    return None  # Login gagal
