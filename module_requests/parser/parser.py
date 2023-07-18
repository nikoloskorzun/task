from html.parser import HTMLParser


class News_parser(HTMLParser):

    __refs = set()
    __base_url = str()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href' and attr[1].startswith('./articles'):
                    self.__refs.add(self.__base_url + attr[1][1:])

    def set_base_url(self, url: str) -> None:
        self.__base_url = url

    def get_refs(self) -> list[str]:
        return list(self.__refs)