from tkinter import *
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

def run_script(url, num_threads):
    processes = []
    for i in range(num_threads):
        bot = KickBot(url)
        process = Process(target=bot.doTest)
        process.start()
        processes.append(process)
    for process in processes:
        process.join()

if __name__ == '__main__':
    url = 'https://example.com'
    num_threads = int(input('Enter the number of threads to use: '))
    run_script(url, num_threads)

class App(Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#1E1E1E")
        self.master = master
        self.pack(fill=BOTH, expand=True)
        self.create_widgets()
        self.kick_bots = []

    def create_widgets(self):
        # Create a frame for the header
        header_frame = Frame(self, bg="#4E4E4E", height=40)
        header_frame.pack(fill=X)

        # Add a label for the header text
        header_label = Label(header_frame, text="Kick View Bot", font=("Segoe UI", 14), fg="#FFFFFF", bg="#4E4E4E")
        header_label.pack(side=LEFT, padx=10)

        # Create a frame for the content
        content_frame = Frame(self, bg="#2D2D2D")
        content_frame.pack(fill=BOTH, expand=True, pady=10, padx=20)

        # Add a label for the URL input
        url_label = Label(content_frame, text="Enter website URL:", font=("Segoe UI", 10), fg="#FFFFFF", bg="#2D2D2D")
        url_label.grid(row=0, column=0, pady=5)

        # Add an entry field for the URL input
        self.url_input = Entry(content_frame, bg="#1E1E1E", fg="#FFFFFF", font=("Segoe UI", 10), borderwidth=0)
        self.url_input.grid(row=1, column=0, padx=10)

        # Add a label for the tabs input
        tabs_label = Label(content_frame, text="Enter number of tabs to open:", font=("Segoe UI", 10), fg="#FFFFFF", bg="#2D2D2D")
        tabs_label.grid(row=2, column=0, pady=5)

        # Add an entry field for the tabs input
        self.tabs_input = Entry(content_frame, bg="#1E1E1E", fg="#FFFFFF", font=("Segoe UI", 10), borderwidth=0)
        self.tabs_input.grid(row=3, column=0, padx=10)

        # Add a start button
        start_button = Button(content_frame, text="Start Bot", font=("Segoe UI", 10), fg="#FFFFFF", bg="#43B581", activebackground="#43B581", borderwidth=0, command=self.start_bot)
        start_button.grid(row=4, column=0, pady=10)

        # Add a stop button
        stop_button = Button(content_frame, text="Stop Bot", font=("Segoe UI", 10), fg="#FFFFFF", bg="#F04747", activebackground="#F04747", borderwidth=0, command=self.stop_bot)
        stop_button.grid(row=5, column=0, pady=10)

        # Add a label for the credits
        credits_label = Label(self, text="Made By: AnonX", font=("Segoe UI", 10), fg="#FFFFFF", bg="#1E1E1E")
        credits_label.pack(side=BOTTOM, padx=10, pady=10, anchor=SE)

    def start_bot(self):
        url = self.url_input.get().strip()
        num_tabs = int(self.tabs_input.get().strip())

        for i in range(0, num_tabs, 4):
            tabs_to_open = min(4, num_tabs-i)
            for j in range(tabs_to_open):
                kickBot = KickBot(url)
                t = Thread(target=kickBot.doTest)
                t.start()
                self.kick_bots.append(kickBot)
            sleep(10)

    def stop_bot(self):
        for kickBot in self.kick_bots:
            kickBot.stop()
        for widget in self.winfo_children():
            widget.destroy()
        self.master.destroy()

root = Tk()
root.title("Kick View Bot")
root.geometry("500x400")
root.config(bg="#1E1E1E")
app = App(master=root)
app.pack(fill=BOTH, expand=True)
app.place(relx=0.5, rely=0.5, anchor=CENTER)
root.mainloop()
