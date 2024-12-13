import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
from app.home_page import apply_custom_css, render_navbar, lang_dict


class TestHomePage(unittest.TestCase):
    def setUp(self):
        # Initialize session state with default values for consistent testing
        st.session_state = {
            "language": "en",  # Default
            "page": "home",  # default page state
        }

    @patch("app.home_page.st.markdown")
    def test_apply_custom_css(self, mock_markdown):
        """
        Test that apply_custom_css() function:
        1. Calls st.markdown() method
        2. Includes a <style> tag in the markdown content
        Ensures that custom CSS styles are being applied correctly to the Streamlit app
        """
        apply_custom_css()
        mock_markdown.assert_called_once()  # Checks if markdown was called exactly once
        self.assertIn(
            "<style>", mock_markdown.call_args[0][0]
        )  # Verifies style tag is present

    @patch("app.home_page.st")
    def test_render_navbar(self, mock_st):
        """
        Test that render_navbar() function:
        1. Renders the navigation bar correctly
        2. Calls st.image() to display the logo
        3. Creates the expected number of columns
        4. Creates navigation buttons

        Key checks include:
        - Logo is displayed with correct path and width
        - Buttons are created (though not checking specific button interactions)
        - Function runs without raising unexpected exceptions
        """
        mock_st.columns.return_value = [MagicMock() for _ in range(6)]
        mock_st.image = MagicMock()
        mock_st.experimental_rerun = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.session_state = {
            "language": "en",  # Ensure a valid language
            "page": "home",
        }

        with patch("app.home_page.st.session_state", mock_st.session_state):
            render_navbar()

            mock_st.image.assert_called_once_with(
                "app/assets/intern-insider-compact-logo.svg", width=100
            )

            mock_st.button.assert_called()


if __name__ == "__main__":
    unittest.main()
