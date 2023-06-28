import module_settings
import module_requests
def main():
    settings = module_settings.before_start_app()
    print(module_requests.check_proxy({'https': '159.223.159.251:8080'}))

if __name__ == "__main__":
    main()