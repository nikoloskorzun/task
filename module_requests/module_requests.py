import requests

from .parser import News_parser


test_domain = {'http': 'http://httpbin.org/ip', 'https': 'https://httpbin.org/ip'}
base_domain = 'https://news.google.com'


def check_proxy(proxy_addr: str, max_retries: int) -> str | None:
    """checks the proxy server for proper operation and returns operation mode
    :param proxy_addr: ip_addr:port, example:1.2.3.4:8080
    :param max_retries: example:5

    :return: 'https' or 'http' or None
    """

    proxies = {
        'https': f'http://{proxy_addr}',
        'http': f'http://{proxy_addr}',
    }
    s = requests.Session()
    s.mount("https://", requests.adapters.HTTPAdapter(max_retries=max_retries))
    s.mount("http://", requests.adapters.HTTPAdapter(max_retries=max_retries))

    s.proxies.update(proxies)
    for protocol in proxies:
        try:
            response = s.get(test_domain[protocol], timeout=7)
            response.raise_for_status()
            if response.status_code == 200 and response.json()['origin'] == proxy_addr.split(':')[0]:
                return protocol
        except Exception as e:
            pass

    return None


def get_array_with_news(user_agent: str, max_retries: int, proxy: dict[str, str] | None) -> tuple[list[str], requests.cookies.RequestsCookieJar] | None:
    header = {'User-agent': user_agent}
    try:
        s = requests.Session()
        s.headers = header
        if proxy is not None:
            s.proxies = proxy
        s.mount("https://", requests.adapters.HTTPAdapter(max_retries=max_retries))

        ans = s.get(base_domain+'/home')
        parser = News_parser()
        parser.set_base_url(base_domain)
        parser.feed(ans.text)
        return parser.get_refs(), ans.cookies
    except Exception as e:
        pass
