import re
from datetime import datetime

from .constants import (
    regex_mid_end_with_slashes,
    regex_mid_end_with_dashes,
    regex_big_end_with_slashes,
    regex_big_end_with_dashes,
    regex_lttle_end_spelled,
    full_month_regex,
    harbour_blue_hex,
    LENGTH_OF_SNIPPET,
    TRAIL_SNIP_TXT
)


def generate_snippet(index: int, extracted_text: list) -> str:
    """Generate a text snippet that contains date to be displayed

    args:
    index: The location of the date we have found in the array of
           extracted texts
    extracted_text: An array where each index is a word in the document
    """
    result = ""

    if LENGTH_OF_SNIPPET > len(extracted_text):
        result = ' '.join(extracted_text)
    else:
        offset = int(LENGTH_OF_SNIPPET / 2)
        # Date is in middle of extracted_text
        if (index in range(offset, len(extracted_text) - offset)):
            snippet = extracted_text[index - offset:index + offset + 1]
            result = TRAIL_SNIP_TXT + ' '.join(snippet) + TRAIL_SNIP_TXT
        elif index == 0:
            snippet = extracted_text[index:index + LENGTH_OF_SNIPPET + 1]
            result = ' '.join(snippet) + TRAIL_SNIP_TXT
        elif index == len(extracted_text) - 1:
            snippet = extracted_text[index - LENGTH_OF_SNIPPET:index + 1]
            result = TRAIL_SNIP_TXT + ' '.join(snippet)

    return result


def extract_dates(file_name: str, pdf_text: str,
                  dates_for_curr_pdf: dict, file_url: str):
    """Given pdf page will extract dates and update ongoing dict obj of dates

    In order to extract dates from the text we first must find them.
    To do that we use a variety of regex expressions in order to check.
    The current dates that we can pin down are as follows:

    little endian: day Month Year
    middle endian: MM/DD/YYYY, MM-DD-YYYY
    big endian: YYYY/MM/DD, YYYY-MM-DD

    When we find a date we store a snippet of the text with its date. We then
    create a obj in the ingoing dict of dates(dates_for_curr_pdf).

    args:
    file_name: name of pdf file
    pdf_text: string representation of a page of the pdf currently looking at
    dates_for_curr_pdf: a dict containing all dates found in current pdf so far
    file_url: url that links to server pdf preview
    """
    extracted_text = re.split(r"\s|\n", pdf_text)
    for index in range(len(extracted_text)):
        word = extracted_text[index]
        extracted_date = None
        # Have multiple regex since its easier to debug
        if re.match(regex_mid_end_with_slashes, word):
            extracted_date = extract_and_format_date(
                "%m/%d/%Y", regex_mid_end_with_slashes, word)

        elif re.match(regex_mid_end_with_dashes, word):
            extracted_date = extract_and_format_date(
                "%m-%d-%Y", regex_mid_end_with_dashes, word)

        elif re.match(regex_big_end_with_slashes, word):
            extracted_date = extract_and_format_date(
                "%Y/%m/%d", regex_big_end_with_slashes, word)

        elif re.match(regex_big_end_with_dashes, word):
            extracted_date = extract_and_format_date(
                "%Y-%m-%d", regex_big_end_with_dashes, word)

        elif re.match(full_month_regex, word):
            # Checking for spelled out dates
            poss_spelled_date = encap_poss_date(index, extracted_text)
            if re.match(regex_lttle_end_spelled, poss_spelled_date):
                extracted_date = extract_and_format_date(
                    "%d %B %Y", regex_lttle_end_spelled, poss_spelled_date)

        if extracted_date:
            file_date_key = file_name + '_[tmp]_' + str(extracted_date)
            generated_snippet = generate_snippet(index, extracted_text)
            if ((file_date_key in dates_for_curr_pdf) and
                    (generated_snippet not in
                     dates_for_curr_pdf[file_date_key]["snippet"])):
                dates_for_curr_pdf[file_date_key]["snippet"] += '\n' + \
                    generate_snippet(index, extracted_text)
            else:
                dates_for_curr_pdf[file_date_key] = {
                    "date": extracted_date,
                    "snippet": generate_snippet(index, extracted_text),
                    "path": file_url
                }


def encap_poss_date(index: int, extracted_text: list):
    """For cutting out spelled out dates in extracted text list

    index: The location of the date we have found in the array
    extracted_text: An array where each index is a word in the document
    """
    full_month_right_offset = 2
    full_month_left_offset = 1

    date_left = index - full_month_left_offset
    date_right = index + full_month_right_offset
    return ' '.join(extracted_text[date_left:date_right])


def extract_and_format_date(curr_date_format: str, regex: str, date: str):
    """Given a date format will convert date to a datetime object and then
       format to %Y-%m-%d(format needed by calendar widgit)

    curr_date_format: a datetime format code that matches date extracted.
                      This is needed in order to convert date to datetime obj
    regex: regex used to match the date
    date: string of the date we have found
    """
    regex_date = re.match(regex, date).string
    return datetime.strptime(regex_date, curr_date_format).strftime("%Y-%m-%d")


def norm_cal_data(extracted_dates: dict):
    """Given log of dates we have extracted from the PDFs we create a dict
       with a specific format that fits the calendar widgit we are using

    extracted_dates: log of all the dates we have collected in pdfs
    format as so:
    {
        'file_name.pdf_[tmp]_YYYY-MM-DD': {
            'date': 'YYYY-MM-DD',
            'snippet': 'YYYY-MM-DD some snippet text here...',
            "path": "url/path/to/preview/file"
        },
        ...
    }
    """
    result = []

    for key in extracted_dates.keys():
        obj = extracted_dates[key]
        split_key = key.split('_[tmp]_')
        result.append({
            'name': split_key[0],
            'start': split_key[1],
            'color': harbour_blue_hex,
            'snippet': obj.get('snippet'),
            'path': obj.get('path')
        })
    return result
