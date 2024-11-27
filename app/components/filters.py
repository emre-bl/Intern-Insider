import streamlit as st
from app.utils import lang_dict  # Centralized language dictionary

def render_filter_section(companies_collection, reviews_collection):
    """
    Render filters for reviews page with centralized language support.
    """
    text = lang_dict[st.session_state['language']]  # Select language-specific text

    # Fetch companies and create a dropdown list
    companies = companies_collection.find({}, {"_id": 0, "name": 1})
    company_list = [company["name"] for company in companies]
    company_list.insert(0, text["all_companies"])  # Add "All Companies" placeholder

    # Display filter section title
    st.markdown(f"### **{text['filter_section_title']}**")

    # Create columns for filters
    col1, col2, col3, col4 = st.columns(4)

    # Company Filter
    with col1:
        company_filter = st.selectbox(text["company_filter"], options=company_list)

    # Rating Filter
    with col2:
        rating_filter = st.selectbox(
            text["rating_filter"],
            options=[text["all_ratings"]] + [5, 4, 3, 2, 1]  # Include "All Ratings" option
        )

    # Query for dynamic department filter based on selected company and rating
    query = {}
    if company_filter != text["all_companies"]:
        query["company_name"] = company_filter
    if rating_filter != text["all_ratings"]:
        query["rating"] = int(rating_filter)

    # Fetch departments dynamically and add placeholder
    departments = reviews_collection.distinct("department", query)
    departments.insert(0, text["all_departments"])  # Add "All Departments" placeholder

    # Department Filter
    with col3:
        department_filter = st.selectbox(text["department_filter"], options=departments)

    # Internship Role Filter
    with col4:
        internship_role_filter = st.text_input(text["role_filter"])

    # Sorting Options
    sort_option = st.radio(
        text["sort_option_label"], 
        text["sort_options"], 
        horizontal=True
    )

    # Return selected filters
    return {
        'company_filter': company_filter,
        'rating_filter': rating_filter,
        'department_filter': department_filter,
        'internship_role_filter': internship_role_filter,
        'sort_option': sort_option
    }
