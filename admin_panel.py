import streamlit as st
from backend.db_connection import connect_to_collection

def admin_panel():
    st.title("Admin Panel")
    tab1, tab2 = st.tabs(["Pending Reviews", "Manage Companies"])

    # Pending Reviews Tab
    with tab1:
        st.subheader("Pending Reviews")
        reviews_collection = connect_to_collection('reviews')

        if reviews_collection:
            pending_reviews = list(reviews_collection.find({"admin_approved": False}))
            if len(pending_reviews) == 0:
                st.write("No pending reviews!")
            else:
                for review in pending_reviews:
                    with st.container():
                        st.write(f"**Company:** {review['company_name']} | **Position:** {review['position']}")
                        st.write(f"**Submission Date:** {review['submission_date']}")
                        st.write(f"**Review Text:** {review['review_text']}")

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Approve", key=f"approve_{review['_id']}"):
                                reviews_collection.update_one({"_id": review['_id']}, {"$set": {"admin_approved": True}})
                                st.experimental_rerun()
                        with col2:
                            if st.button("Reject", key=f"reject_{review['_id']}"):
                                reviews_collection.delete_one({"_id": review['_id']})
                                st.experimental_rerun()
        else:
            st.error("Could not connect to the reviews collection.")

    # Manage Companies Tab
    with tab2:
        st.subheader("Manage Companies")
        companies_collection = connect_to_collection('companies')

        if companies_collection:
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
