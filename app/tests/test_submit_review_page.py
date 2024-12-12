"""
python -m unittest app/tests/test_submit_review_page.py -v


Unit tests for the submit_review_page module.

- Rendering the header and ensuring correct navigation and language toggle.
- Handling form submission and verifying review creation.
- Rendering the review form and fetching company data.

"""

import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
from datetime import datetime
from app.submit_review_page import (
    render_header,
    handle_form_submission,
    render_review_form,
)


class TestSubmitReviewPage(unittest.TestCase):
    def setUp(self):
        st.session_state = {"language": "en", "page": "submit_review"}

    @patch("app.submit_review_page.st.experimental_rerun")
    @patch("app.submit_review_page.st.button")
    @patch("app.submit_review_page.st.columns")
    def test_render_header(self, mock_columns, mock_button, mock_rerun):
        mock_columns.return_value = [MagicMock(), MagicMock(), MagicMock()]

        mock_button.side_effect = [True, False]
        render_header()
        self.assertEqual(st.session_state["page"], "home")
        mock_rerun.assert_called_once()

        mock_button.side_effect = [False, True]
        render_header()
        self.assertEqual(st.session_state["language"], "tr")

    @patch("app.submit_review_page.create_review")
    def test_handle_form_submission(self, mock_create_review):
        mock_create_review.return_value = "123"  # Mocked review ID
        form_data = {
            "company_name": "Test Company",
            "review_text": "Great internship",
            "rating": 5,
            "salary": "5000",
            "department": "Engineering",
            "internship_role": "Software Developer",
            "project_quality": 4,
            "transportation": True,
            "remote_work": False,
            "meal_allowance": True,
            "technologies_used": "Python, SQL",
        }

        result = handle_form_submission(form_data)
        self.assertTrue(result)
        mock_create_review.assert_called_once()

    @patch("app.submit_review_page.get_companies")
    def test_render_review_form(self, mock_get_companies):
        mock_get_companies.return_value = ["Company A", "Company B"]

        render_review_form()
        mock_get_companies.assert_called_once()


if __name__ == "__main__":
    unittest.main()
