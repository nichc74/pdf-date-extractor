from django.test import TestCase
from unittest import skip
from extractor.utils import (
    generate_snippet,
    extract_dates,
    massage_calendar_dates
)


class TestGenerateDateSnippet(TestCase):
    def test_generate_basic_snippet(self):
        # Test with
        date_index = 3
        extracted_text = ["Some", "with", "Nicholas", "10/10/2021", "for", "text"]
        self.assertEqual("with Nicholas 10/10/2021 for text", generate_snippet(date_index, extracted_text))

        # test JUST the date
        self.assertEqual("10/10/2021", generate_snippet(0, ["10/10/2021"]))

    def test_generate_snippet_with_date_at_beginning(self):
        date_index = 0
        # Test with full extracted_txt
        avge_len_extracted_txt = ["10/10/2021", "for", "text", "Nicholas", "some_more"]
        self.assertEqual("10/10/2021 for text Nicholas some_more", generate_snippet(date_index, avge_len_extracted_txt))

        # Test with smaller extracted_txt
        blw_len_extracted_txt = ["10/10/2021", "for", "text"]
        self.assertEqual("10/10/2021 for text", generate_snippet(date_index, blw_len_extracted_txt))

    def test_generate_snippet_with_date_at_end(self):
        # Test with full snippet
        date_avg_len_index = 4
        avge_len_extracted_text = ["some_more", "for", "text", "Nicholas", "10/10/2021"]
        self.assertEqual("some_more for text Nicholas 10/10/2021", generate_snippet(date_avg_len_index, avge_len_extracted_text))

        # Test with smaller snippet
        date_blw_len_index = 2
        blw_len_extracted_text = ["text", "Nicholas", "10/10/2021"]
        self.assertEqual("text Nicholas 10/10/2021", generate_snippet(date_blw_len_index, blw_len_extracted_text))


class TestExtractDates(TestCase):
    def setUp(self):
        self.file_name = 'testFileName.pdf'

    # IN PROGRESS UNIT TEST SUITE
    def test_initial_string(self):
        test_string = "10/30/2019 Terms of Service | KTVU FOX 2 https://www .ktvu.com/terms-of-service 1/21Terms of Service Terms of Service"
        result = {}
        extract_dates(self.file_name, test_string, result)
        expected_result = {
            "testFileName.pdf_[tmp]_2019/10/30": {
                "date": "2019/10/30",
                "snippet": '10/30/2019 Terms of Service |'
            }
        }
        self.assertEqual(expected_result, result)

    def test_extracting_date_with_dashes(self):
        test_string = "checking for the date: 10-10-2020 and I hope it works"
        result = {}
        extract_dates(self.file_name, test_string, result)
        expected_result = {
            "testFileName.pdf_[tmp]_2020/10/10": {
                "date": "2020/10/10",
                "snippet": 'the date: 10-10-2020 and I'
            }
        }
        self.assertEqual(expected_result, result)

    def test_extracting_date_with_slashes(self):
        test_string = "checking for the date: 10/10/2020 and I hope it works"
        result = {}
        extract_dates(self.file_name, test_string, result)
        expected_result = {
            "testFileName.pdf_[tmp]_2020/10/10": {
                "date": "2020/10/10",
                "snippet": 'the date: 10/10/2020 and I'
            }
        }
        self.assertEqual(expected_result, result)
    
    def test_multiple_dates_in_text(self):
        test_string = "checking for the date: 10/10/2020 and some other 10/20/2020 I hope it works"
        result = {}
        extract_dates(self.file_name, test_string, result)
        expected_result = {
            "testFileName.pdf_[tmp]_2020/10/10": {
                "date": "2020/10/10",
                "snippet": 'the date: 10/10/2020 and some'
            },
            "testFileName.pdf_[tmp]_2020/10/20": {
                "date": "2020/10/20",
                "snippet": 'some other 10/20/2020 I hope'
            }
        }
        self.assertEqual(expected_result, result)
    
    def test_multiple_snippets_under_one_date(self):
        test_string = "checking for the date: 10/10/2020 and some other 10/10/2020 I hope it works"
        result = {}
        extract_dates(self.file_name, test_string, result)
        expected_result = {
            "testFileName.pdf_[tmp]_2020/10/10": {
                "date": "2020/10/10",
                "snippet": 'the date: 10/10/2020 and some\nsome other 10/10/2020 I hope'
            },
        }
        self.assertEqual(expected_result, result)

    def test_multiple_snippets_under_one_date_does_not_include_duplicates(self):
        test_string = "checking for the date: 10/10/2020 and some test test the date: 10/10/2020 and some it works"
        result = {}
        extract_dates(self.file_name, test_string, result)
        expected_result = {
            "testFileName.pdf_[tmp]_2020/10/10": {
                "date": "2020/10/10",
                "snippet": 'the date: 10/10/2020 and some'
            },
        }
        self.assertEqual(expected_result, result)

    @skip("Skipping for now...")
    def test_extracting_date_with_full_month_spelled_out(self):
        test_string = "checking for the date: October 10, 2020 and I hope it works"
        result = {}
        extract_dates(self.file_name, test_string, result)
        self.assertEqual("the date: October 10, 2020 and I", result)

    @skip("Skipping for now...")
    def test_extracting_date_with_partial_month_spelled_out(self):
        test_string = "checking for the date: Oct 10, 2020 and I hope it works"
        result = {}
        extract_dates(self.file_name, test_string, result)
        self.assertEqual("the date: Oct 10, 2020 and I", result)

    @skip("Skipping for now...")
    def test_extracting_date_with_full_month_spelled_out_minus_space(self):
        test_string = "checking for the date: Octorber 10,2020 and I hope it works"
        result = {}
        extract_dates(self.file_name, test_string, result)
        self.assertEqual("the date: Octorber 10,2020 and I", result)


class TestMassageExtractedDates(TestCase):
    def setUp(self):
        self.extracted_dates = {
            'test_file.pdf_[tmp]_10/30/2019': {
                'date': '10/30/2019', 'snippet': '10/30/2019 Terms of Service |'
            },
            'TestInsertMe.pdf_[tmp]_11/11/2020': {
                'date': '11/11/2020', 'snippet': '11/11/2020 Iterating Over and Reducing'
            }
        }
    
    def test_simple_massage(self):
        result = massage_calendar_dates(self.extracted_dates)
        expected_result = [
            {
                'name': 'test_file.pdf',
                'start': '10/30/2019',
                'color': '#2f5a89',
                'snippet': '10/30/2019 Terms of Service |'
            },
            {
                'name': 'TestInsertMe.pdf',
                'start': '11/11/2020',
                'color': '#2f5a89',
                'snippet': '11/11/2020 Iterating Over and Reducing'
            }
        ]
        self.assertEqual(expected_result, result)
    

