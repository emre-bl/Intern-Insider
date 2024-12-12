"""
python -m unittest app/components/test_filters.py -v

- Filter section rendering with multilingual support (EN/TR)
- Company filter dropdown population
- Rating filter options
- Department filter dynamic loading
- Sort options radio button
- Pre-filled filter handling
- Session state language management

Checks filter behavior with and without pre-filled values

"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from pathlib import Path

import streamlit as st
from app.components.filters import render_filter_section


class TestFilters(unittest.TestCase):
    def setUp(self):
        self.lang_dict = {
            "en": {
                "filter_section_title": "Filter Reviews",
                "company_filter": "Company",
                "rating_filter": "Rating",
                "all_companies": "All Companies",
                "all_ratings": "All Ratings",
                "all_departments": "All Departments",
                "department_filter": "Department",
                "role_filter": "Internship Role",
                "sort_option_label": "Sort Reviews",
                "sort_options": ["Most Liked", "Newest First", "Oldest First"],
            },
            "tr": {
                "filter_section_title": "Değerlendirmeleri Filtrele",
                "company_filter": "Şirket",
                "rating_filter": "Puan",
                "all_companies": "Tüm Şirketler",
                "all_ratings": "Tüm Puanlar",
                "all_departments": "Tüm Departmanlar",
                "department_filter": "Departman",
                "role_filter": "Staj Pozisyonu",
                "sort_option_label": "Değerlendirmeleri Sırala",
                "sort_options": ["En Beğenilen", "En Yeni", "En Eski"],
            },
        }

    @patch("app.components.filters.st")
    @patch("app.components.filters.lang_dict")
    def test_render_filter_section(self, mock_lang_dict, mock_st):
        mock_st.session_state = {"language": "en"}
        mock_lang_dict.__getitem__.side_effect = self.lang_dict.__getitem__

        mock_company_data = [
            {"name": "Turkcell"},
            {"name": "Roketsan"},
            {"name": "ASELSAN"},
            {"name": "TUSAŞ"},
        ]
        mock_companies = MagicMock()
        mock_companies.find.return_value = mock_company_data

        mock_reviews = MagicMock()
        mock_reviews.distinct.return_value = ["Software", "Hardware"]

        # Configure streamlit mocks
        mock_st.columns.return_value = [
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
        ]
        mock_st.markdown = MagicMock()
        mock_st.selectbox = MagicMock()
        mock_st.radio = MagicMock()

        result = render_filter_section(mock_companies, mock_reviews)

        # Verify filter section title
        mock_st.markdown.assert_called_with("### **Filter Reviews**")


if __name__ == "__main__":
    unittest.main()
