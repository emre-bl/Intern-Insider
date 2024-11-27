import streamlit as st
from app.utils import initialize_session_state, lang_dict  # Centralized utilities

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
        button[title="View fullscreen"]{
            visibility: hidden;
        }
        </style>
    """, unsafe_allow_html=True)

def render_navbar():
    """Render the navigation bar with centralized language support."""
    text = lang_dict[st.session_state["language"]]

    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 2])
    
    with col1:
        st.image("app/assets/intern-insider-compact-logo.svg", width=100)

    with col2:
        if st.button(text["nav_reviews"], key="reviews_btn"):
            st.session_state["page"] = "reviews"
            st.experimental_rerun()

    with col3:
        if st.button(text["submit_review"], key="submit_review_btn"):
            st.session_state["page"] = "submit_review"
            st.experimental_rerun()

    with col4:
        if st.button("🌐 TR/EN", key="lang_toggle"):
            st.session_state["language"] = "tr" if st.session_state["language"] == "en" else "en"
            st.experimental_rerun()

    with col5:
        if st.session_state.get("is_admin"):
            if st.button(text["nav_logout"], key="logout_btn"):
                st.session_state["is_admin"] = False
                st.experimental_rerun()
        else:
            if st.button(text["nav_admin"], key="admin_btn"):
                st.session_state["page"] = "admin_login"
                st.experimental_rerun()

    with col6:
        if st.session_state.get("is_admin"):
            if st.button(text["nav_admin_panel"], key="admin_panel_btn"):
                st.session_state["page"] = "admin_panel"
                st.experimental_rerun()

def render_logo():
    """Render the logo at the top of the app."""
    st.image("app/assets/intern-insider-logo.png")

def render_hero_section():
    """Render hero section with centralized language support."""
    text = lang_dict[st.session_state["language"]]
    st.markdown(f"""
        <div class="hero-section" style="background-color: #f0f4f8;">
            <h1 style="color: #ff8c00; font-size: 55px;">{text['hero_title']}</h1> <!-- Soft orange -->
            <p style="color: #005f73; font-size: 32px;">{text['hero_subtitle']}</p> <!-- Soft blue -->
        </div>
    """, unsafe_allow_html=True)

def render_quick_filter():
    """Render quick filter section with centralized language support."""
    text = lang_dict[st.session_state["language"]]
    st.markdown(f"### {text['filter_title']}")

    with st.form("quick_filter"):
        col1, col2, col3 = st.columns(3)

        with col1:
            company = st.text_input(text["filter_company"])

        with col2:
            departments = ["Computer Engineering", "Industrial Engineering", "Mechanical Engineering"]
            department = st.selectbox(text["filter_department"], departments)

        with col3:
            rating = st.slider(text["filter_rating"], 1, 5, 3)

        submitted = st.form_submit_button(text["search_button"])
        if submitted:
            # Handle filter submission logic
            st.info("Search submitted! (Filter logic to be implemented)")

def render_popular_reviews():
    """Render popular reviews section with centralized language support."""
    text = lang_dict[st.session_state["language"]]
    st.markdown(f"### {text['popular_reviews']}")

    # Sample reviews data - Replace with actual database queries in production
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

def home_page():
    """Home page rendering function."""
    initialize_session_state()  # Ensure session state is initialized
    text = lang_dict[st.session_state["language"]]

    st.set_page_config(
        page_title="Intern Insider",
        page_icon="👩‍💻",
        layout="wide"
    )

    if st.session_state["page"] == "admin_login":
        from app.admin_login import admin_login
        admin_login()
    elif st.session_state["page"] == "submit_review":
        from app.submit_review_page import submit_review
        submit_review()
    elif st.session_state["page"] == "admin_panel":
        from app.admin_panel import admin_panel
        admin_panel()
    elif st.session_state["page"] == "reviews":
        from app.reviews_page import reviews_page
        reviews_page()
    else:
        # Default to Home Page
        apply_custom_css()
        render_logo()
        render_navbar()
        render_hero_section()
        render_quick_filter()
        render_popular_reviews()

if __name__ == "__main__":
    home_page()
