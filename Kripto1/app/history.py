import streamlit as st
from database.db_connection import get_db_connection
from utils.encryption import super_encrypt, super_decrypt  # Import fungsi enkripsi yang sesuai

def history():
    """
    Halaman untuk menampilkan riwayat pesanan berdasarkan tabel ticket.
    """
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.title("Order History")
        user_id = st.session_state.user_id

        # Mengenkripsi user_id untuk mencocokkannya dengan yang ada di database
        encrypted_user_id = super_encrypt(user_id, event_id=0)[0]  # Asumsi event_id=0 sebagai placeholder
        
        conn = get_db_connection()
        cursor = conn.cursor()

        # Ambil data riwayat pesanan untuk user_id yang sudah dienkripsi
        query = """
            SELECT ticket_id, user_id, event_id, tickets_ordered, order_date
            FROM ticket
            WHERE user_id = %s
            ORDER BY order_date DESC
        """
        cursor.execute(query, (encrypted_user_id,))
        orders = cursor.fetchall()
        conn.close()

        if orders:
            st.subheader("Your Orders")
            for order in orders:
                order_id, encrypted_user_id, encrypted_event_id, tickets_ordered, order_date = order

                try:
                    # Dekripsi user_id dan event_id setelah diambil dari database
                    decrypted_user_id, decrypted_event_id = super_decrypt(encrypted_user_id, encrypted_event_id)

                    # Menampilkan data pesanan setelah didekripsi
                    st.write(f"**Order ID:** {order_id}")
                    st.write(f"**Tickets Ordered:** {tickets_ordered}")
                    st.write(f"**Order Date:** {order_date}")
                    # Jika perlu, tampilkan user_id dan event_id yang sudah didekripsi
                    st.write(f"**Decrypted User ID:** {decrypted_user_id}")
                    st.write(f"**Decrypted Event ID:** {decrypted_event_id}")
                    st.markdown("---")
                except Exception as e:
                    st.error(f"Failed to decrypt order with Order ID: {order_id}. Error: {e}")
        else:
            st.info("You have no order history.")
    else:
        st.warning("Please log in to view your order history.")
