from django.test import TestCase
from unittest import skip
from extractor.utils import (
    generate_snippet,
    extract_dates,
    norm_cal_data,
    encap_poss_date
)


class TestEncapsulatePossibleDate(TestCase):
    def test_base_spelled_out_date(self):
        extracted_text = ["and", "then", "17",
                          "October", "2022", "with", "some"]
        month_index = 3
        result = encap_poss_date(month_index, extracted_text)
        self.assertEqual(result, "17 October 2022")

    def test_spelled_out_date_begin_str(self):
        extracted_text = ["17", "October", "2022", "with", "some"]
        month_index = 1
        result = encap_poss_date(month_index, extracted_text)
        self.assertEqual(result, "17 October 2022")

    def test_spelled_out_date_end_str(self):
        extracted_text = ["with", "some", "17", "October", "2022"]
        month_index = 3
        result = encap_poss_date(month_index, extracted_text)
        self.assertEqual(result, "17 October 2022")


class TestGenerateDateSnippet(TestCase):
    def test_generate_basic_snippet(self):
        # Test with
        date_index = 3
        extracted_text = ["Some", "with",
                          "Nicholas", "10/10/2021", "for", "text"]
        self.assertEqual("...with Nicholas 10/10/2021 for text...",
                         generate_snippet(date_index, extracted_text))

        # test JUST the date
        self.assertEqual("10/10/2021", generate_snippet(0, ["10/10/2021"]))

    def test_generate_snippet_with_date_at_beginning(self):
        date_index = 0
        # Test with full extracted_txt
        avge_len_extracted_txt = ["10/10/2021",
                                  "for", "text", "Nicholas", "some_more"]
        self.assertEqual("10/10/2021 for text Nicholas some_more...",
                         generate_snippet(date_index, avge_len_extracted_txt))

        # Test with smaller extracted_txt
        blw_len_extracted_txt = ["10/10/2021", "for", "text"]
        self.assertEqual("10/10/2021 for text",
                         generate_snippet(date_index, blw_len_extracted_txt))

    def test_generate_snippet_with_date_at_end(self):
        # Test with full snippet
        date_avg_len_index = 4
        avg_len_extrted = ["some_more",
                                   "for", "text", "Nicholas", "10/10/2021"]
        self.assertEqual("...some_more for text Nicholas 10/10/2021",
                         generate_snippet(date_avg_len_index, avg_len_extrted))

        # Test with smaller snippet
        date_blw_len_index = 2
        blw_len_extrted = ["text", "Nicholas", "10/10/2021"]
        self.assertEqual("text Nicholas 10/10/2021",
                         generate_snippet(date_blw_len_index, blw_len_extrted))


class TestExtractDates(TestCase):
    def setUp(self):
        self.file_name = 'testFileName.pdf'
        self.test_file_path = 'some_file_path'

    def test_initial_string(self):
        test_string = ("10/30/2019 Terms of Service | KTVU FOX 2 "
                       "https://www .ktvu.com/terms-of-service 1/21Terms"
                       " of Service Terms of Service")
        result = {}
        extract_dates(self.file_name, test_string, result, self.test_file_path)
        expected_result = {
            "testFileName.pdf_[tmp]_2019-10-30": {
                "date": "2019-10-30",
                "snippet": '10/30/2019 Terms of Service |...',
                "path": "some_file_path"
            }
        }
        self.assertEqual(expected_result, result)

    def test_extracting_date_with_dashes(self):
        test_string = "checking for the date: 10-10-2020 and I hope it works"
        result = {}
        extract_dates(self.file_name, test_string, result, self.test_file_path)
        expected_result = {
            "testFileName.pdf_[tmp]_2020-10-10": {
                "date": "2020-10-10",
                "snippet": '...the date: 10-10-2020 and I...',
                "path": "some_file_path"
            }
        }
        self.assertEqual(expected_result, result)

    def test_extracting_date_with_slashes(self):
        test_string = "checking for the date: 10/10/2020 and I hope it works"
        result = {}
        extract_dates(self.file_name, test_string, result, self.test_file_path)
        expected_result = {
            "testFileName.pdf_[tmp]_2020-10-10": {
                "date": "2020-10-10",
                "snippet": '...the date: 10/10/2020 and I...',
                "path": "some_file_path"
            }
        }
        self.assertEqual(expected_result, result)

    def test_multiple_dates_in_text(self):
        test_string = ("checking for the date: 10/10/2020 and some "
                       "other 10/20/2020 I hope it works")
        result = {}
        extract_dates(self.file_name, test_string, result, self.test_file_path)
        expected_result = {
            "testFileName.pdf_[tmp]_2020-10-10": {
                "date": "2020-10-10",
                "snippet": '...the date: 10/10/2020 and some...',
                "path": "some_file_path"
            },
            "testFileName.pdf_[tmp]_2020-10-20": {
                "date": "2020-10-20",
                "snippet": '...some other 10/20/2020 I hope...',
                "path": "some_file_path"
            }
        }
        self.assertEqual(expected_result, result)

    def test_multiple_snippets_under_one_date(self):
        test_string = ("checking for the date: 10/10/2020 and "
                       "some other 10/10/2020 I hope it works")
        result = {}
        extract_dates(self.file_name, test_string, result, self.test_file_path)
        expected_result = {
            "testFileName.pdf_[tmp]_2020-10-10": {
                "date": "2020-10-10",
                "snippet": ("...the date: 10/10/2020 and some...\n"
                            "...some other 10/10/2020 I hope..."),
                "path": "some_file_path"
            },
        }
        self.assertEqual(expected_result, result)

    def test_multiple_snippets_under_one_date_does_not_include_duplicates(self):
        test_string = "checking for the date: 10/10/2020 and some test test the date: 10/10/2020 and some it works"
        result = {}
        extract_dates(self.file_name, test_string, result, self.test_file_path)
        expected_result = {
            "testFileName.pdf_[tmp]_2020-10-10": {
                "date": "2020-10-10",
                "snippet": '...the date: 10/10/2020 and some...',
                "path": "some_file_path"
            },
        }
        self.assertEqual(expected_result, result)

    def test_extract_big_endian_date_with_slashes(self):
        test_string = ("2019/10/30 Terms of Service | KTVU FOX 2 "
                       "https://www .ktvu.com/terms-of-service 1/21Terms "
                       "of Service Terms of Service")
        result = {}
        extract_dates(self.file_name, test_string, result, self.test_file_path)
        expected_result = {
            "testFileName.pdf_[tmp]_2019-10-30": {
                "date": "2019-10-30",
                "snippet": '2019/10/30 Terms of Service |...',
                "path": "some_file_path"
            }
        }
        self.assertEqual(expected_result, result)

    def test_extract_big_endian_date_with_dashes(self):
        test_string = ("2019-10-30 Terms of Service | KTVU FOX 2 "
                       "https://www .ktvu.com/terms-of-service 1/21Terms "
                       "of Service Terms of Service")
        result = {}
        extract_dates(self.file_name, test_string, result, self.test_file_path)
        expected_result = {
            "testFileName.pdf_[tmp]_2019-10-30": {
                "date": "2019-10-30",
                "snippet": '2019-10-30 Terms of Service |...',
                "path": "some_file_path"
            }
        }
        self.assertEqual(expected_result, result)

    @skip("Skipping for now...")
    def test_extracting_date_with_full_month_spelled_out(self):
        test_string = "checking for date: October 10, 2020 and I hope it works"
        result = {}
        extract_dates(self.file_name, test_string, result, self.test_file_path)
        self.assertEqual("the date: October 10, 2020 and I", result)

    @skip("Skipping for now...")
    def test_extracting_date_with_partial_month_spelled_out(self):
        test_string = "checking for date: Oct 10, 2020 and I hope it works"
        result = {}
        extract_dates(self.file_name, test_string, result, self.test_file_path)
        self.assertEqual("the date: Oct 10, 2020 and I", result)

    @skip("Skipping for now...")
    def test_extracting_date_with_full_month_spelled_out_minus_space(self):
        test_string = "checking for date: Octorber 10,2020 and I hope it works"
        result = {}
        extract_dates(self.file_name, test_string, result, self.test_file_path)
        self.assertEqual("the date: Octorber 10,2020 and I", result)

    def test_extracting_day_month_year_spelled_out(self):
        test_string = "checking for date: 12 November 2022 and I hope it works"
        result = {}
        extract_dates(self.file_name, test_string, result, self.test_file_path)
        expected_result = {
            "testFileName.pdf_[tmp]_2022-11-12": {
                "date": "2022-11-12",
                "snippet": '...date: 12 November 2022 and...',
                "path": "some_file_path"
            }
        }
        self.assertEqual(expected_result, result)


class TestMassageExtractedDates(TestCase):
    def setUp(self):
        self.extracted_dates = {
            'test_file.pdf_[tmp]_2019-10-30': {
                'date': '2019-10-30',
                'snippet': '10/30/2019 Terms of Service |...',
                "path": "some_file_path"
            },
            'TestInsertMe.pdf_[tmp]_2020-11-11': {
                'date': '2020-11-11',
                'snippet': '11/11/2020 Iterating Over and Reducing...',
                "path": "some_file_path"
            }
        }

    def test_simple_massage(self):
        result = norm_cal_data(self.extracted_dates)
        expected_result = [
            {
                'name': 'test_file.pdf',
                'start': '2019-10-30',
                'color': '#2f5a89',
                'snippet': '10/30/2019 Terms of Service |...',
                "path": "some_file_path"

            },
            {
                'name': 'TestInsertMe.pdf',
                'start': '2020-11-11',
                'color': '#2f5a89',
                'snippet': '11/11/2020 Iterating Over and Reducing...',
                "path": "some_file_path"
            }
        ]
        self.assertEqual(expected_result, result)
