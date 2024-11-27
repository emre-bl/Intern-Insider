import streamlit as st
from backend.db_connection import connect_to_collection
from app.utils import initialize_session_state, lang_dict

def render_header():
    """Render the header with Home and Language Toggle buttons."""
    text = lang_dict[st.session_state["language"]]

    col1, col2, col3 = st.columns([8, 1, 1])
    with col1:
        st.markdown(f"### {text['admin_login_title']}")  # Admin Login Page Title
    with col2:
        if st.button(text["home_button"], key="return_home_btn"):
            st.session_state["page"] = "home"
            st.experimental_rerun()
    with col3:
        if st.button("🌐 TR/EN", key="lang_toggle"):
            st.session_state["language"] = 'tr' if st.session_state["language"] == 'en' else 'en'
            st.experimental_rerun()

def admin_login():
    """Admin login page with centralized language support."""
    initialize_session_state()  # Ensure session state is initialized
    text = lang_dict[st.session_state["language"]]

    # Check if admin is already logged in
    if st.session_state.get("is_admin"):
        st.success(text["already_logged_in"])
        return  # Prevent showing the login form

    # Render Header
    render_header()

    # User login form
    username = st.text_input(text["username_label"])
    password = st.text_input(text["password_label"], type="password")
    
    if st.button(text["login_button"]):
        try:
            # Connect to the admin collection
            admin_collection = connect_to_collection("admin")
            if admin_collection is None:
                st.error(text["db_connection_error"])
                return

            # Verify user credentials
            admin_user = admin_collection.find_one({"admin_id": username, "password": password})
            if admin_user:
                st.success(text["login_success"])
                st.session_state["is_admin"] = True
                st.session_state["page"] = "home"  # Redirect to home page
                st.experimental_rerun()
            else:
                st.error(text["login_failed"])
        except Exception as e:
            st.error(f"{text['unexpected_error']}: {e}")

if __name__ == "__main__":
    admin_login()
