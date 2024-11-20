import streamlit as st
from database.db_connection import get_db_connection
from utils.authentication import encrypt_password


def regist():
    st.title("Register New Account")
    
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    role = "user"  # Set default role to 'user'

    if st.button("Register"):
        if username and email and password:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if username or email already exists
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            existing_user = cursor.fetchone()

            if existing_user:
                st.error("Username or Email already exists. Please choose another.")
            else:
                # Encrypt the password before saving to database
                password_hash = encrypt_password(password)
                
                # Insert the new user into the database
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, role)
                    VALUES (%s, %s, %s, %s)
                """, (username, email, password_hash, role))

                conn.commit()
                cursor.close()
                conn.close()
                
                # Update session state to redirect to login page
                st.session_state.page = "login"  # Set the page to "login" after registration
                st.session_state.logged_in = False  # Make sure the user is logged out initiallyama
                st.session_state.username = None  # Clear the username session
                st.success("Registration successful! You can now log in.")
                
        else:
            st.error("Please fill in all fields.")

# This can be used in the main app for registration logic
if __name__ == "__main__":
    regist()
