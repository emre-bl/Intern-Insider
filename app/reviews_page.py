import streamlit as st
from backend.db_connection import connect_to_collection
from backend.queries import build_reviews_query, sort_reviews
from app.components.filters import render_filter_section
from app.components.review_display import display_reviews

def reviews_page():
    """
    Main reviews page rendering function
    """
    st.markdown("# Reviews")

    # Database connections
    reviews_collection = connect_to_collection('reviews')
    companies_collection = connect_to_collection('company')
    
    if reviews_collection is None or companies_collection is None:
        st.error("Database connection failed.")
        return

    # Render filters and get filter options
    filters = render_filter_section(companies_collection, reviews_collection)

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

