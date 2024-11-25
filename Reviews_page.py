from datetime import datetime
import streamlit as st
from pymongo import MongoClient
from backend.db_connection import connect_to_collection

def reviews_page():
    st.markdown("# Reviews")

    # MongoDB'den collection bağlantısı
    reviews_collection = connect_to_collection('reviews')
    companies_collection = connect_to_collection('company')
    
    if reviews_collection is None or companies_collection is None:
        st.error("Veritabanı bağlantısı başarısız.")
        return

    # Şirket isimlerini getir
    companies = companies_collection.find({}, {"_id": 0, "name": 1})
    company_list = [company["name"] for company in companies]
    company_list.insert(0, "All Companies")  # Tüm şirketler için bir seçenek ekle

    # Filtreleme Bölümü
    st.markdown("### **Filter Reviews**")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        company_filter = st.selectbox("Company", options=company_list)
    with col2:
        rating_filter = st.selectbox("Rating", options=["All Ratings", 5, 4, 3, 2, 1])
    with col3:
        department_filter = st.text_input("Department")
    with col4:
        internship_role_filter = st.text_input("Internship Role")

    # Sıralama
    sort_option = st.radio("Sort Reviews", ["Most Liked", "Newest First", "Oldest First"], horizontal=True)

    # Filtreleme ve Sıralama İşlemleri
    query = {}
    if company_filter != "All Companies":
        query["company_name"] = company_filter
    if rating_filter != "All Ratings":
        query["rating"] = int(rating_filter)
    if department_filter:
        query["department"] = {"$regex": department_filter, "$options": "i"}
    if internship_role_filter:
        query["internship_role"] = {"$regex": internship_role_filter, "$options": "i"}

    # MongoDB'den veriyi al ve sırala
    reviews = list(reviews_collection.find(query))
    if sort_option == "Most Liked":
        reviews = list(reviews_collection.find(query).sort(sort_by)) if sort_by else list(reviews_collection.find(query))
    elif sort_option == "Newest First":
        reviews = sorted(reviews, key=lambda x: datetime.strptime(x['feedback_date'], "%d/%m/%Y"), reverse=True)
    elif sort_option == "Oldest First":
        reviews = sorted(reviews, key=lambda x: datetime.strptime(x['feedback_date'], "%d/%m/%Y"))



    # İncelemeleri Gösterme
    if reviews:
        for review in reviews:
            st.markdown("---")
            col1, col2 = st.columns([8, 2])

            with col1:
                st.markdown(f"### {review['company_name']} - ⭐ {review['rating']}")
                st.markdown(f"**Department:** {review['department']} | **Role:** {review['internship_role']}")
                st.markdown(f"**Review:** {review['review_text']}")
                st.markdown(f"**Salary:** {review['salary_info']} | **Project Rating:** {review['project_rating']}/10")
                st.markdown(f"**Feedback Date:** {review['feedback_date']}")
            with col2:
                if st.button(f"👍 Helpful ({review['like_count']})", key=f"like_{review['_id']}"):
                    # Beğeni Sayısını Artır
                    reviews_collection.update_one({"_id": review["_id"]}, {"$inc": {"like_count": 1}})
                    st.experimental_rerun()
    else:
        st.info("Hiç yorum bulunamadı.")

# Fonksiyonu çağır
if __name__ == "__main__":
    reviews_page()
