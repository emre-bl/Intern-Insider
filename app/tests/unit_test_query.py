# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 21:54:51 2024

@author: Ezgi
"""

import unittest
import re
from datetime import datetime
from backend.queries import build_reviews_query, sort_reviews
import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_reviews_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


class TestBuildReviewsQuery(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        data_file_path = os.path.join(
            PROJECT_ROOT, "app/tests/data/mydatabase.reviews.json"
        )
        cls.test_reviews = load_reviews_from_file(data_file_path)

    def test_no_filters(self):
        # Hiç filtre verilmediğinde
        result = build_reviews_query()
        expected = {"admin_approved": True}
        self.assertEqual(result, expected)

    def test_company_filter(self):
        # Sadece company_filter kullanıldığında
        result = build_reviews_query(company_filter="Acme Corp")
        expected = {"admin_approved": True, "company_name": "Acme Corp"}
        self.assertEqual(result, expected)

    def test_rating_filter(self):
        # Sadece rating_filter kullanıldığında
        result = build_reviews_query(rating_filter="5")
        expected = {"admin_approved": True, "rating": 5}
        self.assertEqual(result, expected)

    def test_department_filter(self):
        # Sadece department_filter kullanıldığında
        result = build_reviews_query(department_filter="Engineering")
        expected = {"admin_approved": True, "department": "Engineering"}
        self.assertEqual(result, expected)

    def test_internship_role_filter(self):
        # Sadece internship_role_filter kullanıldığında
        result = build_reviews_query(internship_role_filter="developer")
        expected = {
            "admin_approved": True,
            "internship_role": {"$regex": "developer", "$options": "i"},
        }
        self.assertEqual(result, expected)

    def test_multiple_filters(self):
        # Birden fazla filtre birlikte kullanıldığında
        result = build_reviews_query(
            company_filter="Acme Corp",
            rating_filter="4",
            department_filter="Engineering",
            internship_role_filter="developer",
        )
        expected = {
            "admin_approved": True,
            "company_name": "Acme Corp",
            "rating": 4,
            "department": "Engineering",
            "internship_role": {"$regex": "developer", "$options": "i"},
        }
        self.assertEqual(result, expected)

    def test_ignore_default_filters(self):
        # Varsayılan filtrelerin all değerleri dikkate alınmamalı
        result = build_reviews_query(
            company_filter="All Companies",
            rating_filter="All Ratings",
            department_filter="All Departments",
            internship_role_filter=None,
        )
        expected = {"admin_approved": True}
        self.assertEqual(result, expected)

    def test_no_filters_with_data(self):
        query = build_reviews_query()
        expected_result = [
            review for review in self.test_reviews if review["admin_approved"] == True
        ]
        matched_reviews = [
            review
            for review in self.test_reviews
            if all(query[key] == review[key] for key in query if key in review)
        ]

        self.assertEqual(matched_reviews, expected_result)

    def test_company_filter_with_data(self):
        query = build_reviews_query(company_filter="Turkcell")
        expected_result = [
            review
            for review in self.test_reviews
            if review["company_name"] == "Turkcell" and review["admin_approved"] == True
        ]

        matched_reviews = [
            review
            for review in self.test_reviews
            if all(query[key] == review[key] for key in query if key in review)
        ]

        self.assertEqual(matched_reviews, expected_result)

    def test_rating_filter_with_data(self):
        # 5 star ratings
        query = build_reviews_query(rating_filter="5")
        expected_result = [
            review
            for review in self.test_reviews
            if review["rating"] == 5 and review["admin_approved"] == True
        ]

        matched_reviews = [
            review
            for review in self.test_reviews
            if all(query[key] == review[key] for key in query if key in review)
        ]

        self.assertEqual(matched_reviews, expected_result)

    def test_department_filter_with_data(self):
        query = build_reviews_query(department_filter="Logistics")
        expected_result = [
            review
            for review in self.test_reviews
            if review["department"] == "Logistics" and review["admin_approved"] == True
        ]

        matched_reviews = [
            review
            for review in self.test_reviews
            if all(query[key] == review[key] for key in query if key in review)
        ]

        self.assertEqual(matched_reviews, expected_result)

    def test_internship_role_filter_with_data(self):
        query = build_reviews_query(internship_role_filter="Data Analyst Intern")
        expected_result = [
            review
            for review in self.test_reviews
            if "Data Analyst Intern".lower() in review["internship_role"].lower()
            and review["admin_approved"] == True
        ]

        # MongoDB Regex sorgusu icin
        matched_reviews = [
            review
            for review in self.test_reviews
            if all(
                (
                    (
                        isinstance(query[key], dict)
                        and "$regex" in query[key]
                        and re.search(query[key]["$regex"], review[key], re.IGNORECASE)
                    )
                    if isinstance(query[key], dict)
                    else (query[key] == review[key])
                )
                for key in query
                if key in review and query[key] is not None
            )
        ]

        self.assertEqual(matched_reviews, expected_result)

    def test_sort_reviews(self):
        """Test sorting functionality."""
        # Most Liked
        max_like_count = max(review["like_count"] for review in self.test_reviews)
        min_like_count = min(review["like_count"] for review in self.test_reviews)
        sorted_reviews = sort_reviews(self.test_reviews, "Most Liked")
        self.assertEqual(
            sorted_reviews[0]["like_count"],
            max_like_count,
            "Most liked review is not at the top",
        )
        self.assertEqual(
            sorted_reviews[-1]["like_count"],
            min_like_count,
            "Least liked review is not at the bottom",
        )

        # Newest First
        sorted_reviews = sort_reviews(self.test_reviews, "Newest First")
        for i in range(1, len(sorted_reviews)):
            current_date = datetime.strptime(
                sorted_reviews[i]["feedback_date"], "%d/%m/%Y"
            )
            previous_date = datetime.strptime(
                sorted_reviews[i - 1]["feedback_date"], "%d/%m/%Y"
            )
            self.assertGreaterEqual(
                previous_date, current_date, "Reviews are not sorted by newest first"
            )

        # Oldest First
        sorted_reviews = sort_reviews(self.test_reviews, "Oldest First")
        for i in range(1, len(sorted_reviews)):
            current_date = datetime.strptime(
                sorted_reviews[i]["feedback_date"], "%d/%m/%Y"
            )
            previous_date = datetime.strptime(
                sorted_reviews[i - 1]["feedback_date"], "%d/%m/%Y"
            )
            self.assertLessEqual(
                previous_date, current_date, "Reviews are not sorted by oldest first"
            )


if __name__ == "__main__":
    unittest.main()
