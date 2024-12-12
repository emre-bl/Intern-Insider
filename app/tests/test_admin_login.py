"""
python -m unittest app/tests/test_admin_login.py -v


Unit tests for the admin_login module.

- Testing successful and unsuccessful login attempts.
- Checking the proper handling of language localization.
- Ensuring that session state variables are correctly updated.
- Mocking external dependencies to isolate the testing environment.
"""

import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
from app.admin_login import render_header, admin_login


class TestAdminLogin(unittest.TestCase):
    def setUp(self):
        self.test_lang_dict = {
            "en": {
                "admin_login_title": "Admin Login",
                "home_button": "🏠 Home",
                "username_label": "Username",
                "password_label": "Password",
                "login_button": "Login",
                "login_success": "Login successful!",
                "login_failed": "Invalid username or password.",
                "db_connection_error": "Database connection failed.",
                "already_logged_in": "Admin is already logged in!",
                "unexpected_error": "An unexpected error occurred",
            },
            "tr": {
                "admin_login_title": "Admin Girişi",
                "home_button": "🏠 Anasayfa",
                "username_label": "Kullanıcı Adı",
                "password_label": "Şifre",
                "login_button": "Giriş Yap",
                "login_success": "Giriş başarılı!",
                "login_failed": "Geçersiz kullanıcı adı veya şifre.",
                "db_connection_error": "Veritabanı bağlantısı başarısız.",
                "already_logged_in": "Admin halihazırda giriş yapmış!",
                "unexpected_error": "Beklenmedik bir hata oluştu",
            },
        }
        st.session_state = {"language": "en", "page": "admin_login", "is_admin": False}

    @patch("app.admin_login.render_header")  # Mock render_header to avoid rerun
    @patch("app.admin_login.st.experimental_rerun")
    @patch("app.admin_login.st.text_input")
    @patch("app.admin_login.st.button")
    @patch("app.admin_login.st.success")
    @patch("app.admin_login.st.error")
    def test_admin_login_functionality(
        self,
        mock_error,
        mock_success,
        mock_button,
        mock_text_input,
        mock_rerun,
        mock_render_header,
    ):
        with patch("app.admin_login.lang_dict", self.test_lang_dict):
            # login doğru ise

            mock_text_input.side_effect = ["admin", "password123"]
            mock_button.return_value = True
            mock_admin_data = {"admin_id": "admin", "password": "password123"}

            with patch("app.admin_login.connect_to_collection") as mock_db:
                mock_db.return_value = MagicMock()
                mock_db.return_value.find_one.return_value = mock_admin_data

                st.session_state["language"] = "en"
                admin_login()
                mock_success.assert_called_with(
                    self.test_lang_dict["en"]["login_success"]
                )
                self.assertTrue(st.session_state["is_admin"])

            mock_text_input.reset_mock()
            mock_text_input.side_effect = ["wrong_user", "wrong_pass"]
            mock_button.return_value = True
            mock_success.reset_mock()
            mock_error.reset_mock()

            with patch("app.admin_login.connect_to_collection") as mock_db:
                mock_db.return_value = MagicMock()
                mock_db.return_value.find_one.return_value = None

                st.session_state["language"] = "tr"
                st.session_state["is_admin"] = False  # Reset admin state
                admin_login()

                # Verify Turkish error message
                mock_error.assert_called_once_with(
                    self.test_lang_dict["tr"]["login_failed"]
                )
                self.assertFalse(st.session_state["is_admin"])

    @patch("app.admin_login.st.success")
    @patch("app.admin_login.st.experimental_rerun")
    def test_already_logged_in(self, mock_rerun, mock_success):
        with patch("app.admin_login.lang_dict", self.test_lang_dict):
            st.session_state["is_admin"] = True
            st.session_state["language"] = "en"
            admin_login()
            mock_success.assert_called_with(
                self.test_lang_dict["en"]["already_logged_in"]
            )


if __name__ == "__main__":
    unittest.main()
