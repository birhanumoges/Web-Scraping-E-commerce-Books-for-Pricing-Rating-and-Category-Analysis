import re
def clean_price(price_text):
    return float(price_text.replace('£', '').strip())
    # keep only digits and dot
    number = re.sub(r'[^0-9.]', '', price_text)
    return float(number)

def convert_rating(rating_class):
    mapping = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    for key in mapping:
        if key in rating_class:
            return mapping[key]
    return 0
