from urllib.parse import urlparse

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)


def validate_item(item):
    expected_keys = {"commission_name": str, "agenda_link": str}
    for key, expected_type in expected_keys.items():
        if key not in item or not isinstance(item[key], expected_type):
            return False
        if key == "agenda_link" and not is_valid_url(item[key]):
            return False
    return True 