import os

import streamlit as st
from database.db_connection import get_db_connection
from utils.encryption import super_decrypt, super_encrypt


def fetch_order_history(user_id):
    """
    Fungsi untuk mengambil data riwayat pesanan berdasarkan user_id.
    """
    # Ambil kunci enkripsi dari environment variables
    vigenere_key = os.getenv("VIGENERE_KEY")  # Kunci untuk Vigenere
    aes_password = os.getenv("AES_PASSWORD")  # Password untuk AES

    # Pastikan user_id adalah string sebelum dienkripsi
    user_id_str = str(user_id)

    # Mengenkripsi user_id untuk mencari data yang sesuai di database
    encrypted_user_id = super_encrypt(user_id_str, vigenere_key, aes_password)
    
    try:
        # Membuka koneksi database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query untuk mengambil data pesanan berdasarkan encrypted user_id
        query = """
            SELECT ticket_id, user_id, event_id, tickets_ordered, order_date
            FROM ticket
            WHERE user_id = %s
            ORDER BY order_date DESC
        """
        cursor.execute(query, (encrypted_user_id,))
        orders = cursor.fetchall()

        # Menutup koneksi database
        cursor.close()
        conn.close()

        return orders
    except Exception as e:
        st.error(f"Failed to fetch order history: {e}")
        return []

def display_order(order):
    """
    Menampilkan detail pesanan yang telah didekripsi untuk user_id dan event_id.
    """
    order_id, encrypted_user_id, encrypted_event_id, tickets_ordered, order_date = order

    # Ambil kunci enkripsi untuk dekripsi
    vigenere_key = os.getenv("VIGENERE_KEY")
    aes_password = os.getenv("AES_PASSWORD")

    try:
        # Dekripsi user_id dan event_id
        decrypted_user_id = super_decrypt(encrypted_user_id, vigenere_key, aes_password)
        decrypted_event_id = super_decrypt(encrypted_event_id, vigenere_key, aes_password)

        # Menampilkan data pesanan setelah didekripsi
        st.write(f"**Order ID:** {order_id}")
        st.write(f"**Tickets Ordered:** {tickets_ordered}")
        st.write(f"**Order Date:** {order_date}")
        st.write(f"**Decrypted User ID:** {decrypted_user_id}")
        st.write(f"**Decrypted Event ID:** {decrypted_event_id}")
        st.markdown("---")
    except Exception as e:
        st.error(f"Failed to decrypt order with Order ID: {order_id}. Error: {e}")

def history():
    """
    Halaman untuk menampilkan riwayat pesanan berdasarkan tabel ticket.
    """
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.title("Order History")
        user_id = st.session_state.user_id

        # Mengambil riwayat pesanan berdasarkan user_id
        orders = fetch_order_history(user_id)

        if orders:
            st.subheader("Your Orders")
            for order in orders:
                display_order(order)
        else:
            st.info("You have no order history.")
    else:
        st.warning("Please log in to view your order history.")
