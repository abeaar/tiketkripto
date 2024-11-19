import streamlit as st
from database.db_connection import get_db_connection
from utils.authentication import verify_login


def login():
    st.title("Login")

    # Form input untuk username dan password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()  # Pastikan `cursor` dideklarasikan di sini

            # Verifikasi login dan dapatkan role
            role = verify_login(username, password, conn)

            if role:
                # Mendapatkan ID pengguna dari database
                cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
                user_id = cursor.fetchone()[0]

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.session_state.user_id = user_id  # Simpan user ID

                # Mengarahkan pengguna ke halaman berdasarkan role
                if role == "admin":
                    st.session_state.page = "dashboard_admin"  # Halaman admin
                elif role == "user":
                    st.session_state.page = "dashboard_user"  # Halaman user

                st.success("Login successful!")
            else:
                st.error("Invalid username or password.")

            cursor.close()  # Tutup cursor setelah selesai digunakan
            conn.close()    # Tutup koneksi database
        else:
            st.error("Database connection failed. Please try again later.")

# Ini bisa dipanggil di aplikasi utama untuk login
if __name__ == "__main__":
    login()
