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

# Language Switch
def switch_language():
    current_lang = st.session_state.get('language', 'en')
    new_lang = 'tr' if current_lang == 'en' else 'en'
    st.session_state['language'] = new_lang
    st.experimental_rerun()

def admin_panel():
    if 'language' not in st.session_state:
        st.session_state['language'] = 'en'

    text = lang_dict[st.session_state['language']]

    # Header Section
    col1, col2 = st.columns([9, 1])
    with col2:
        if st.button("🌐 TR/EN"):
            switch_language()

    st.title(text["title"])

    # Ana sayfaya dönme butonu
    if st.button(text["home_button"]):
        st.session_state['page'] = 'home'
        st.experimental_rerun()

    tab1, tab2 = st.tabs([text["pending_reviews_tab"], text["manage_companies_tab"]])

    # Pending Reviews Tab
    with tab1:
        st.subheader(text["pending_reviews"])
        reviews_collection = connect_to_collection('reviews')
        if reviews_collection is not None:
            pending_reviews = list(reviews_collection.find({"admin_approved": False}))

            if len(pending_reviews) == 0:
                st.write(text["no_pending_reviews"])
            else:
                if "current_review_index" not in st.session_state:
                    st.session_state.current_review_index = 0

                current_index = st.session_state.current_review_index
                if current_index < len(pending_reviews):
                    review = pending_reviews[current_index]
                    company_name = review.get('company_name', text["company_name"])
                    position = review.get('position', text["position"])
                    submission_date = review.get('submission_date', text["submission_date"])
                    review_text = review.get('review_text', text["review_text"])

                    st.write(f"**{text['company_name']}:** {company_name}")
                    st.write(f"**{text['position']}:** {position}")
                    st.write(f"**{text['submission_date']}:** {submission_date}")
                    st.write(f"**{text['review_text']}:** {review_text}")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(text["approve_button"]):
                            reviews_collection.update_one(
                                {"_id": review['_id']}, {"$set": {"admin_approved": True}}
                            )
                            st.session_state.current_review_index += 1
                            st.experimental_rerun()

                    with col2:
                        if st.button(text["reject_button"]):
                            reviews_collection.delete_one({"_id": review['_id']})
                            st.session_state.current_review_index += 1
                            st.experimental_rerun()
                else:
                    st.write(text["no_more_reviews"])
        else:
            st.error("Could not connect to the reviews collection.")

    # Manage Companies Tab
    with tab2:
        st.subheader(text["manage_companies_tab"])
        companies_collection = connect_to_collection('company')

        if companies_collection is not None:
            # Add Company Section
            st.markdown(f"### {text['add_company']}")
            with st.form("add_company_form"):
                company_name = st.text_input(text["company_name"])
                industry = st.text_input(text["industry"])
                location = st.text_input(text["location"])
                submitted = st.form_submit_button(text["submit_button"])
                if submitted:
                    new_company = {
                        "name": company_name,
                        "industry": industry,
                        "location": location,
                        "created_at": datetime.now()
                    }
                    companies_collection.insert_one(new_company)
                    st.success(text["success_add"])
                    st.experimental_rerun()

            # Remove Company Section
            st.markdown(f"### {text['remove_company']}")
            existing_companies = list(companies_collection.find())
            if existing_companies:
                company_names = {str(company['_id']): company['name'] for company in existing_companies}
                selected_company_id = st.selectbox(
                    text["select_company_to_remove"], options=company_names.keys(), format_func=lambda x: company_names[x]
                )
                if st.button(text["remove_company"]):
                    companies_collection.delete_one({"_id": ObjectId(selected_company_id)})
                    st.success(text["remove_success"].format(company_names[selected_company_id]))
                    st.experimental_rerun()
            else:
                st.write(text["no_pending_reviews"])
        else:
            st.error("Could not connect to the companies collection.")
