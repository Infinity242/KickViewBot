from threading import Thread
from multiprocessing import Process
import requests
import socket
from time import sleep

class KickBot():
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.csrf_token = None

    def getToken(self):
        response = self.session.get(self.url)
        self.csrf_token = response.headers.get('X-CSRFToken')

    def doTest(self):
        self.getToken()
        not_found_count = 0
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.url, 80))
                headers = {
                    'X-CSRFToken': self.csrf_token,
                    'Connection': 'close'
                }
                request = f"GET / HTTP/1.1\r\nHost: {self.url}\r\n"
                for key, value in headers.items():
                    request += f"{key}: {value}\r\n"
                request += "\r\n"
                s.send(request.encode())
                response = s.recv(4096)
                if "Start watching" in response.decode():
                    print("Button clicked!")
                    not_found_count = 0
                else:
                    print("Watch now button not found on this page")
                    not_found_count += 1
                    if not_found_count >= 10:
                        print("Watch now button not found after 10 attempts. Stopping search.")
                        break
                s.close()
            except Exception as e:
                print(f"Connection error: {e}. Retrying...")
            sleep(10)

        while True:
            pass

def run_script(url, num_threads):
    threads = []
    num_windows = 0
    for i in range(num_threads):
        bot = KickBot(url)
        thread = Thread(target=bot.doTest)
        thread.start()
        threads.append(thread)
        num_windows += 1
        if num_windows == 4:
            num_windows = 0
            sleep(6)
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    url = input("Enter the website URL: ")
    num_threads = int(input('Enter the number of threads to use: '))
    run_script(url, num_threads)