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


def generate_snippet(index, extracted_text):
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


def extract_dates(file_name, pdf_text, dates_for_curr_pdf, file_url):
    extracted_text = pdf_text.split(' ')
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


def encap_poss_date(index, extracted_text):
    full_month_right_offset = 2
    full_month_left_offset = 1

    date_left = index - full_month_left_offset
    date_right = index + full_month_right_offset
    return ' '.join(extracted_text[date_left:date_right])


def extract_and_format_date(date_format, regex, word):
    regex_date = re.match(regex, word).string
    return datetime.strptime(regex_date, date_format).strftime("%Y-%m-%d")


def massage_calendar_dates(extracted_dates):
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
