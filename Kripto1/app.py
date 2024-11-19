import streamlit as st
from app.dashboard_user import dashboard_user
from app.dashboard_admin import dashboard_admin
from app.login import login
from app.regist import regist

# Mengecek status login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = "login"  # Default ke halaman login

# Navigasi berdasarkan halaman yang dipilih
if st.session_state.logged_in:
    if st.session_state.page == "dashboard_user":
        dashboard_user()  # Menampilkan halaman dashboard
    elif st.session_state.page == "dashboard_admin":
        dashboard_admin()  # Menampilkan halaman dashboard
else:
    if st.session_state.page == "login":
        login()  # Menampilkan halaman login
        
        # Teks Markdown untuk berpindah ke halaman registrasi dengan tombol
        if st.button("Belum punya akun? Register sekarang"):
            st.session_state.page = "register"

    elif st.session_state.page == "register":
        regist()  # Menampilkan halaman register
        
        # Teks Markdown untuk berpindah ke halaman login dengan tombol
        if st.button("Sudah punya akun? Login sekarang"):
            st.session_state.page = "login"

# Fungsi untuk mengatur halaman yang dipilih
def set_page(page_name):
    st.session_state.page = page_name
