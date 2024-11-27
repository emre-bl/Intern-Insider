import streamlit as st
from datetime import datetime

lang_dict = {
    'en': {
        "filter_section_title": "Filter Reviews",
        "company_filter": "Company",
        "rating_filter": "Rating",
        "all_companies": "All Companies",
        "all_ratings": "All Ratings",
        "all_departments": "All Departments",
        "department_filter": "Department",
        "role_filter": "Internship Role",
        "sort_option_label": "Sort Reviews",
        "sort_options": ["Most Liked", "Newest First", "Oldest First"],
        "rating_label": "Rating",
        "department_label": "Department",
        "role_label": "Role",
        "review_label": "Review",
        "salary_label": "Salary",
        "project_rating_label": "Project Rating",
        "feedback_date_label": "Feedback Date",
        "helpful_button": "👍 Helpful",
        "no_reviews_found": "No reviews found."
    },
    'tr': {
        "filter_section_title": "Değerlendirmeleri Filtrele",
        "company_filter": "Şirket",
        "rating_filter": "Puan",
        "all_companies": "Tüm Şirketler",
        "all_ratings": "Tüm Puanlar",
        "all_departments": "Tüm Departmanlar",
        "department_filter": "Departman",
        "role_filter": "Staj Pozisyonu",
        "sort_option_label": "Değerlendirmeleri Sırala",
        "sort_options": ["En Beğenilen", "En Yeni", "En Eski"],
        "rating_label": "Puan",
        "department_label": "Departman",
        "role_label": "Pozisyon",
        "review_label": "Değerlendirme",
        "salary_label": "Maaş",
        "project_rating_label": "Proje Puanı",
        "feedback_date_label": "Geri Bildirim Tarihi",
        "helpful_button": "👍 Faydalı",
        "no_reviews_found": "Hiç değerlendirme bulunamadı."
    }
}

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
