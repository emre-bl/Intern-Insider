import streamlit as st
from app.utils import lang_dict  # Centralized language dictionary

def display_reviews(reviews, reviews_collection):
    """
    Display reviews with like functionality and centralized language support.
    """
    text = lang_dict[st.session_state['language']]  # Select language-specific text

    if reviews:
        for review in reviews:
            st.markdown("---")
            col1, col2 = st.columns([8, 2])

            with col1:
                st.markdown(f"### {review['company_name']} - ⭐ {review['rating']}")
                st.markdown(f"**{text['department_label']}:** {review['department']} | **{text['role_label']}:** {review['internship_role']}")
                st.markdown(f"**{text['review_label']}:** {review['review_text']}")
                st.markdown(f"**{text['salary_label']}:** {review['salary_info']} | **{text['project_rating_label']}:** {review['project_rating']}/10")
                st.markdown(f"**{text['feedback_date_label']}:** {review['feedback_date']}")
            
            with col2:
                if st.button(f"{text['helpful_button']} ({review.get('like_count', 0)})", 
                             key=f"like_{review['_id']}"):
                    # Increment like count
                    reviews_collection.update_one(
                        {"_id": review["_id"]}, 
                        {"$inc": {"like_count": 1}}
                    )
                    st.experimental_rerun()
    else:
        st.info(text["no_reviews_found"])  # Localized "No reviews found" message
