import streamlit as st
from app.utils import lang_dict  # Centralized language dictionary


def render_filter_section(
    companies_collection, reviews_collection, pre_filled_filters=None
):
    """
    Render filters for reviews page with optional pre-filled values.
    """
    text = lang_dict[st.session_state["language"]]  # Select language-specific text
    pre_filled_filters = pre_filled_filters or {}

    # Fetch
    companies = companies_collection.find({}, {"_id": 0, "name": 1})
    company_list = [company["name"] for company in companies]
    company_list.insert(0, text["all_companies"])  # Add "All Companies" placeholder

    st.markdown(f"### **{text['filter_section_title']}**")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        company_filter = st.selectbox(
            text["company_filter"],
            options=company_list,
            index=(
                company_list.index(
                    pre_filled_filters.get("company_filter", text["all_companies"])
                )
                if pre_filled_filters.get("company_filter") in company_list
                else 0
            ),
        )

    with col2:
        rating_filter = st.selectbox(
            text["rating_filter"],
            options=[text["all_ratings"]] + [5, 4, 3, 2, 1],
            index=(
                [text["all_ratings"]]
                + [5, 4, 3, 2, 1].index(
                    pre_filled_filters.get("rating_filter", text["all_ratings"])
                )
                if pre_filled_filters.get("rating_filter") in [5, 4, 3, 2, 1]
                else 0
            ),
        )

    # dynamic filters
    query = {}
    if company_filter != text["all_companies"]:
        query["company_name"] = company_filter
    if rating_filter != text["all_ratings"]:
        query["rating"] = int(rating_filter)

    departments = reviews_collection.distinct("department", query)
    departments.insert(0, text["all_departments"])  # Add "All Departments" placeholder

    with col3:
        department_filter = st.selectbox(
            text["department_filter"],
            options=departments,
            index=(
                departments.index(
                    pre_filled_filters.get("department_filter", text["all_departments"])
                )
                if pre_filled_filters.get("department_filter") in departments
                else 0
            ),
        )

    with col4:
        internship_role_filter = st.text_input(text["role_filter"])

    sort_option = st.radio(
        text["sort_option_label"], text["sort_options"], horizontal=True
    )

    return {
        "company_filter": company_filter,
        "rating_filter": rating_filter,
        "department_filter": department_filter,
        "internship_role_filter": internship_role_filter,
        "sort_option": sort_option,
    }
