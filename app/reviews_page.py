import streamlit as st
from backend.db_connection import connect_to_collection
from backend.queries import build_reviews_query, sort_reviews
from app.components.filters import render_filter_section
from app.components.review_display import display_reviews
from app.utils import initialize_session_state, lang_dict

def reviews_page():
    """
    Main reviews page rendering function.
    """
    initialize_session_state()
    text = lang_dict[st.session_state["language"]]

    # Page title, Home button, and Language toggle
    col1, col2, col3 = st.columns([8, 1, 1])

    with col2:
        # Home button
        if st.button(text["home_button"]):
            st.session_state["page"] = "home"
            st.experimental_rerun()

    with col3:
        # Language toggle button
        if st.button("🌐 TR/EN"):
            st.session_state["language"] = "en" if st.session_state["language"] == "tr" else "tr"
            st.experimental_rerun()

    # Page title
    st.markdown(f"# {text['reviews_page_title']}")

    # Database connections
    reviews_collection = connect_to_collection('reviews')
    companies_collection = connect_to_collection('company')
    
    if reviews_collection is None or companies_collection is None:
        st.error("Database connection failed.")
        return

    # Pre-fill filters from session state if available
    quick_filters = st.session_state.get("reviews_filters", {})
    
    filters = render_filter_section(
        companies_collection,
        reviews_collection,
        pre_filled_filters=quick_filters
    )

    # Build query
    query = build_reviews_query(
        company_filter=filters['company_filter'],
        rating_filter=filters['rating_filter'],
        department_filter=filters['department_filter'],
        internship_role_filter=filters['internship_role_filter']
    )

    # Fetch and sort reviews
    reviews = list(reviews_collection.find(query))
    sorted_reviews = sort_reviews(reviews, filters['sort_option'])

    # Display reviews
    display_reviews(sorted_reviews, reviews_collection)

if __name__ == "__main__":
    reviews_page()
