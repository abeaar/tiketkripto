import mysql.connector
from database.db_connection import get_db_connection


def get_available_events():
    """ Fungsi untuk mengambil daftar acara yang tersedia dari database """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Ambil data acara yang masih memiliki tiket tersedia
    cursor.execute("SELECT event_id, event_name, event_date, description, available_tickets, ticket_price FROM event WHERE available_tickets > 0")
    events = cursor.fetchall()
    conn.close()

    # Konversi hasil query ke format yang lebih mudah digunakan
    return [{
        'event_id': event[0], 
        'event_name': event[1], 
        'event_date': event[2], 
        'description': event[3], 
        'available_tickets': event[4], 
        'ticket_price': event[5]
    } for event in events]

def update_ticket_availability(event_id, tickets_ordered):
    """ Update jumlah tiket yang tersedia setelah pemesanan """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update jumlah tiket yang tersedia di database
    cursor.execute(
        "UPDATE event SET available_tickets = available_tickets - %s WHERE event_id = %s AND available_tickets >= %s",
        (tickets_ordered, event_id, tickets_ordered)
    )
    conn.commit()

    return cursor.rowcount > 0

def insert_ticket_order(user_id, event_id, tickets_ordered):
    """ Menambahkan pesanan ke tabel ticket """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO ticket (user_id, event_id, tickets_ordered, order_date) VALUES (%s, %s, %s, NOW())",
        (user_id, event_id, tickets_ordered)
    )
    conn.commit()
    conn.close()


