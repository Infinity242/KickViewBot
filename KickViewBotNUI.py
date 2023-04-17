from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from threading import Thread
from time import sleep
from multiprocessing import Process

class KickBot():
    def __init__(self, url):
        self.url = url
        self.driver = None

    def setupWebBrowser(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-minimized")
        chrome_options.add_argument("--mute-audio")
        #chrome_options.add_argument("--headless")
        self.driver = Chrome(options=chrome_options)

    def doTest(self):
        self.setupWebBrowser()
        self.driver.get(self.url)
        not_found_count = 0
        while True:
            try:
                # Locate the button by its text
                button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Start watching')]")
                # Click the button
                button.click()
                print("Button clicked!")
                not_found_count = 0
            except NoSuchElementException:
                # Refresh page if "Oops, Something went wrong" message is on the screen
                if "Oops, Something went wrong" in self.driver.page_source:
                    self.driver.refresh()
                    print("Page refreshed!")
                    not_found_count = 0
                elif not_found_count >= 10:
                    print("Watch now button not found after 10 attempts. Stopping search.")
                    break
                elif "Checking if the site connection is secure" in self.driver.page_source:
                    self.driver.close()
                    sleep(5)
                    self.setupWebBrowser()
                    self.driver.get(self.url)
                    print("Browser restarted")
                else:
                    print("Watch now button not found on this page")
                not_found_count += 1
            sleep(10)

        # Keep the browser window open after the program has finished searching for the button
        while True:
            pass

def run_script(url, num_threads):
    processes = []
    num_windows = 0
    for i in range(num_threads):
        bot = KickBot(url)
        process = Process(target=bot.doTest)
        process.start()
        processes.append(process)
        num_windows += 1
        if num_windows == 4:
            num_windows = 0
            sleep(6) # Wait for 6 seconds before starting another set of 4 windows
    for process in processes:
        process.join()

if __name__ == '__main__':
    print("This tool was created by AnonX#8622")
    input("Press Enter to say thanks...")
    url = input("Enter the website URL: ")
    num_threads = int(input('Enter the number of threads to use: '))
    run_script(url, num_threads)
