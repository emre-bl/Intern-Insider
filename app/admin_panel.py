import streamlit as st
from backend.db_connection import connect_to_collection
from datetime import datetime
from bson import ObjectId
from app.utils import initialize_session_state, lang_dict

def switch_language():
    """Switch between languages."""
    st.session_state['language'] = 'tr' if st.session_state['language'] == 'en' else 'en'

def render_header():
    """Render the header with Home and Language Toggle buttons."""
    text = lang_dict[st.session_state['language']]
    col1, col2, col3 = st.columns([8, 1, 1])
    with col2:
        if st.button(text["home_button"], key="home_button"):
            st.session_state['page'] = 'home'
            st.experimental_rerun()
    with col3:
        if st.button("🌐 TR/EN", key="lang_toggle"):
            switch_language()
            st.experimental_rerun()

@st.cache(ttl=30)  # Cache for a limited time
def fetch_pending_reviews():
    """Fetch pending reviews from the database."""
    reviews_collection = connect_to_collection('reviews')
    if reviews_collection is not None:
        return list(reviews_collection.find({"admin_approved": False}))
    return []

@st.cache(ttl=100)  # Cache for a longer duration
def fetch_companies():
    """Fetch companies from the database."""
    companies_collection = connect_to_collection('company')
    if companies_collection is not None:
        return list(companies_collection.find())
    return []

def handle_review_action(review_id, action, reviews_collection):
    """Handle review approval or rejection."""
    if action == 'approve':
        reviews_collection.update_one(
            {"_id": ObjectId(review_id)},
            {"$set": {"admin_approved": True}}
        )
    elif action == 'reject':
        reviews_collection.delete_one({"_id": ObjectId(review_id)})
    
    st.session_state.current_review_index += 1
    st.session_state.last_refresh = datetime.now()

def display_pending_reviews(text):
    """Display and handle pending reviews."""
    reviews_collection = connect_to_collection('reviews')
    if reviews_collection is None:
        st.error(text["db_connection_error"])
        return

    # Refresh pending reviews if necessary
    pending_reviews = fetch_pending_reviews()
    if not pending_reviews:
        st.write(text["no_pending_reviews"])
        return

    current_index = st.session_state.get("current_review_index", 0)
    if current_index >= len(pending_reviews):
        st.write(text["no_more_reviews"])
        return

    review = pending_reviews[current_index]
    with st.container():
        st.write(f"**{text['company_name']}:** {review.get('company_name')}")
        st.write(f"**{text['position']}:** {review.get('internship_role')}")
        st.write(f"**{text['submission_date']}:** {review.get('feedback_date')}")
        st.write(f"**{text['review_text']}:** {review.get('review_text')}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button(text["approve_review_button"], key=f"approve_{current_index}"):
                handle_review_action(review['_id'], 'approve', reviews_collection)
                st.experimental_rerun()
        with col2:
            if st.button(text["reject_review_button"], key=f"reject_{current_index}"):
                handle_review_action(review['_id'], 'reject', reviews_collection)
                st.experimental_rerun()

def handle_company_management(text):
    """Handle company addition and removal."""
    companies_collection = connect_to_collection('company')
    if companies_collection is None:
        st.error(text["db_connection_error"])
        return

    # Add Company Section
    with st.form("add_company_form", clear_on_submit=True):
        st.markdown(f"### {text['add_new_company']}")
        company_data = {
            "name": st.text_input(text["company_name"]),
            "industry": st.text_input(text["industry"]),
            "location": st.text_input(text["location"]),
        }
        if st.form_submit_button(text["submit_button"]):
            company_data["created_at"] = datetime.now()
            companies_collection.insert_one(company_data)
            st.success(text["success_add"])
            st.experimental_rerun()

    # Remove Company Section
    st.markdown(f"### {text['remove_company']}")
    companies = fetch_companies()
    if not companies:
        st.info(text["no_pending_reviews"])
        return

    company_names = {str(company['_id']): company['name'] for company in companies}
    selected_company_id = st.selectbox(
        text["remove_company"],
        options=company_names.keys(),
        format_func=lambda x: company_names[x]
    )

    if st.button(text["remove_company"]):
        companies_collection.delete_one({"_id": ObjectId(selected_company_id)})
        st.success(text["remove_success"].format(company_names[selected_company_id]))
        st.experimental_rerun()

def admin_panel():
    """Main admin panel function."""
    initialize_session_state()
    text = lang_dict[st.session_state['language']]

    # Header
    render_header()

    # Title
    st.title(text["admin_panel_title"])

    # Tabs
    tab1, tab2 = st.tabs([text["pending_reviews_tab"], text["manage_companies_tab"]])

    with tab1:
        st.subheader(text["pending_reviews_tab"])
        display_pending_reviews(text)

    with tab2:
        st.subheader(text["manage_companies_tab"])
        handle_company_management(text)

if __name__ == "__main__":
    admin_panel()
