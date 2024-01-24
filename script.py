from selenium import webdriver
import time
import signal
import sys

def clear_cookies(driver):
    driver.delete_all_cookies()

def signal_handler(sig, frame):
    print("\nScript terminated by user. Exiting...")
    sys.exit(0)

def main():

    driver = webdriver.Chrome()

    try:
        driver.get("https://deriv.com")

        signal.signal(signal.SIGINT, signal_handler)

        while True:
            time.sleep(10)  # Clear cookies every 10 seconds
            clear_cookies(driver)

    except KeyboardInterrupt:
        
        print("\nScript terminated by user. Exiting...")
        sys.exit(0)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
