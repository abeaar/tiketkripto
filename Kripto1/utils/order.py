from database.db_connection import get_db_connection
from utils.encryption import super_encrypt  # Import fungsi enkripsi

def insert_ticket(user_id, event_id, tickets_ordered):
    try:

        encrypted_user_id, encrypted_event_id = super_encrypt(user_id, event_id)
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query untuk memasukkan data ke tabel 'ticket'
        cursor.execute(
            "INSERT INTO ticket (user_id, event_id, tickets_ordered, order_date) VALUES (%s, %s, %s, NOW())",
             (encrypted_user_id, encrypted_event_id, tickets_ordered)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error inserting ticket: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

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