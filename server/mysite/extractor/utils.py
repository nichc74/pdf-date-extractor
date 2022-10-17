import re

LENGTH_OF_SNIPPET = 4

regex_date_with_slashes = "(\d|\d{2})\/(\d|\d{2})\/(\d{4})"
regex_date_with_dashes = "(\d|\d{2})-(\d|\d{2})-(\d{4})"

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


def extract_dates(input_string):
    extracted_text = input_string.split(' ')
    result = {}
    for index in range(len(extracted_text)):
        word = extracted_text[index]
        extracted_date = None
        # Have multiple regex since its easier to debug
        if re.match(regex_date_with_slashes, word):
            extracted_date = re.match(regex_date_with_slashes, word).string
        elif re.match(regex_date_with_dashes, word):
            extracted_date = re.match(regex_date_with_dashes, word).string

        if extracted_date and extracted_date not in result:
            result[str(extracted_date)] = {
                "date": extracted_date,
                "snippet": generate_snippet(index, extracted_text)
            }
    return result
