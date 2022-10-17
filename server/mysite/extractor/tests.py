from django.test import TestCase
from extractor.utils import generate_snippet, extract_dates


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
    # IN PROGRESS UNIT TEST SUITE
    def test_initial_string(self):
        test_string = "10/30/2019 Terms of Service | KTVU FOX 2 https://www .ktvu.com/terms-of-service 1/21Terms of Service Terms of Service"
        self.assertEqual("10/30/2019 Terms of Service |", extract_dates(test_string))

    def test_extracting_date_with_dashes(self):
        test_string = "In some string I am checking for the date: 10-10-2020 and I hope it works"
        self.assertEqual("the date: 10-10-2020 and I", extract_dates(test_string))

    def test_extracting_date_with_slashes(self):
        test_string = "In some string I am checking for the date: 10/10/2020 and I hope it works"
        self.assertEqual("the date: 10/10/2020 and I", extract_dates(test_string))

    def test_extracting_date_with_full_month_spelled_out(self):
        test_string = "In some string I am checking for the date: October 10, 2020 and I hope it works"
        self.assertEqual("the date: October 10, 2020 and I", extract_dates(test_string))

    def test_extracting_date_with_partial_month_spelled_out(self):
        test_string = "In some string I am checking for the date: Oct 10, 2020 and I hope it works"
        self.assertEqual("the date: Oct 10, 2020 and I", extract_dates(test_string))

    def test_extracting_date_with_full_month_spelled_out_minus_space(self):
        test_string = "In some string I am checking for the date: Octorber 10,2020 and I hope it works"
        self.assertEqual("the date: Octorber 10,2020 and I", extract_dates(test_string))
