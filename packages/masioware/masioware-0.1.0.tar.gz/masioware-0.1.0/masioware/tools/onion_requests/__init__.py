from requests import Session


def requests_tor_session():

    tor_session = Session()

    tor_session.proxies = {
        'http': 'socks5h://localhost:9050',
        'https': 'socks5h:/localhost:9050',
    }

    return tor_session
