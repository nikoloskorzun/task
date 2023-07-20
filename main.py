import module_settings
import module_requests
import module_sqlite
import module_selenium
import module_multiprocessing

from os import getcwd
from datetime import datetime
def target(url: str, cookies, settings, db, table_cookie_profile, lock):

    o = module_selenium.Selenium_worker(settings['SELENIUM']['firefox-options'], 'Firefox', url, cookies)
    o.run()
    c = o.get_cookies()
    o.close()
    params = (url, c, datetime.now())
    table_cookie_profile.update_profile(db.get_connection_cursor(), params)



def main():

    settings = module_settings.before_start_app()
    db = module_sqlite.Database(getcwd() + '\\' + settings['IDENTITY']['database-fn'])
    t = module_sqlite.Table_Cookie_Profile()
    if db.table_exist(t):
        db.create_table(t)
    #proxy = next(module_settings.get_working_proxy('http_proxy.txt', module_requests.check_proxy, int(settings['IDENTITY']['max-retries'])))

    proxy = {'https': '129.153.157.63:3128'}

    arr_with_news_urls, cookies = module_requests.get_array_with_news(settings['IDENTITY']['user-agent'],
                                                                      int(settings['IDENTITY']['max-retries']),
                                                                      proxy=proxy)

    arr_with_news_urls = 'http  s://news.google.com/articles/CBMiZWh0dHBzOi8vd3d3LmNic25ld3MuY29tL25ld3MvdG9ybmFkby1wZml6ZXItcGxhbnQtbm9ydGgtY2Fyb2xpbmEtZGFtYWdlLWxvbmctdGVybS1tZWRpY2luZS1zaG9ydGFnZXMv0gFpaHR0cHM6Ly93d3cuY2JzbmV3cy5jb20vYW1wL25ld3MvdG9ybmFkby1wZml6ZXItcGxhbnQtbm9ydGgtY2Fyb2xpbmEtZGFtYWdlLWxvbmctdGVybS1tZWRpY2luZS1zaG9ydGFnZXMv?hl=en-US&gl=US&ceid=US%3Aen'
    p = module_multiprocessing.Pool(int(settings['PROCESSES']['max']))

    p.add_target_func(target)

    for url in arr_with_news_urls:
        p.add_arg([url, cookies, settings, db, t])
    p.run()



if __name__ == "__main__":
    main()