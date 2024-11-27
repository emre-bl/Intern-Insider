import streamlit as st
from datetime import datetime

def initialize_session_state():
    """
    Initialize default session state variables for the app.
    """
    # General session variables
    if 'language' not in st.session_state:
        st.session_state['language'] = 'en'  # Default language
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'  # Default to home page
    if 'is_admin' not in st.session_state:
        st.session_state['is_admin'] = False  # Default to not logged in

    # Admin-specific session variables
    if 'current_review_index' not in st.session_state:
        st.session_state['current_review_index'] = 0  # Index for pending reviews
    if 'pending_reviews' not in st.session_state:
        st.session_state['pending_reviews'] = []  # List of reviews to approve/reject
    if 'companies' not in st.session_state:
        st.session_state['companies'] = []  # List of companies for admin management
    if 'last_refresh' not in st.session_state:
        st.session_state['last_refresh'] = datetime.now()  # Timestamp for caching
