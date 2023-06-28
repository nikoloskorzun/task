import requests

test_domain = 'https://example.org'


def check_proxy(proxy_addr: dict[str, str]) -> bool:
    try:
        ans = requests.get(test_domain, proxies=proxy_addr, timeout=3)
        if ans.status_code == 200:
            return True
        return False
    except:
        return False

def check_proxy__(proxy_addr: str) -> dict[str, str]:
    pass


def r():
    print("req")