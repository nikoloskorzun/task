import configparser
from os import getcwd, listdir
from pickle import dump, load
from typing import Callable


settings_filename = 'settings.ini'
settings_template_filename = 'module_settings\\config.template'


class Config_template:
    def save(self, filename: str) -> None:
        """With pickle saving structure in file
        :param filename:
        :return:
        """
        with open(filename, 'wb') as file:
            dump(self.__content, file)

    def load(self, filename: str) -> None:
        """With pickle loading structure from file
        :param filename:
        :return None:
        """
        with open(filename, 'rb') as file:
            self.__content = load(file)

    def get(self) -> dict[str, dict[str, type]]:
        return self.__content

    def set(self, template: dict[str, dict[str, type]]) -> None:
        self.__content = template

    def __init__(self):
        self.__content = None


def set_template() -> None:
    template = {"IDENTITY": {"user-agent": str, "proxy-list-fn": str, 'max-retries': int}, "PROCESSES": {"max": int}}
    c = Config_template()
    c.set(template)

    c.save(settings_template_filename)


def is_correct(config: configparser.ConfigParser) -> bool:
    """Checks the config to match the template lying in the file settings_template_filename

    :param config:
    :return: True if correct, else False
    """
    temp_config_io = Config_template()
    temp_config_io.load(settings_template_filename)
    template = temp_config_io.get()

    for group in template:
        if group not in config:
            return False
        for el in template[group]:
            if el not in config[group]:
                return False
            type_of_el = template[group][el]
            if type_of_el == int:
                if not config[group][el].isdigit():
                    return False
            elif type_of_el == float:
                if not config[group][el].isnumeric():
                    return False

    return True


def get_default_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config["IDENTITY"] = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 "
                                        "Firefox/114.0", "proxy-list-fn": "http_proxy.txt", 'max-retries': '10'}
    config['PROCESSES'] = {'max': '5'}
    return config


def get_working_proxy_list(count: int, filename_proxies_source: str, proxy_checker: Callable[[str], str], max_retries: int) -> list[dict[str, str]]:
    res = []
    amount=0
    with open(filename_proxies_source) as f:
        for line in f:
            protocol = proxy_checker(line, max_retries)
            if protocol is not None:
                res.append({protocol: line})
                amount+=1
                if count<=amount:
                    return res
    return res


def get_working_proxy(filename_proxies_source: str, proxy_checker: Callable[[str], str], max_retries: int) -> dict[str, str]:
    with open(filename_proxies_source) as f:
        for line in f:
            protocol = proxy_checker(line, max_retries)
            if protocol is not None:
                yield {protocol: line}


def before_start_app() -> configparser.ConfigParser:
    """Returns the settings from the .ini file and checks them

    :return: Correct settings regardless of the problems occurred
    """
    root_dir = getcwd()
    config = configparser.ConfigParser()

    if settings_filename in listdir(root_dir):
        config.read(settings_filename)
        if is_correct(config):
            pass
        else:
            print(f"In {settings_filename} error found. Fix it, or delete .ini file and run the script, current "
                  f"settings - default")
            config = get_default_config()
    else:
        print(f"{settings_filename} not found.\nCreating .ini file with default settings")
        config = get_default_config()
        with open(settings_filename, 'w') as configfile:
            config.write(configfile)

    return config
