from requests import get
from hashlib import sha1
from collections import defaultdict
from sys import argv


def request_api_data(query_char):
    first_five_hex_chars = query_char[:5]
    url = 'https://api.pwnedpasswords.com/range/' + first_five_hex_chars
    response = get(url)

    if response.status_code != 200:
        raise RuntimeError(
            'Something went wrong with the API. Try again in a minute.')

    pass_dict = defaultdict(
        int,
        {first_five_hex_chars + k: v for
            k, v in [pair.split(':') for pair in response.text.splitlines()]}
    )

    return pass_dict[query_char]


def pwned_api_check(password):
    m = sha1()
    m.update(password.encode())
    return request_api_data(m.hexdigest().upper())


passwords = argv[1:]

for password in passwords:
    result = pwned_api_check(password)
    print(f'{password} has been pwned {result} times')
