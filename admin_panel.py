import streamlit as st
from backend.db_connection import connect_to_collection
from datetime import datetime
from bson import ObjectId

# Translations
lang_dict = {
    'en': {
        "title": "Admin Panel",
        "home_button": "Go to Home",
        "pending_reviews_tab": "Pending Reviews",
        "manage_companies_tab": "Manage Companies",
        "add_company": "Add Company",
        "remove_company": "Remove Company",
        "pending_reviews": "Pending Reviews",
        "no_pending_reviews": "No pending reviews!",
        "company_name": "Company Name",
        "industry": "Industry",
        "location": "Location",
        "submit_button": "Add Company",
        "success_add": "Company added successfully!",
        "remove_success": "Company '{}' removed successfully!",
        "select_company_to_remove": "Select Company to Remove",
        "approve_button": "Approve",
        "reject_button": "Reject",
        "no_more_reviews": "No more pending reviews!",
        "review_text": "Review Text",
        "submission_date": "Submission Date",
        "position": "Position",
    },
    'tr': {
        "title": "Admin Paneli",
        "home_button": "Ana Sayfa",
        "pending_reviews_tab": "Bekleyen Değerlendirmeler",
        "manage_companies_tab": "Şirket Yönetimi",
        "add_company": "Şirket Ekle",
        "remove_company": "Şirket Sil",
        "pending_reviews": "Bekleyen Değerlendirmeler",
        "no_pending_reviews": "Bekleyen değerlendirme yok!",
        "company_name": "Şirket Adı",
        "industry": "Endüstri",
        "location": "Konum",
        "submit_button": "Şirket Ekle",
        "success_add": "Şirket başarıyla eklendi!",
        "remove_success": "Şirket '{}' başarıyla silindi!",
        "select_company_to_remove": "Silmek için Şirket Seç",
        "approve_button": "Onayla",
        "reject_button": "Reddet",
        "no_more_reviews": "Daha fazla bekleyen değerlendirme yok!",
        "review_text": "Değerlendirme Metni",
        "submission_date": "Gönderim Tarihi",
        "position": "Pozisyon",
    }
}


def initialize_session_state():
    """Initialize session state variables"""
    if 'language' not in st.session_state:
        st.session_state['language'] = 'en'
    if 'current_review_index' not in st.session_state:
        st.session_state.current_review_index = 0
    if 'pending_reviews' not in st.session_state:
        st.session_state.pending_reviews = []
    if 'companies' not in st.session_state:
        st.session_state.companies = []
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()


def switch_language():
    """Switch between languages"""
    st.session_state['language'] = 'tr' if st.session_state['language'] == 'en' else 'en'

@st.cache(ttl=10)  
def fetch_pending_reviews():
    """Fetch pending reviews from database"""
    reviews_collection = connect_to_collection('reviews')
    if reviews_collection is not None:
        return list(reviews_collection.find({"admin_approved": False}))
    return []

@st.cache(ttl=10)  
def fetch_companies():
    """Fetch companies from database"""
    companies_collection = connect_to_collection('company')
    if companies_collection is not None:
        return list(companies_collection.find())
    return []

def handle_review_action(review_id, action, reviews_collection):
    """Handle review approval or rejection"""
    if action == 'approve':
        reviews_collection.update_one(
            {"_id": review_id},
            {"$set": {"admin_approved": True}}
        )
    else:  # reject
        reviews_collection.delete_one({"_id": review_id})
    
    st.session_state.current_review_index += 1
    # Force refresh of cached reviews
    st.session_state.last_refresh = datetime.now()

def display_pending_reviews(text):
    """Display and handle pending reviews"""
    reviews_collection = connect_to_collection('reviews')
    if reviews_collection is None:
        st.error("Could not connect to the reviews collection.")
        return

    # Fetch reviews only if needed
    if datetime.now().timestamp() - st.session_state.last_refresh.timestamp() > 10:
        pending_reviews = fetch_pending_reviews()
        st.session_state.pending_reviews = pending_reviews
    else:
        pending_reviews = st.session_state.pending_reviews

    if not pending_reviews:
        st.write(text["no_pending_reviews"])
        return

    current_index = st.session_state.current_review_index
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
            if st.button(text["approve_button"], key=f"approve_{current_index}"):
                handle_review_action(review['_id'], 'approve', reviews_collection)
                st.experimental_rerun()

        with col2:
            if st.button(text["reject_button"], key=f"reject_{current_index}"):
                handle_review_action(review['_id'], 'reject', reviews_collection)
                st.experimental_rerun()

def handle_company_management(text):
    """Handle company addition and removal"""
    companies_collection = connect_to_collection('company')
    if companies_collection is None:
        st.error("Could not connect to the companies collection.")
        return

    # Add Company Form
    with st.form("add_company_form", clear_on_submit=True):
        st.markdown(f"### {text['add_company']}")
        company_data = {
            "name": st.text_input(text["company_name"]),
            "industry": st.text_input(text["industry"]),
            "location": st.text_input(text["location"]),
        }
        
        if st.form_submit_button(text["submit_button"]):
            company_data["created_at"] = datetime.now()
            companies_collection.insert_one(company_data)
            st.success(text["success_add"])
            st.session_state.last_refresh = datetime.now()
            st.experimental_rerun()

    # Remove Company Section
    st.markdown(f"### {text['remove_company']}")
    companies = fetch_companies()
    
    if companies:
        company_names = {str(company['_id']): company['name'] for company in companies}
        selected_company_id = st.selectbox(
            text["select_company_to_remove"],
            options=company_names.keys(),
            format_func=lambda x: company_names[x]
        )
        
        if st.button(text["remove_company"]):
            companies_collection.delete_one({"_id": ObjectId(selected_company_id)})
            st.success(text["remove_success"].format(company_names[selected_company_id]))
            st.session_state.last_refresh = datetime.now()
            st.experimental_rerun()
    else:
        st.write(text["no_pending_reviews"])

def admin_panel():
    """Main admin panel function"""
    initialize_session_state()
    text = lang_dict[st.session_state['language']]

    # Header
    col1, col2 = st.columns([9, 1])
    with col2:
        if st.button("🌐 TR/EN"):
            switch_language()
            st.experimental_rerun()

    st.title(text["title"])

    if st.button(text["home_button"]):
        st.session_state['page'] = 'home'
        st.experimental_rerun()

    # Tabs
    tab1, tab2 = st.tabs([text["pending_reviews_tab"], text["manage_companies_tab"]])

    with tab1:
        st.subheader(text["pending_reviews"])
        display_pending_reviews(text)

    with tab2:
        st.subheader(text["manage_companies_tab"])
        handle_company_management(text)

if __name__ == "__main__":
    admin_panel()