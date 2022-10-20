import re
from datetime import datetime

LENGTH_OF_SNIPPET = 4

# MM/DD/YYYY - middle endian
regex_mid_end_with_slashes = "(\d|\d{2})\/(\d|\d{2})\/(\d{4})"
regex_mid_end_with_dashes = "(\d|\d{2})-(\d|\d{2})-(\d{4})"

# YYYY/MM/DD - big endian
regex_big_end_with_slashes = "^(\d{4})\/(\d{1,2})\/(\d{1,2})$"
regex_big_end_with_dashes = "^(\d{4})-(\d{1,2})-(\d{1,2})$"

# DD MM YYYY - little endian with month spelled out
regex_lttle_end_spelled = r"^(\d{1,2})\s((\bJanuary)|(\bFebruary)|(\bMarch)|(\bApril)|(\bMay)|(\bJune)|(\bJuly)|(\bAugust)|(\bSeptember)|(\bOctober)|(\bNovember)|(\bDecember))\s(\d{4})"

full_month_regex = r"^((\bJanuary)|(\bFebruary)|(\bMarch)|(\bApril)|(\bMay)|(\bJune)|(\bJuly)|(\bAugust)|(\bSeptember)|(\bOctober)|(\bNovember)|(\bDecember))$"

harbour_blue_hex = '#2f5a89'


def generate_snippet(index, extracted_text):
    result = ""
    trail_snip_txt = '...'
    # variable to account for length of snippet. Can be adjusted to add more words to snippet
    if LENGTH_OF_SNIPPET > len(extracted_text):
        result = ' '.join(extracted_text)
    else:
        mid_snip_offset = int(LENGTH_OF_SNIPPET / 2)
        # Date is in middle of extracted_text
        if (index in range(mid_snip_offset, len(extracted_text) - mid_snip_offset)):
            # Do an add 1 at the end to account for index offset
            result = trail_snip_txt + ' '.join(extracted_text[index - mid_snip_offset:index + mid_snip_offset + 1]) + trail_snip_txt
        elif index == 0:
            result = ' '.join(extracted_text[index:index + LENGTH_OF_SNIPPET + 1]) + trail_snip_txt
        elif index == len(extracted_text) - 1:
            result = trail_snip_txt + ' '.join(extracted_text[index - LENGTH_OF_SNIPPET:index + 1])

    return result


def extract_dates(file_name, pdf_text, dates_for_curr_pdf, file_url):
    extracted_text = pdf_text.split(' ')
    for index in range(len(extracted_text)):
        word = extracted_text[index]
        extracted_date = None
        # Have multiple regex since its easier to debug
        if re.match(regex_mid_end_with_slashes, word):
            regex_date = re.match(regex_mid_end_with_slashes, word).string
            extracted_date = datetime.strptime(regex_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        elif re.match(regex_mid_end_with_dashes, word):
            regex_date = re.match(regex_mid_end_with_dashes, word).string
            extracted_date = datetime.strptime(regex_date, "%m-%d-%Y").strftime("%Y-%m-%d")
        elif re.match(regex_big_end_with_slashes, word):
            regex_date = re.match(regex_big_end_with_slashes, word).string
            extracted_date = datetime.strptime(regex_date, "%Y/%m/%d").strftime("%Y-%m-%d")
        elif re.match(regex_big_end_with_dashes, word):
            regex_date = re.match(regex_big_end_with_dashes, word).string
            extracted_date = datetime.strptime(regex_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        elif re.match(full_month_regex, word):
            # Checking for spelled out dates
            poss_spelled_date = encap_poss_date(index, extracted_text)
            if re.match(regex_lttle_end_spelled, poss_spelled_date):
                regex_date = re.match(regex_lttle_end_spelled, poss_spelled_date).string
                extracted_date = datetime.strptime(regex_date, "%d %B %Y").strftime("%Y-%m-%d")

        if extracted_date:
            file_date_key = file_name + '_[tmp]_' + str(extracted_date)
            generated_snippet = generate_snippet(index, extracted_text)
            if (file_date_key in dates_for_curr_pdf) and (generated_snippet not in dates_for_curr_pdf[file_date_key]["snippet"]):
                dates_for_curr_pdf[file_date_key]["snippet"] += '\n' + generate_snippet(index, extracted_text)
            else:
                dates_for_curr_pdf[file_date_key] = {
                    "date": extracted_date,
                    "snippet": generate_snippet(index, extracted_text),
                    "path": file_url
                }


def encap_poss_date(index, extracted_text):
    full_month_right_offset = 2
    full_month_left_offset = 1

    return ' '.join(extracted_text[index - full_month_left_offset:index + full_month_right_offset])

def extract_and_format_date(date_format, regex, word):
    regex_date = re.match(regex, word).string
    return datetime.strptime(regex_date, date_format).strftime("%Y-%m-%d")


def massage_calendar_dates(extracted_dates):
    result = []
    file_date_keys = extracted_dates.keys()
    print(file_date_keys)

    for key in file_date_keys:
        obj = extracted_dates[key]
        print(obj)
        split_key = key.split('_[tmp]_')
        result.append({
            'name': split_key[0],
            'start': split_key[1],
            'color': harbour_blue_hex,
            'snippet': obj.get('snippet'),
            'path': obj.get('path')
        })
    return result
