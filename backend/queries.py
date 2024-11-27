from datetime import datetime

def build_reviews_query(company_filter=None, rating_filter=None, 
                        department_filter=None, internship_role_filter=None, 
                        all_ratings_placeholder=None):
    """
    Build a dynamic MongoDB query based on provided filters
    """
    query = {"admin_approved": True}

    if company_filter and company_filter not in ["All Companies", "Tüm Şirketler"]:
        query["company_name"] = company_filter
    
    if rating_filter and rating_filter != all_ratings_placeholder:  # Skip placeholder
        try:
            query["rating"] = int(rating_filter)
        except ValueError:
            pass  # Ignore non-numeric values
    
    if department_filter and department_filter not in ["All Departments", "Tüm Departmanlar"]:
        query["department"] = department_filter
    
    if internship_role_filter:
        query["internship_role"] = {"$regex": internship_role_filter, "$options": "i"}
    
    return query

def sort_reviews(reviews, sort_option):
    """
    Sort reviews based on selected option
    """
    if sort_option == "Most Liked":
        return sorted(reviews, key=lambda x: x.get('like_count', 0), reverse=True)
    elif sort_option == "Newest First":
        return sorted(reviews, 
                      key=lambda x: datetime.strptime(x['feedback_date'], "%d/%m/%Y"), 
                      reverse=True)
    elif sort_option == "Oldest First":
        return sorted(reviews, 
                      key=lambda x: datetime.strptime(x['feedback_date'], "%d/%m/%Y"))
    return reviews