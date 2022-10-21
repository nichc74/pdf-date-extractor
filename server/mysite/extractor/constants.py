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