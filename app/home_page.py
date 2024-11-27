import streamlit as st
from backend.db_connection import connect_to_collection
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
    """Render quick filter section similar to reviews_page filters."""
    text = lang_dict[st.session_state["language"]]
    st.markdown(f"### {text['filter_title']}")

    with st.form("quick_filter"):
        col1, col2, col3 = st.columns(3)

        with col1:
            company = st.text_input(text["company_filter"], key="quick_company_filter")

        with col2:
            department = st.text_input(text["department_filter"], key="quick_department_filter")

        with col3:
            rating = st.selectbox(
                text["filter_rating"],
                options=[text["all_ratings"]] + [5, 4, 3, 2, 1],
                key="quick_rating_filter"
            )

        submitted = st.form_submit_button(text["search_button"])
        if submitted:
            # Store filters in session state
            st.session_state["reviews_filters"] = {
                "company_filter": company,
                "department_filter": department,
                "rating_filter": rating
            }
            # Redirect to reviews page
            st.session_state["page"] = "reviews"
            st.experimental_rerun()

def render_popular_reviews():
    """Render the most liked reviews section with data fetched from the database."""
    text = lang_dict[st.session_state["language"]]
    st.markdown(f"### {text['popular_reviews']}")

    # Connect to the reviews collection
    reviews_collection = connect_to_collection('reviews')
    if reviews_collection is None:
        st.error("Could not connect to the database.")
        return

    # Fetch the top three most liked reviews
    top_reviews = list(
        reviews_collection.find({"admin_approved": True})
        .sort("like_count", -1)  # Sort by like_count in descending order
        .limit(3)  # Limit to the top 3 reviews
    )

    if not top_reviews:  # Handle case with no approved reviews
        st.info(text["no_reviews_available"])  # Add this key to lang_dict
        return

    # Render each review
    for review in top_reviews:
        with st.container():
            st.markdown(f"""
                <div class="review-card">
                    <h4>{review['company_name']} - ⭐ {review['rating']}</h4>
                    <p><em>{review['department']}</em></p>
                    <p>{review['review_text']}</p>
                    <small>{review['feedback_date']} | {text['likes']}: {review.get('like_count', 0)}</small>
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
