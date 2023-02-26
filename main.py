from selenium import webdriver
from threading import Thread
from time import sleep

class KickBot():
    def __init__(self, url) -> None:
        self.url = url
        self.driver = None
        
    def setupWebBrowser(self):
        self.driver = webdriver.Chrome()
        
    def doTest(self):
        self.setupWebBrowser()
        
        self.driver.get(self.url)
        while True:
            sleep(10)

url = input("Enter website URL: ")

num_tabs = int(input("Enter number of tabs to open: "))
        
for i in range(num_tabs):
    kickBot = KickBot(url)
    t = Thread(target=kickBot.doTest)
    t.start()
