import streamlit as st
from backend.db_connection import connect_to_collection
from app.utils import initialize_session_state

def admin_login():
    initialize_session_state()  # Ensure session state is ready

    # Check if admin is already logged in
    if st.session_state["is_admin"]:
        st.success("Admin halihazırda giriş yapmış!")
        return  # Prevent showing the login form

    # Login form
    st.title("Admin Girişi")

    # User login credentials
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    
    if st.button("Giriş Yap"):
        try:
            # Connect to the admin collection
            admin_collection = connect_to_collection("admin")
            if admin_collection is None:
                st.error("Veri tabanına bağlanılamadı. Lütfen daha sonra tekrar deneyin.")
                return

            # Verify user credentials
            admin_user = admin_collection.find_one({"admin_id": username, "password": password})
            if admin_user:
                st.success("Giriş başarılı!")
                st.session_state["is_admin"] = True
                st.session_state["page"] = "home"  # Redirect to home page after successful login
                st.experimental_rerun()
            else:
                st.error("Geçersiz kullanıcı adı veya şifre.")
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

    # Option to return to the home page
    if st.button("Ana Sayfaya Geri Dön"):
        st.session_state["page"] = "home"
        st.experimental_rerun()

if __name__ == "__main__":
    admin_login()
