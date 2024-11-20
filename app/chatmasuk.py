import os

import streamlit as st
from database.db_connection import get_db_connection
from dotenv import load_dotenv
from utils.chatutils import fetch_chats, save_chat

# Load environment variables
load_dotenv()
vigenere_key = os.getenv("VIGENERE_KEY")
aes_password = os.getenv("AES_PASSWORD")


def chatmasuk():
    st.title("Chat dengan User")

    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all users for sidebar
    cursor.execute("""
        SELECT DISTINCT sender_id 
        FROM chat 
        WHERE receiver_role = 'admin'
    """)
    users = [row[0] for row in cursor.fetchall()]

    # Sidebar for selecting user
    st.sidebar.title("Select User to Chat")
    selected_user_id = st.sidebar.selectbox("User ID", users, format_func=lambda x: f"User {x}")

    if not selected_user_id:
        st.info("No user selected. Please select a user to view the chat.")
        conn.close()
        return

    # Fetch chats with selected user
    chats = fetch_chats(cursor, user_id=selected_user_id, aes_password=aes_password, vigenere_key=vigenere_key)

    # Display chat history
    st.subheader(f"Chat with User {selected_user_id}")
    if chats:
        for chat in chats:
            if chat["sender_role"] == "user":
                st.write(f"🟢 **User ({chat['timestamp']}):** {chat['message']}")
            else:
                st.write(f"🔵 **Admin ({chat['timestamp']}):** {chat['message']}")
    else:
        st.info("No messages yet with this user.")

    # Form to send a message
    with st.form("send_message_form"):
        admin_message = st.text_area("Message:", placeholder="Type your message to the user...")
        submit_message = st.form_submit_button("Send")

        if submit_message and admin_message.strip():
            # Save chat to database
            save_chat(
                cursor, conn,
                sender_id=st.session_state.get("user_id", None),  # Assume admin ID is in session state
                sender_role="admin",
                receiver_id=selected_user_id,
                receiver_role="user",
                message=admin_message,
                aes_password=aes_password, vigenere_key=vigenere_key
            )
            conn.commit()  # Commit the transaction
            st.success("Message sent successfully!")
            
            # Set session state to refresh the page (using session state as trigger)
            st.session_state['message_sent'] = True

            # Refresh the chat display based on session state change
            st.session_state['message_sent'] = False  # Reset the flag

    conn.close()
