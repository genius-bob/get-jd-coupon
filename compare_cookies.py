from trillworks import cookies, headers, params


def compare_cookies(cookies3, cookies2):
    compare_result = {}
    for k, v in cookies3.items():
        if v != cookies2.get(k, ''):
            compare_result[k] = [
                v,
                cookies2.get(k, ''),
            ]
    return compare_result

