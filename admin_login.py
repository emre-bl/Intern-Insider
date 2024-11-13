import streamlit as st

def admin_login():
    st.title("Admin Girişi")

    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    
    if st.button("Giriş Yap"):
        """
        Veri tabanına bağlandığında burayı değiştir.
        """
        if username == "admin" and password == "admin123":  # Örnek giriş bilgileri
            st.success("Giriş başarılı!")
            st.session_state["is_admin"] = True
            st.session_state["page"] = "home"  # Başarılı giriş sonrası ana sayfaya yönlendirme
            st.experimental_rerun()
        else:
            st.error("Geçersiz kullanıcı adı veya şifre.")
    
    if st.button("Ana Sayfaya Geri Dön"):
        st.session_state["page"] = "home"
        st.experimental_rerun()

if __name__ == "__main__":
    admin_login()
