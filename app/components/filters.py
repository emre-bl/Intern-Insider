import streamlit as st

def render_filter_section(companies_collection, reviews_collection):
    """
    Render filters for reviews page
    """
    # Fetch companies and departments
    companies = companies_collection.find({}, {"_id": 0, "name": 1})
    company_list = [company["name"] for company in companies]
    company_list.insert(0, "All Companies")

    st.markdown("### **Filter Reviews**")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        company_filter = st.selectbox("Company", options=company_list)
    with col2:
        rating_filter = st.selectbox("Rating", options=["All Ratings", 5, 4, 3, 2, 1])

    # Dynamic departments based on current filters
    query = {}
    if company_filter != "All Companies":
        query["company_name"] = company_filter
    if rating_filter != "All Ratings":
        query["rating"] = int(rating_filter)

    departments = reviews_collection.distinct("department", query)
    departments.insert(0, "All Departments")

    with col3:
        department_filter = st.selectbox("Department", options=departments)
    with col4:
        internship_role_filter = st.text_input("Internship Role")

    # Sorting
    sort_option = st.radio("Sort Reviews", 
                            ["Most Liked", "Newest First", "Oldest First"], 
                            horizontal=True)

    return {
        'company_filter': company_filter,
        'rating_filter': rating_filter,
        'department_filter': department_filter,
        'internship_role_filter': internship_role_filter,
        'sort_option': sort_option
    }