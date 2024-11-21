import streamlit as st
from backend.db_connection import connect_to_collection
from datetime import datetime

def admin_panel():
    st.title("Admin Panel")
    
    # Ana sayfaya dönme butonu
    if st.button("Ana Sayfa"):
        st.session_state['page'] = 'home'  # Ana sayfaya dön
        st.experimental_rerun()

    tab1, tab2 = st.tabs(["Pending Reviews", "Manage Companies"])

    # Pending Reviews Tab
    with tab1:
        st.subheader("Pending Reviews")
        reviews_collection = connect_to_collection('reviews')
        if reviews_collection is not None:
            st.write("**Pending Reviews:**")
            pending_reviews = list(reviews_collection.find({"admin_approved": False}))

            if len(pending_reviews) == 0:
                st.write("No pending reviews!")
            else:
                # Sıradaki belgenin indeksi için Streamlit session state kullanımı
                if "current_review_index" not in st.session_state:
                    st.session_state.current_review_index = 0
                
                # Belirtilen indeksteki belgeyi al
                current_index = st.session_state.current_review_index
                if current_index < len(pending_reviews):
                    review = pending_reviews[current_index]
                    company_name = review.get('company_name', 'Unknown Company')
                    position = review.get('position', 'Not Provided')
                    submission_date = review.get('submission_date', 'Unknown Date')
                    review_text = review.get('review_text', 'No Review Text Provided')

                    st.write(f"**Company:** {company_name}")
                    st.write(f"**Position:** {position}")
                    st.write(f"**Submission Date:** {submission_date}")
                    st.write(f"**Review Text:** {review_text}")

                    # Onaylama ve reddetme butonları
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Approve"):
                            reviews_collection.update_one(
                                {"_id": review['_id']}, {"$set": {"admin_approved": True}}
                            )
                            st.session_state.current_review_index += 1  # Bir sonraki incelemeye geç
                            st.experimental_rerun()

                    with col2:
                        if st.button("Reject"):
                            reviews_collection.delete_one({"_id": review['_id']})
                            st.session_state.current_review_index += 1  # Bir sonraki incelemeye geç
                            st.experimental_rerun()
                else:
                    st.write("No more pending reviews!")
        else:
            st.error("Could not connect to the reviews collection.")

    # Manage Companies Tab
    with tab2:
        st.subheader("Manage Companies")
        companies_collection = connect_to_collection('company')

        if companies_collection is not None:
            # Add new company form
            with st.form("add_company_form"):
                company_name = st.text_input("Company Name")
                industry = st.text_input("Industry")
                location = st.text_input("Location")
                submitted = st.form_submit_button("Add Company")
                if submitted:
                    new_company = {
                        "name": company_name,
                        "industry": industry,
                        "location": location,
                        "created_at": datetime.now()
                    }
                    companies_collection.insert_one(new_company)
                    st.success("Company added successfully!")
                    st.experimental_rerun()

            # List existing companies
            st.write("**Existing Companies:**")
            companies = list(companies_collection.find())
            for company in companies:
                with st.container():
                    st.write(f"**{company['name']}** ({company['industry']} - {company['location']})")
                    if st.button("Remove", key=f"remove_{company['_id']}"):
                        companies_collection.delete_one({"_id": company['_id']})
                        st.experimental_rerun()
        else:
            st.error("Could not connect to the companies collection.")
