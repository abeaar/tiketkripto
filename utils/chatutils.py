from utils.encryption import vigenere_encrypt, vigenere_decrypt, aes_encrypt, aes_decrypt

def fetch_chats(cursor, user_id, aes_password, vigenere_key):

    cursor.execute("""
        SELECT id, sender_id, sender_role, receiver_id, receiver_role, message, timestamp 
        FROM chat 
        WHERE sender_id = %s OR receiver_id = %s
        ORDER BY timestamp ASC
    """, (user_id, user_id))

    chats = cursor.fetchall()

    decrypted_chats = []
    for chat_id, sender_id, sender_role, receiver_id, receiver_role, encrypted_message, timestamp in chats:
        try:
            # Decrypt the message
            aes_decrypted = aes_decrypt(encrypted_message, aes_password)
            decrypted_message = vigenere_decrypt(aes_decrypted, vigenere_key)
        except Exception:
            decrypted_message = "Unable to decrypt message."
        
        decrypted_chats.append({
            "chat_id": chat_id,
            "sender_id": sender_id,
            "sender_role": sender_role,
            "receiver_id": receiver_id,
            "receiver_role": receiver_role,
            "message": decrypted_message,
            "timestamp": timestamp
        })
    return decrypted_chats

def save_chat(cursor, conn, sender_id, sender_role, receiver_id, receiver_role, message, aes_password, vigenere_key):
    """
    Encrypt and save a chat message to the database.
    """
    # Encrypt the message
    vigenere_encrypted = vigenere_encrypt(message, vigenere_key)
    aes_encrypted = aes_encrypt(vigenere_encrypted, aes_password)

    # Save to database
    cursor.execute("""
        INSERT INTO chat (sender_id, sender_role, receiver_id, receiver_role, message)
        VALUES (%s, %s, %s, %s, %s)
    """, (sender_id, sender_role, receiver_id, receiver_role, aes_encrypted))
    conn.commit()
