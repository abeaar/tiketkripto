import streamlit as st
from database.db_connection import get_db_connection


def dashboard_user():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        # Sidebar untuk navigasi
        page = st.sidebar.selectbox("Navigate", ["Dashboard", "Cart","History"])

        if page == "Dashboard":
            st.title(f"Welcome, {st.session_state.username}!")
            st.header("Upcoming Events")

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT event_id, event_name, event_date, description, available_tickets, ticket_price FROM event WHERE available_tickets > 0 ORDER BY event_date ASC")
            events = cursor.fetchall()
            conn.close()

            if events:
                for event_id, event_name, event_date, description, available_tickets, ticket_price in events:
                    st.subheader(event_name)
                    st.write(f"📅 **Date:** {event_date}")
                    st.write(f"📝 **Description:** {description}")
                    st.write(f"🎟 **Available Tickets:** {available_tickets}")
                    st.write(f"💰 **Ticket Price:** ${ticket_price:.2f}")

                    # Form untuk memesan tiket
                    with st.form(f"form_{event_id}"):
                        num_tickets = st.number_input(
                            f"Number of Tickets for {event_name}",
                            min_value=1,
                            max_value=available_tickets,
                            step=1,
                            key=f"num_tickets_{event_id}"
                        )
                        submit_button = st.form_submit_button("Order Tickets")
                        if submit_button:
                            if num_tickets > available_tickets:
                                st.error("Not enough tickets available!")
                            elif 'user_id' in st.session_state:
                                 order_ticket(event_id, event_name, num_tickets, ticket_price, st.session_state.user_id)
                            else:
                                st.error("User ID not found in session state.")
            else:
                st.info("No events with available tickets.")

            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.page = "login"
                st.success("Logged out successfully!")

        elif page == "Cart":
            from app.keranjang import keranjang
            keranjang()  # Pindah ke halaman keranjang

        elif page == "History":  # Tambahkan ini untuk memuat halaman History
            from app.history import history 
            history()
    else:
        st.warning("Please log in to continue.")

def order_ticket(event_id, event_name, num_tickets, ticket_price, user_id):
    """
    Menambahkan tiket ke keranjang dalam session state termasuk user_id.
    """
    if 'cart' not in st.session_state:
        st.session_state.cart = []  # Inisialisasi keranjang jika belum ada

    # Tambahkan pesanan ke session dengan user_id
    st.session_state.cart.append({
        'user_id': user_id,
        'event_id': event_id,
        'event_name': event_name,
        'tickets_ordered': num_tickets,
        'ticket_price': ticket_price
    })
    st.success(f"Added {num_tickets} tickets for {event_name} to your cart!")


# Ini bisa dipanggil di aplikasi utama
if __name__ == "__main__":
    dashboard_user()
