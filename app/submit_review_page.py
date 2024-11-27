import streamlit as st
from datetime import datetime
from backend.db_connection import create_review, get_companies
from app.utils import initialize_session_state, lang_dict
import time

def render_header():
    """Render the header with Home and Language Toggle buttons."""
    text = lang_dict[st.session_state['language']]

    col1, col2, col3 = st.columns([8, 1, 1])
    with col2:
        # Home Button
        if st.button(text["home_button"], key="home_button"):
            st.session_state['page'] = 'home'
            st.experimental_rerun()
    with col3:
        # Language Toggle Button
        if st.button("🌐 TR/EN", key="lang_toggle"):
            st.session_state['language'] = 'tr' if st.session_state['language'] == 'en' else 'en'
            st.experimental_rerun()

def handle_form_submission(form_data):
    """Handle form submission logic."""
    text = lang_dict[st.session_state['language']]
    review_data = {
        "company_name": form_data.get('company_name', ''),
        "review_text": form_data.get('review_text', ''),
        "rating": form_data.get('rating', 3),
        "salary_info": form_data.get('salary', text["not_provided"]),
        "department": form_data.get('department', ''),
        "internship_role": form_data.get('internship_role', ''),
        "project_rating": form_data.get('project_quality', 1),
        "transportation_info": form_data.get('transportation', False),
        "remote_work_option": form_data.get('remote_work', False),
        "meal_card": form_data.get('meal_allowance', False),
        "technologies_used": form_data.get('technologies_used', '').split(", "),
        "feedback_date": datetime.now().strftime("%d/%m/%Y"),
        "like_count": 0,
        "admin_approved": False
    }

    # Save review to the database
    review_id = create_review(review_data)
    return review_id is not None

def render_review_form():
    """Render the form to submit an internship review."""
    text = lang_dict[st.session_state['language']]

    # Fetch company list from the database
    companies = get_companies()
    if not companies:
        st.error(text["company_warning_message"])
        return

    companies.insert(0, text["company_name"])  # Add placeholder for the dropdown

    # Form layout
    with st.form("review_form", clear_on_submit=True):
        st.markdown(f"<h1>{text['submit_review_page']}</h1>", unsafe_allow_html=True)

        # Form fields
        form_data = {
            'company_name': st.selectbox(text["company_name"], companies),
            'rating': st.select_slider(text["overall_rating"], options=[1, 2, 3, 4, 5], value=3),
            'review_text': st.text_area(text["detailed_review"]),
            'salary': st.text_input(text["salary"]),
            'department': st.text_input(text["department"]),
            'internship_role': st.text_input(text["internship_role"]),
            'project_quality': st.slider(text["project_quality"], 1, 10),
            'transportation': st.checkbox(text["transportation"]),
            'remote_work': st.checkbox(text["remote_work"]),
            'meal_allowance': st.checkbox(text["meal_allowance"]),
            'technologies_used': st.text_input(
                text["technologies_used"], 
                value="", 
                placeholder=text["tech_used_placeholder"]
            )
        }

        # Submit Button
        submitted = st.form_submit_button(text["submit_button"])
        if submitted:
            # Validation
            if form_data['company_name'] == text["company_name"]:
                st.warning(text['company_warning_message'])
            elif not form_data['review_text']:
                st.warning(text['warning_message'])
            elif handle_form_submission(form_data):
                st.success(text["success_message"])
                time.sleep(2)  # Wait before redirecting
                st.session_state['page'] = 'home'
                st.experimental_rerun()
            else:
                st.error("There was an error saving your review. Please try again.")

def submit_review():
    """Main function for the Submit Review page."""
    initialize_session_state()
    text = lang_dict[st.session_state['language']]

    # Render Header
    render_header()

    # Render Review Form
    render_review_form()

if __name__ == "__main__":
    submit_review()
