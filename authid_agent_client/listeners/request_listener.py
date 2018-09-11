import threading
import requests
import time

DEFAULT_INTERVAL = 3
DEFAULT_MAX_REQUESTS = 120

STATUS_REJECTED = "rejected"
STATUS_CONFIRMED = "confirmed"


class RequestListener:
    def __init__(self, request_id: str, api_url: str, callback, interval: int = DEFAULT_INTERVAL,
                 max_requests: int = DEFAULT_MAX_REQUESTS):
        self.request_id = request_id
        self.api_url = api_url
        self.callback = callback

        self.run = False
        self.interval = interval
        self.max_requests = max_requests
        self.request_count = 0

    def start(self):
        self.run = True
        thread = threading.Thread(target=self.__start, args=())
        thread.daemon = True
        thread.start()

    def __start(self):
        while self.run:

            http_status, request = self.__fetch_status(self.request_id)

            if http_status == 404 or http_status == 204:
                self.run = False
                self.callback(404, None)

            if request["status"] == STATUS_REJECTED or request["status"] == STATUS_CONFIRMED:
                self.run = False
                self.callback(200, request)

            if self.request_count >= self.max_requests:
                self.run = False

            time.sleep(self.interval)
            self.request_count += 1

    def __fetch_status(self, request_id: str):
        request_url = self.api_url + request_id
        request = requests.get(request_url)

        if request.status_code == 204:
            return 204, None
        return request.status_code, request.json()
