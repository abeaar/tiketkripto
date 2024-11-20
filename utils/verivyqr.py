from utils.steganography import extract_hidden_data_from_qr
import streamlit as st

def verifyqr_code():
    st.title("Verify QR Code")
    uploaded_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        try:
            # Ekstrak data tersembunyi
            hidden_data = extract_hidden_data_from_qr(uploaded_file)
            if hidden_data:
                st.success("QR Code Verified!")
                st.write(f"Hidden Data: {hidden_data}")
            else:
                st.error("No hidden data found in QR Code!")
        except Exception as e:
            st.error(f"Failed to verify QR Code: {e}")
