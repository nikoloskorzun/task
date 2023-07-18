import module_settings
import module_requests

def main():
    settings = module_settings.before_start_app()



    #proxy = next(module_settings.get_working_proxy('http_proxy.txt', module_requests.check_proxy, int(settings['IDENTITY']['max-retries'])))
    #print(proxy)
    #arr = module_requests.get_array_with_news(settings['IDENTITY']['user-agent'], int(settings['IDENTITY']['max-retries']), proxy={'https': '144.160.240.75:8080'})
    #print(arr)


if __name__ == "__main__":
    main()