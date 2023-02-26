from tkinter import *
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from threading import Thread
from time import sleep

class KickBot():
    def __init__(self, url):
        self.url = url
        self.driver = None

    def setupWebBrowser(self):
        self.driver = Chrome()

    def doTest(self):
        self.setupWebBrowser()
        self.driver.get(self.url)
        # Locate the button by its text
        button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Start watching')]")
        # Click the button
        button.click()
        while True:
            sleep(10)

class App(Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#1E1E1E")
        self.master = master
        self.pack(fill=BOTH, expand=True)
        self.create_widgets()

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

    def start_bot(self):
        url = self.url_input.get().strip()
        num_tabs = int(self.tabs_input.get().strip())

        for i in range(num_tabs):
            kickBot = KickBot(url)
            t = Thread(target=kickBot.doTest)
            t.start()

root = Tk()
root.title("Kick View Bot")
root.geometry("500x400")
root.config(bg="#1E1E1E")
app = App(master=root)
app.pack(fill=BOTH, expand=True)
app.place(relx=0.5, rely=0.5, anchor=CENTER)
root.mainloop()