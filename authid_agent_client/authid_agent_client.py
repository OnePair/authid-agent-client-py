import requests
import json

from authid_agent_client.listeners.request_listener import RequestListener

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8080

API_PATH = "/api/v0.0.1/"
IDS_PATH = API_PATH + "ids/"
PROCESSOR_KEYS_PATH = API_PATH + "processorKeys/"
REQUESTS_PATH = API_PATH + "requests/"
ADDRESSES_PATH = API_PATH + "addresses/"
TRANSFER_PATH = API_PATH + "ids:transfer/"
CHALLENGES_PATH = API_PATH + "challenges/"
SIGN_CHALLENGE_PATH = API_PATH + "challenges:sign"
VERIFY_CHALLENGE_PATH = API_PATH + "challenges:verify"


'''def default_request_callback(status: int, response):
    print("\n", "Got request with status:", status, "\n", end="")
    print("Got request data:\n", json.dumps(response, sort_keys=True, indent=True), end="")
'''

class AuthIDAgentClient:
    def __init__(self, host: str = DEFAULT_HOST, port: str = DEFAULT_PORT,
                 request_callback=None):
        self.__host = host
        self.__port = port
        self.__base_url = "http://" + host + ":" + str(port)
        self.__ids_url = self.__base_url + IDS_PATH
        self.__requests_url = self.__base_url + REQUESTS_PATH
        self.__addresses_url = self.__base_url + ADDRESSES_PATH
        self.__transfer_url = self.__base_url + TRANSFER_PATH
        self.__processor_keys_path = self.__base_url + PROCESSOR_KEYS_PATH
        self.__challenges_path = self.__base_url + CHALLENGES_PATH
        self.__sign_challenge_path = self.__base_url + SIGN_CHALLENGE_PATH
        self.__verify_challenge_path = self.__base_url + VERIFY_CHALLENGE_PATH

        self.__request_callback = request_callback

    def get_authid(self, authid: str):
        request_url = self.__ids_url + authid
        request = requests.get(request_url)

        return request.status_code, request.json()

    def register_authid(self, id: str, protocol: str, address: str, fee: str):
        request_url = self.__ids_url + id

        request = requests.post(request_url, {"protocol": protocol, "address": address, "fee": fee})

        if request.status_code == 200:
            self.add_request_listener(request.json()["requestID"])

        return request.status_code, request.json()

    def transfer_authid(self, id: str, protocol: str, address: str):
        request = requests.post(self.__transfer_url, {"id": id, "protocol": protocol, "address": address})

        if request.status_code == 200:
            self.add_request_listener(request.json()["requestID"])

        return request.status_code, request.json()

    def generate_processor_keys(self, id: str):
        request_url = self.__processor_keys_path + id
        request = requests.post(request_url)

        if request.status_code == 200:
            self.add_request_listener(request.json()["requestID"])

        return request.status_code, request.json()

    def new_address(self, protocol: str):
        request_url = self.__addresses_url + "/" + protocol
        request = requests.post(request_url)

        if request.status_code == 200:
            self.add_request_listener(request.json()["requestID"])

        return request.status_code, request.json()

    """
    The authentication functions
    """

    def create_challenge(self, challenger_id: str, receiver_id: str):
        request = requests.post(self.__challenges_path,
                                params={"challengerID": challenger_id, "receiverID": receiver_id},
                                headers={"Content-Type": "application/json"})

        return request.status_code, request.json()

    def sign_challenge(self, challenge: dict):
        request = requests.post(self.__sign_challenge_path, json=challenge)

        if request.status_code == 200:
            self.add_request_listener(request.json()["requestID"])

        return request.status_code, request.json()

    def verify_challenge(self, signed_challenge: dict):

        print("signed challenge:", signed_challenge)
        request = requests.post(self.__verify_challenge_path, signed_challenge,
                                headers={"Content-Type": "application/json"})

        return request.status_code, request.json()

    def add_request_listener(self, request_id: str):
        listener = RequestListener(request_id, self.__requests_url, self.__request_callback)
        listener.start()
