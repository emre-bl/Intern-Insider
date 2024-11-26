import streamlit as st

def display_reviews(reviews, reviews_collection):
    """
    Display reviews with like functionality
    """
    if reviews:
        for review in reviews:
            st.markdown("---")
            col1, col2 = st.columns([8, 2])

            with col1:
                st.markdown(f"### {review['company_name']} - ⭐ {review['rating']}")
                st.markdown(f"**Department:** {review['department']} | **Role:** {review['internship_role']}")
                st.markdown(f"**Review:** {review['review_text']}")
                st.markdown(f"**Salary:** {review['salary_info']} | **Project Rating:** {review['project_rating']}/10")
                st.markdown(f"**Feedback Date:** {review['feedback_date']}")
            
            with col2:
                if st.button(f"👍 Helpful ({review.get('like_count', 0)})", 
                             key=f"like_{review['_id']}"):
                    # Increment like count
                    reviews_collection.update_one(
                        {"_id": review["_id"]}, 
                        {"$inc": {"like_count": 1}}
                    )
                    st.experimental_rerun()
    else:
        st.info("No reviews found.")