import streamlit as st
from datetime import datetime
from backend.db_connection import create_review, get_companies

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

@st.cache  
def get_cached_companies():
    """Şirket listesini cache'le"""
    return get_companies()

def initialize_session_state():
    """Session state değişkenlerini başlat"""
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'
    if 'language' not in st.session_state:
        st.session_state['language'] = 'en'
    if 'form_submitted' not in st.session_state:
        st.session_state['form_submitted'] = False

def switch_language():
    """Dil değiştirme fonksiyonu"""
    st.session_state['language'] = 'tr' if st.session_state['language'] == 'en' else 'en'


def create_layout():
    """Sayfa düzenini oluştur"""
    col1, col2 = st.columns([9, 1])
    with col2:
        if st.button('🌐 TR/EN'):
            switch_language()
            st.experimental_rerun()
    return col1

def display_home_page():
    """Ana sayfa görüntüleme"""
    st.title("Home Page")
    st.write("Welcome to the internship review platform!")
    if st.button("Go to Submit Review"):
        st.session_state['page'] = 'submit_review'
        st.experimental_rerun()

def handle_form_submission(form_data, text):
    """Form gönderme işlemini yönet"""
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
    
    review_id = create_review(review_data)
    return review_id is not None

def display_review_form():
    """İnceleme formunu görüntüle"""
    text = lang_dict[st.session_state['language']]
    col1 = create_layout()
    
    companies = get_cached_companies()
    if not companies:
        st.error("No companies available for review.")
        return

    with st.form("review_form", clear_on_submit=True):
        st.markdown(f"<h1>{text['submit_review']}</h1>", unsafe_allow_html=True)
        
        form_data = {
            'company_name': st.selectbox(text["company_name"], companies),
            'rating': st.select_slider(text["overall_rating"], options=[1, 2, 3, 4, 5], value=3),
            'review_text': st.text_area(text["detailed_review"]),
            'salary': st.text_input(text["salary"]),
            'department': st.selectbox(text["department"], 
                                    ["Computer Engineering", "Industrial Engineering", "Mechanical Engineering"]),
            'internship_role': st.text_input(text["internship_role"]),
            'project_quality': st.slider(text["project_quality"], 1, 10),
            'transportation': st.checkbox(text["transportation"]),
            'remote_work': st.checkbox(text["remote_work"]),
            'meal_allowance': st.checkbox(text["meal_allowance"]),
            'technologies_used': st.text_input(text["technologies_used"])
        }

        submitted = st.form_submit_button(text["submit_button"])
        if submitted:
            if handle_form_submission(form_data, text):
                st.success(text["success_message"])
                st.session_state['form_submitted'] = True
                st.session_state['page'] = 'home'
                st.experimental_rerun()
            else:
                st.error("There was an error saving your review. Please try again.")

    if st.button(text["return_home"]):
        st.session_state['page'] = 'home'
        st.experimental_rerun()

def submit_review():
    """Ana uygulama fonksiyonu"""
    initialize_session_state()
    
    if st.session_state['page'] == 'home':
        display_home_page()
    else:
        display_review_form()

if __name__ == "__main__":
    submit_review()
