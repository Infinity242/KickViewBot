import sys
print(sys.path)
import CustomTkinter as tk
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
import cloudscraper
import time

# read usernames from a file and store them in a list
with open("usernames.txt", "r") as f:
    usernames = [line.strip() for line in f.readlines()]

# create a Cloudscraper instance
scraper = cloudscraper.create_scraper()

# function to check the validity of a username and send a message to the webhook if it is valid
def check_username(username):
    driver = webdriver.Chrome()
    url = f"https://kick.com/channels/check-username/{username}"
    driver.get(url)

    if "Good to go" in driver.page_source:
        # check opposite case of the username
        if username[0].islower():
            alt_username = username.capitalize()
        else:
            alt_username = username.lower()
        url = f"https://kick.com/channels/check-username/{alt_username}"
        driver.get(url)
        if "Good to go" in driver.page_source:
            print(f"{username} and {alt_username} are valid")
            if webhook_url:
                message = {
                    "content": f"{username} and {alt_username} are valid"
                }
                response = requests.post(webhook_url, json=message)
            with open("valid.txt", "a") as valid_file:
                valid_file.write(f"{username}\n")
        else:
            print(f"{username} is invalid")
            with open("invalid.txt", "a") as invalid_file:
                invalid_file.write(f"{username}\n")
    else:
        print(f"{username} is invalid")
        with open("invalid.txt", "a") as invalid_file:
            invalid_file.write(f"{username}\n")

    driver.quit()

def start():
    # ask user for the Discord webhook URL or type "no" to skip
    global webhook_url
    webhook_url = url_entry.get()
    if webhook_url.lower() == 'no':
        webhook_url = None

    # ask user for the number of threads
    num_threads = int(num_threads_entry.get())

    # create a ThreadPoolExecutor with the given number of threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        # submit a check_username task for each username
        for username in usernames:
            # wait until a worker becomes available before submitting the next task
            while len(futures) >= num_threads:
                for f in as_completed(futures):
                    futures.remove(f)
                time.sleep(0.1)
            # submit the task and append the future object to the list
            future = executor.submit(check_username, username)
            futures.append(future)

    # close the Cloudscraper instance
    scraper.close()

# create the GUI
root = tk.Tk()
root.title("Check Usernames")

url_label = tk.Label(root, text="Discord webhook URL:")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

num_threads_label = tk.Label(root, text="Number of threads:")
num_threads_label.pack()
num_threads_entry = tk.Entry(root, width=50)
num_threads_entry.pack()

start_button = tk.Button(root, text="Start", command=start)
start_button.pack()

root.mainloop()