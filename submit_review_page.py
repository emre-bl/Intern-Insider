import streamlit as st
from datetime import datetime
from backend.db_connection import create_review  

lang_dict = {
    'en': {
        "submit_review": "Submit Internship Review",
        "company_name": "Company Name",
        "overall_rating": "Overall Rating",
        "detailed_review": "Detailed Review",
        "salary": "Salary Information (Optional)",
        "department": "Department",
        "internship_role": "Internship Role",
        "project_quality": "Project Quality Rating (1-10)",
        "additional_info": "Additional Information",
        "transportation": "Transportation Available",
        "remote_work": "Remote Work Option",
        "meal_allowance": "Meal Allowance",
        "technologies_used": "Technologies Used",
        "submit_button": "Submit Review",
        "return_home": "Return to Home",
        "success_message": "Your review has been successfully submitted!",
        "not_provided": "Not provided",
        "rating_stars": "★"
    },
    'tr': {
        "submit_review": "Staj Değerlendirmesi Gönder",
        "company_name": "Şirket Adı",
        "overall_rating": "Genel Değerlendirme",
        "detailed_review": "Detaylı Değerlendirme",
        "salary": "Aylık Maaş Bilgisi (Opsiyonel)",
        "department": "Departman",
        "internship_role": "Staj Pozisyonu",
        "project_quality": "Proje Kalitesi Puanı (1-10)",
        "additional_info": "Ek Bilgi",
        "transportation": "Ulaşım Mevcut",
        "remote_work": "Uzaktan Çalışma Seçeneği",
        "meal_allowance": "Yemek Yardımı",
        "technologies_used": "Kullanılan Teknolojiler",
        "submit_button": "Değerlendirmeyi Gönder",
        "return_home": "Ana Sayfaya Dön",
        "success_message": "Değerlendirmeniz başarıyla gönderildi!",
        "not_provided": "Sağlanmadı",
        "rating_stars": "★"
    }
}

def switch_language():
    current_lang = st.session_state.get('language', 'en')
    new_lang = 'tr' if current_lang == 'en' else 'en'
    st.session_state['language'] = new_lang
    st.session_state['language_changed'] = True  # Dil değişti flag'ini ekleyin

def submit_review():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'  # Varsayılan sayfa
    
    if st.session_state['page'] == 'home':
        st.title("Home Page")
        st.write("Welcome to the internship review platform!")

        # Ana sayfada "Go to Submit Review" butonu
        if st.button("Go to Submit Review"):
            st.session_state['page'] = 'submit_review'  # Sayfayı değiştirme
            st.experimental_rerun()  # Sayfayı yeniden yükle

    elif st.session_state['page'] == 'submit_review':
        # Dil seçimi
        if 'language_changed' not in st.session_state:
            st.session_state['language_changed'] = False  # Dil değişimi durumu başlatılır

        if st.session_state['language_changed']:
            st.session_state['language_changed'] = False  # Dil değişimi durumu sıfırlanır
            st.experimental_rerun()  # Sayfa yenilemesi

        # Dil seçimi butonunu sağ üst köşeye ekleyelim
        current_lang = st.session_state.get('language', 'en')
        text = lang_dict[current_lang]

        # Sayfa başlığı ve dil butonunu ekleyelim
        col1, col2 = st.columns([9, 1])
        with col2:
            # Dil değiştir butonu
            if st.button('🌐 TR/EN'):
                switch_language()
        
        st.markdown(f"<h1>{text['submit_review']}</h1>", unsafe_allow_html=True)

        company_name = st.selectbox(text["company_name"], ["ABC Corp", "XYZ Ltd", "Tech Solutions", "Innovative Labs", "Global Tech"])
        rating = st.select_slider(text["overall_rating"], options=[1, 2, 3, 4, 5], value=3)
        review_text = st.text_area(text["detailed_review"], placeholder="Share your internship experience...")
        salary = st.text_input(text["salary"], placeholder="Monthly salary")
        department = st.selectbox(text["department"], ["Computer Engineering", "Industrial Engineering", "Mechanical Engineering"])
        internship_role = st.text_input(text["internship_role"], placeholder="e.g., Software Developer Intern")
        project_quality = st.slider(text["project_quality"], 1, 10)
        
        # Ek Bilgi - seçenekli kutular
        st.write(text["additional_info"])
        transportation = st.checkbox(text["transportation"])
        remote_work = st.checkbox(text["remote_work"])
        meal_allowance = st.checkbox(text["meal_allowance"])
        
        # Kullanılan teknolojiler (metin alanı)
        technologies_used = st.text_input(text["technologies_used"], placeholder="e.g., Python, React, Docker")

        # Gönder butonu
        if st.button(text["submit_button"]):
            # Veritabanına kaydedilecek inceleme verileri
            review_data = {
                "company_name": company_name,
                "review_text": review_text,
                "rating": rating,
                "salary_info": salary if salary else text["not_provided"],
                "department": department,
                "internship_role": internship_role,
                "project_rating": project_quality,
                "transportation_info": text["transportation"] if transportation else text["not_provided"],
                "remote_work_option": text["remote_work"] if remote_work else text["not_provided"],
                "meal_card": text["meal_allowance"] if meal_allowance else text["not_provided"],
                "technologies_used": technologies_used.split(", "),  # Virgülle ayrılmış teknolojiler listesi
                "feedback_date": datetime.now().strftime("%d/%m/%Y"),
                "like_count": 0  # Varsayılan beğeni sayısı 0
            }

            # Veriyi veritabanına ekleme
            review_id = create_review(review_data)
            if review_id:
                st.success(text["success_message"])
            else:
                st.error("There was an error saving your review. Please try again.")
            
            # Form bilgilerini ekranda gösteriyoruz
            st.write(text["company_name"] + ":", company_name)
            st.write(text["overall_rating"] + ":", text["rating_stars"] * rating)
            st.write(text["detailed_review"] + ":", review_text)
            st.write(text["salary"] + ":", salary if salary else text["not_provided"])
            st.write(text["department"] + ":", department)
            st.write(text["internship_role"] + ":", internship_role)
            st.write(text["project_quality"] + ":", project_quality)
            st.write(text["transportation"] + ":", transportation)
            st.write(text["remote_work"] + ":", remote_work)
            st.write(text["meal_allowance"] + ":", meal_allowance)
            st.write(text["technologies_used"] + ":", technologies_used)

        # Ana sayfaya dönme butonu
        if st.button(text["return_home"]):
            st.session_state['page'] = 'home'  # Ana sayfaya dön
            st.experimental_rerun()  # Sayfayı yeniden yükle

if __name__ == "__main__":
    submit_review()
