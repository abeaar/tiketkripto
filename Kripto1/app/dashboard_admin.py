import streamlit as st
from utils.decode_qrcode import decode_qr_code
from utils.stenography_decoder import decode_steg_image

def dashboard_admin():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.title(f"Welcome admin, {st.session_state.username}!")

        if st.button("Logout"):
            # Mengubah status logged_in dan username di session_state
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.page = "login"  # Redirect to the login page after logout
            st.success("Logged out successfully!")
        
        uploaded_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])

        if uploaded_file:
            # Simpan file yang di-upload
            with open("uploaded_qr.png", "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Dekripsi data QR Code
            qr_data = decode_qr_code("uploaded_qr.png")
            
            if qr_data:
                st.write(f"Decoded Data: {qr_data}")
            else:
                st.write("Failed to decode QR Code.")


    else:
        st.warning("Please log in to continue.")

# This can be used in the main app for dashboard
if __name__ == "__main__":
    dashboard_admin()