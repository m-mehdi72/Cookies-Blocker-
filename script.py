from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from browser_cookie3 import chrome
import time
import signal
import sys
import os

def clear_cookies(driver):
    driver.delete_all_cookies()

def clear_third_party_cookies(driver):

    all_cookies = driver.get_cookies()

    # Filter and delete third-party cookies
    for cookie in all_cookies:
        if 'deriv.com' not in cookie['domain']:
            driver.delete_cookie(cookie['name'])

    # Use browser_cookie3 to get all cookies from Chrome
    chrome_cookies = chrome()

    # Filter and delete third-party cookies
    for cookie in chrome_cookies:
        if 'deriv.com' not in cookie.domain:
            driver.delete_cookie(cookie.name)

def signal_handler(sig, frame):
    print("\nScript terminated by user. Exiting...")
    sys.exit(0)

class DriverOptions(object):

    def __init__(self):
        self.options = Options()
        self.options.add_argument('--no-sandbox')
        # self.options.add_argument('--start-maximized')
        # self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--incognito')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_argument('disable-infobars')
        mobile_user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36 Edg/118.0.2088.17"
        self.options.add_argument(f'user-agent={mobile_user_agent}')


class WebDriver(DriverOptions):

    def __init__(self):
        DriverOptions.__init__(self)
        self.driver_instance = self.get_driver()

    def get_driver(self):
        path = os.path.join(os.getcwd(), 'chromedriver')
        driver = webdriver.Chrome(options=self.options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source":
                "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
        })

        return driver


def main():

    webdriver = WebDriver()
    driver = webdriver.driver_instance
    try:
        driver.get("https://deriv.com")

        signal.signal(signal.SIGINT, signal_handler)

        while True:
            cookies = driver.get_cookies()
            print("All Cookies:", cookies)
            time.sleep(3)  # Clear cookies every 3 seconds
            clear_cookies(driver)
            # clear_third_party_cookies(driver)

    except KeyboardInterrupt:
        
        print("\nScript terminated by user. Exiting...")
        sys.exit(0)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
