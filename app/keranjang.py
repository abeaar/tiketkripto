import os

import streamlit as st
from utils.order import insert_ticket, reduce_available_tickets
from utils.qr_ticket import generate_ticket_qr
from dotenv import load_dotenv
from utils.steganography import encode_image

load_dotenv()
vigenere_key = os.getenv("VIGENERE_KEY")
aes_password = os.getenv("AES_PASSWORD")


def keranjang():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.title("Your Cart")

        # Inisialisasi keranjang jika belum ada
        st.session_state.cart = st.session_state.get('cart', [])

        if st.session_state.cart:
            # Tampilkan detail item dalam keranjang
            total_price, total_ticket = display_cart_details()

            # Tombol checkout atau clear cart
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Checkout"):
                    checkout_cart(total_ticket)
            with col2:
                if st.button("Clear Cart"):
                    clear_cart()
        else:
            st.info("Your cart is empty.")
    else:
        st.warning("Please log in to continue.")


def display_cart_details():
    """Menampilkan detail keranjang dan menghitung total harga & tiket."""
    total_price = 0
    total_ticket = 0

    for item in st.session_state.cart:
        st.write(f"Event: {item['event_name']} - Tickets: {item['tickets_ordered']}")
        total_price += item['ticket_price'] * item['tickets_ordered']
        total_ticket += item['tickets_ordered']

    st.write(f"**Total Price: ${total_price:.2f}**")
    return total_price, total_ticket


def clear_cart():
    """Mengosongkan keranjang."""
    st.session_state.cart = []
    st.success("Your cart has been cleared!")


def checkout_cart(total_ticket):
    """Proses checkout keranjang."""
    user_id = st.session_state.user_id
    success = True

    st.session_state.total_purchased_tickets = st.session_state.get('total_purchased_tickets', 0)

    # Gabungkan tiket berdasarkan event_id
    consolidated_tickets = consolidate_cart()

    # Buat folder QR Code jika belum ada
    qr_code_folder = "qrcodes"
    if not os.path.exists(qr_code_folder):
        os.makedirs(qr_code_folder)

    # Proses setiap event dalam keranjang
    for event_data in consolidated_tickets.values():
        if not process_event(event_data, user_id, qr_code_folder, vigenere_key, aes_password):
            success = False
            break

    # Update status berdasarkan hasil checkout
    finalize_checkout(success, total_ticket)



def consolidate_cart():
    """Menggabungkan item di keranjang berdasarkan event_id."""
    consolidated_tickets = {}
    for item in st.session_state.cart:
        event_id = item['event_id']
        if event_id not in consolidated_tickets:
            consolidated_tickets[event_id] = {
                'event_id': event_id,
                'event_name': item['event_name'],
                'tickets_ordered': item['tickets_ordered']
            }
        else:
            consolidated_tickets[event_id]['tickets_ordered'] += item['tickets_ordered']
    return consolidated_tickets


def process_event(event_data, user_id, qr_code_folder, vigenere_key, aes_password):
    """Proses untuk satu event: kurangi tiket, masukkan data, dan buat QR Code."""
    tickets_to_order = event_data['tickets_ordered']

    # Kurangi tiket di database
    if not reduce_available_tickets(event_data['event_id'], tickets_to_order):
        st.error(f"Gagal mengupdate tiket untuk {event_data['event_name']}. Tiket tidak mencukupi.")
        return False

    # Masukkan tiket ke database
    ticket_id = insert_ticket(user_id, event_data['event_id'], tickets_to_order, vigenere_key, aes_password)
    if not ticket_id:
        st.error(f"Gagal memasukkan tiket untuk {event_data['event_name']}. Membatalkan proses.")
        return False

    # Generate dan encode QR Code
    qr_image_path = os.path.join(qr_code_folder, f"qrcode_{ticket_id}.png")
    encoded_image_path = os.path.join(qr_code_folder, f"encoded_ticket_{ticket_id}.png")

    generate_ticket_qr(
        user_id, 
        event_data['event_name'], 
        event_data['tickets_ordered'], 
        ticket_id
    )

    data_to_encode = f"UserID:{user_id}|EventID:{event_data['event_id']}|Tickets:{event_data['tickets_ordered']}|TicketID:{ticket_id}"
    encode_image(qr_image_path, data_to_encode, encoded_image_path)

    # Tampilkan QR Code
    st.image(encoded_image_path, caption=f"Your Event Ticket QR Code - Ticket ID {ticket_id}")
    return True



def finalize_checkout(success, total_ticket):
    """Finalisasi proses checkout."""
    if success:
        st.session_state.total_purchased_tickets += total_ticket
        st.session_state.cart = []
        st.success(f"Pembelian berhasil! Anda telah membeli {total_ticket} tiket.")
        st.write(f"Total tiket yang telah Anda beli: {st.session_state.total_purchased_tickets}")
    else:
        st.error("Pembelian gagal. Silakan coba lagi.")
