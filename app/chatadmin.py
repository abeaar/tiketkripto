import os
import streamlit as st
from database.db_connection import get_db_connection
from dotenv import load_dotenv
from utils.chatutils import fetch_chats, save_chat

# Load environment variables
load_dotenv()
vigenere_key = os.getenv("VIGENERE_KEY")
aes_password = os.getenv("AES_PASSWORD")

def chatadmin():
    st.title("Chat dengan Admin")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user messages
    user_id = st.session_state.get("user_id", None)  # Ensure session_state contains the user_id
    if user_id is None:
        st.warning("Please log in to access the chat.")
        return

    # Fetch chats based on the session state
    chats = fetch_chats(cursor, user_id, aes_password, vigenere_key)

    # Display chats
    if chats:
        for chat in chats:
            if chat["sender_role"] == 'user':
                st.write(f"🟢 **You ({chat['timestamp']}):** {chat['message']}")
            else:
                st.write(f"🔵 **Admin ({chat['timestamp']}):** {chat['message']}")
    else:
        st.info("No messages yet.")

    # Check if there's a new message sent (using session state)
    if 'message_sent' in st.session_state and st.session_state.message_sent:
        st.session_state.message_sent = False  # Reset the flag
        st.success("Message sent successfully!")

    # Form to send message
    with st.form("send_message_form"):
        user_message = st.text_area("Message:", placeholder="Type your message to admin...")
        submit_message = st.form_submit_button("Send")

        if submit_message:
            if user_message.strip():
                # Save chat to database
                save_chat(
                    cursor, conn,
                    sender_id=user_id, sender_role='user',
                    receiver_id=2, receiver_role='admin',
                    message=user_message,
                    aes_password=aes_password, vigenere_key=vigenere_key
                )
                # Mark message as sent in session state
                st.session_state.message_sent = True
                st.session_state.user_message = user_message  # Store the message for display purpose
                conn.commit()  # Commit the transaction
                
                # Use session state flag to trigger UI update
                st.session_state.new_message = True  # This will act as a trigger for the re-render

    conn.close()

