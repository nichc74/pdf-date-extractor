import re
from datetime import datetime

LENGTH_OF_SNIPPET = 4

regex_date_with_slashes = "(\d|\d{2})\/(\d|\d{2})\/(\d{4})"
regex_date_with_dashes = "(\d|\d{2})-(\d|\d{2})-(\d{4})"
harbour_blue_hex = '#2f5a89'

def generate_snippet(index, extracted_text):
    result = ""
    # variable to account for length of snippet. Can be adjusted to add more words to snippet
    if LENGTH_OF_SNIPPET > len(extracted_text):
        result = ' '.join(extracted_text)
    else:
        mid_snip_offset = int(LENGTH_OF_SNIPPET / 2)
        # Date is in middle of extracted_text
        if (index in range(mid_snip_offset, len(extracted_text) - mid_snip_offset)):
            # Do an add 1 at the end to account for index offset
            result = ' '.join(extracted_text[index - mid_snip_offset:index + mid_snip_offset + 1])
        elif index == 0:
            result = ' '.join(extracted_text[index:index + LENGTH_OF_SNIPPET + 1])
        elif index == len(extracted_text) - 1:
            result = ' '.join(extracted_text[index - LENGTH_OF_SNIPPET:index + 1])

    return result

def extract_dates(file_name, pdf_text, dates_for_curr_pdf):
    extracted_text = pdf_text.split(' ')
    for index in range(len(extracted_text)):
        word = extracted_text[index]
        extracted_date = None
        # Have multiple regex since its easier to debug
        if re.match(regex_date_with_slashes, word):
            regex_date = re.match(regex_date_with_slashes, word).string
            extracted_date = datetime.strptime(regex_date, "%m/%d/%Y").strftime("%Y/%m/%d")
        elif re.match(regex_date_with_dashes, word):
            regex_date = re.match(regex_date_with_dashes, word).string
            extracted_date = datetime.strptime(regex_date, "%m-%d-%Y").strftime("%Y/%m/%d")

        if extracted_date:
            file_date_key = file_name + '_[tmp]_' + str(extracted_date)
            generated_snippet = generate_snippet(index, extracted_text)
            if (file_date_key in dates_for_curr_pdf) and (generated_snippet not in dates_for_curr_pdf[file_date_key]["snippet"]):
                dates_for_curr_pdf[file_date_key]["snippet"] += '\n' + generate_snippet(index, extracted_text)
            else:
                dates_for_curr_pdf[file_date_key] = {
                    "date": extracted_date,
                    "snippet": generate_snippet(index, extracted_text)
                }


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
            'snippet': obj.get('snippet')
        })
    return result
