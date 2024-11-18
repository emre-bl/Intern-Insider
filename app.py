import streamlit as st
import pandas as pd
from datetime import datetime

TRANSLATIONS = {
    "en": {
        "nav_companies": "Companies",
        "nav_reviews": "Reviews",
        "nav_admin": "Admin Login",
        "nav_logout": "Logout",
        "nav_admin_panel": "Admin Panel",
        "submit_review": "Submit Review",
        "hero_title": "Find Your Perfect Internship",
        "hero_subtitle": "Read real experiences from former interns and make informed decisions about your future internship.",
        "filter_title": "Quick Search",
        "filter_company": "Company Name",
        "filter_department": "Department",
        "filter_rating": "Minimum Rating",
        "popular_reviews": "Popular Reviews",
        "search_button": "Search",
    },
    "tr": {
        "nav_companies": "Şirketler",
        "nav_reviews": "Değerlendirmeler",
        "nav_admin": "Admin Girişi",
        "nav_logout": "Çıkış Yap",
        "nav_admin_panel": "Admin Panel",
        "submit_review": "Şirket Değerlendir",
        "hero_title": "Hayalindeki Stajı Bul",
        "hero_subtitle": "Eski stajyerlerin gerçek deneyimlerini oku ve gelecekteki stajın hakkında bilinçli kararlar al.",
        "filter_title": "Hızlı Arama",
        "filter_company": "Şirket Adı",
        "filter_department": "Departman",
        "filter_rating": "Minimum Puan",
        "popular_reviews": "Popüler Değerlendirmeler",
        "search_button": "Ara",
    }
}

def init_session_state():
    """Initialize session state variables"""
    if 'language' not in st.session_state:
        st.session_state.language = 'tr'
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False  # Varsayılan olarak admin giriş yapılmamış

def get_text(key: str) -> str:
    """Get translated text based on current language"""
    return TRANSLATIONS[st.session_state.language][key]

def apply_custom_css():
    """Apply custom CSS styles"""
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
            margin-bottom: 2rem;
        }
        .hero-section {
            text-align: center;
            padding: 4rem 2rem;
            background-color: #f8f9fa;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .filter-section {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .popular-reviews {
            margin-top: 2rem;
        }
        .review-card {
            padding: 1rem;
            border: 1px solid #eee;
            border-radius: 5px;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

def render_navbar():
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 2])
    
    with col1:
        st.image("assets/intern-insider-compact-logo.svg", width=100)
    
    with col2:
        st.button(get_text("nav_reviews"), key="reviews_btn")

    # Şirket Değerlendir butonu
    with col3:
        if st.button(get_text("submit_review"), key="submit_review_btn"):
            st.session_state.page = "submit_review"
            st.experimental_rerun()
    
    # Dil değiştirme
    with col4:
        if st.button("🌐 TR/EN", key="lang_toggle"):
            st.session_state.language = 'en' if st.session_state.language == 'tr' else 'tr'
            st.experimental_rerun()

    # Admin girişi/çıkış işlemleri
    with col5:
        if st.session_state.get("is_admin"):
            if st.button(get_text("nav_logout"), key="logout_btn"):
                st.session_state.is_admin = False
                st.experimental_rerun()
        else:
            if st.button(get_text("nav_admin"), key="admin_btn"):
                st.session_state.page = "admin_login"
                st.experimental_rerun()
    
    with col6:
        if st.session_state.get("is_admin"):
            if st.button(get_text("nav_admin_panel"), key="admin_panel_btn"):
                st.session_state.page = "admin_panel"
                st.experimental_rerun()


def render_logo():
    """Render the logo at the top of the app"""
    st.image("assets/intern-insider-logo.png")

def render_hero_section():
    """Render hero section"""
    st.markdown(f"""
        <div class="hero-section" style="background-color: #f0f4f8;">
            <h1 style="color: #ff8c00;">{get_text('hero_title')}</h1>  <!-- Soft turuncu -->
            <p style="color: #005f73;">{get_text('hero_subtitle')}</p>  <!-- Lacivert ile uyumlu soft mavi -->
        </div>
    """, unsafe_allow_html=True)


def render_quick_filter():
    """Render quick filter section"""
    st.markdown(f"### {get_text('filter_title')}")
    
    with st.form("quick_filter"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            company = st.text_input(get_text("filter_company"))
        
        with col2:
            departments = ["Computer Engineering", "Industrial Engineering", "Mechanical Engineering"]
            department = st.selectbox(get_text("filter_department"), departments)
        
        with col3:
            rating = st.slider(get_text("filter_rating"), 1, 5, 3)
        
        submitted = st.form_submit_button(get_text("search_button"))
        if submitted:
            # Handle filter submission
            pass

def render_popular_reviews():
    """Render popular reviews section"""
    st.markdown(f"### {get_text('popular_reviews')}")
    
    # Sample reviews data - In production, Database'den çekilecek
    sample_reviews = [
        {
            "company": "Tech Corp",
            "rating": 4.5,
            "department": "Computer Engineering",
            "review": "Great learning experience with modern technologies...",
            "date": "2024-03-15"
        },
        {
            "company": "Industry Ltd",
            "rating": 4.8,
            "department": "Industrial Engineering",
            "review": "Excellent mentorship program and hands-on projects...",
            "date": "2024-03-10"
        }
    ]
    
    for review in sample_reviews:
        with st.container():
            st.markdown(f"""
                <div class="review-card">
                    <h4>{review['company']} - ⭐ {review['rating']}</h4>
                    <p><em>{review['department']}</em></p>
                    <p>{review['review']}</p>
                    <small>{review['date']}</small>
                </div>
            """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Intern Insider",
        page_icon="👩‍💻",
        layout="wide"
    )

    if "page" not in st.session_state:
        st.session_state["page"] = "home"

    if st.session_state["page"] == "admin_login":
        from admin_login import admin_login
        admin_login()
    elif st.session_state["page"] == "submit_review":
        from submit_review_page import submit_review
        submit_review()
    elif st.session_state["page"] == "admin_panel":
        from admin_panel import admin_panel
        admin_panel()
    else:
        init_session_state()
        apply_custom_css()
        render_logo()
        render_navbar()
        render_hero_section()
        render_quick_filter()
        render_popular_reviews()

if __name__ == "__main__":
    main()
