import streamlit as st
from backend.db_connection import connect_to_collection

def admin_login():
    st.title("Admin Girişi")

    # Kullanıcı giriş bilgileri
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    
    if st.button("Giriş Yap"):
        try:
            # Admin koleksiyonuna bağlan
            admin_collection = connect_to_collection("admin")
            if admin_collection is None:
                st.error("Veri tabanına bağlanılamadı. Lütfen daha sonra tekrar deneyin.")
                return

            # Kullanıcı bilgilerini kontrol et
            admin_user = admin_collection.find_one({"admin_id": username, "password": password})
            if admin_user:
                st.success("Giriş başarılı!")
                st.session_state["is_admin"] = True
                st.session_state["page"] = "home"  # Başarılı giriş sonrası ana sayfaya yönlendirme
                st.experimental_rerun()
            else:
                st.error("Geçersiz kullanıcı adı veya şifre.")
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

    # Ana sayfaya geri dönme seçeneği
    if st.button("Ana Sayfaya Geri Dön"):
        st.session_state["page"] = "home"
        st.experimental_rerun()

if __name__ == "__main__":
    admin_login()
