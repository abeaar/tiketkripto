from database.db_connection import get_db_connection
from utils.encryption import super_encrypt  # 

def insert_ticket(user_id, event_id, tickets_ordered, vigenere_key, aes_password):
    try:
        # Ambil koneksi database
        conn = get_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor()

        # Enkripsi user_id dan event_id sebelum disimpan
        encrypted_user_id = super_encrypt(str(user_id), vigenere_key, aes_password)
        encrypted_event_id = super_encrypt(str(event_id), vigenere_key, aes_password)

        # Query untuk menyisipkan data tiket terenkripsi
        query = """
            INSERT INTO ticket (user_id, event_id, tickets_ordered, order_date)
            VALUES (%s, %s, %s, NOW())
        """
        values = (encrypted_user_id, encrypted_event_id, tickets_ordered)
        cursor.execute(query, values)

        # Dapatkan `ticket_id` dari record yang baru dimasukkan
        ticket_id = cursor.lastrowid

        # Commit perubahan
        conn.commit()

        # Tutup cursor dan koneksi
        cursor.close()
        conn.close()

        return ticket_id  # Kembalikan ID tiket
    except Error as e:
        print(f"Error while inserting ticket: {e}")
        return None



def reduce_available_tickets(event_id, tickets_ordered):
    """
    Mengurangi jumlah tiket yang tersedia di tabel 'event'.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update query untuk mengurangi jumlah tiket
        cursor.execute(
            "UPDATE event SET available_tickets = available_tickets - %s WHERE event_id = %s AND available_tickets >= %s",
            (tickets_ordered, event_id, tickets_ordered)
        )
        conn.commit()

        if cursor.rowcount == 0:
            # Jika tidak ada baris yang terpengaruh, berarti tiket tidak mencukupi
            return False
        return True
    except Exception as e:
        print(f"Error reducing tickets: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()