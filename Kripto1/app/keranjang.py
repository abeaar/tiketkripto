import os
import streamlit as st
from utils.order import insert_ticket, reduce_available_tickets
from utils.qr_ticket import generate_ticket_qr
from utils.steganography import encode_image


def keranjang():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.title("Your Cart")

        # Cek apakah keranjang sudah ada
        if 'cart' not in st.session_state:
            st.session_state.cart = []
        
        if len(st.session_state.cart) > 0:
            total_price = 0
            total_ticket = 0

            # Tampilkan detail item dalam keranjang
            for item in st.session_state.cart:
                st.write(f"Event: {item['event_name']} - Tickets: {item['tickets_ordered']}")
                total_price += item['ticket_price'] * item['tickets_ordered']
                total_ticket += item['tickets_ordered']

            # Tampilkan total harga
            st.write(f"**Total Price: ${total_price:.2f}**")

            # Tombol untuk checkout atau clear cart
            if st.button("Checkout"):
                checkout_cart(total_ticket)
            if st.button("Clear Cart"):
                clear_cart()
        else:
            st.info("Your cart is empty.")
    else:
        st.warning("Please log in to continue.")

# Fungsi untuk mengosongkan keranjang
def clear_cart():
    st.session_state.cart = []
    st.success("Your cart has been cleared!")

# Fungsi untuk melakukan checkout
def checkout_cart(total_ticket):
    user_id = st.session_state.user_id
    success = True

    if 'total_purchased_tickets' not in st.session_state:
        st.session_state.total_purchased_tickets = 0

    # Gabungkan tiket dengan event_id yang sama
    consolidated_tickets = {}
    for item in st.session_state.cart:
        event_id = item['event_id']
        if event_id in consolidated_tickets:
            consolidated_tickets[event_id]['tickets_ordered'] += item['tickets_ordered']
        else:
            consolidated_tickets[event_id] = {
                'event_id': event_id,
                'event_name': item['event_name'],
                'tickets_ordered': item['tickets_ordered']
            }

    # Proses checkout untuk tiket yang sudah digabung
    for event_data in consolidated_tickets.values():
        tickets_to_order = event_data['tickets_ordered']

        # Kurangi jumlah tiket yang tersedia di database
        if not reduce_available_tickets(event_data['event_id'], tickets_to_order):
            st.error(f"Gagal mengupdate tiket yang tersedia untuk {event_data['event_name']}. Tiket tidak mencukupi.")
            success = False
            break

        # Masukkan data ke tabel 'ticket' dengan jumlah total tiket per event
        result = insert_ticket(user_id, event_data['event_id'], tickets_to_order)
        if not result:
            st.error(f"Gagal memasukkan tiket untuk {event_data['event_name']}. Membatalkan proses.")
            success = False
            break

    if success:
        # Generate QR Code untuk setiap event
        for event_data in consolidated_tickets.values():
            # Gunakan event_id dan user_id untuk membuat id_tiket unik
            id_tiket = f"{user_id}_{event_data['event_id']}"

            # Generate QR code dengan nama file sesuai dengan id_tiket
            qr_image_path = generate_ticket_qr(
                user_id, 
                event_data['event_name'], 
                event_data['tickets_ordered'],
                id_tiket
            )
            
            data_to_encode = f"UserID:{user_id}|EventID:{event_data['event_id']}|Tickets:{event_data['tickets_ordered']}"
            encoded_image_path = f"encoded_ticket_{id_tiket}.png"
            
            # Encode data dalam gambar QR
            encode_image(qr_image_path, data_to_encode, encoded_image_path)

            # Tentukan folder penyimpanan QR Code
            qr_code_folder = "qrcodes"
            if not os.path.exists(qr_code_folder):  # Pastikan folder ada
                os.makedirs(qr_code_folder)

            # Nama file QR code berdasarkan id_tiket
            qr_image_path = os.path.join(qr_code_folder, f"qrcode_{id_tiket}.png")
            st.image(qr_image_path, caption=f"Your Event Ticket QR Code - {id_tiket}")

        # Update total tiket yang sudah dibeli
        st.session_state.total_purchased_tickets += total_ticket
        st.session_state.cart = []  # Kosongkan keranjang jika berhasil
        st.success(f"Pembelian berhasil! Anda telah membeli {total_ticket} tiket.")
        st.write(f"Total tiket yang telah Anda beli: {st.session_state.total_purchased_tickets}")
    else:
        st.error("Pembelian gagal. Silakan coba lagi.")
