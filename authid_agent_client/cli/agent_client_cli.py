import os

from cmd import Cmd

from authid_agent_client.authid_agent_client import AuthIDAgentClient

import base64
import json


class AgentClientCli(Cmd):
    def __init__(self):
        super().__init__()
        self.__agent_client = AuthIDAgentClient(request_callback=AgentClientCli.request_callback)

    def do_exit(self, args):
        raise SystemExit

    def do_get_authid(self, args):
        """
        Retrieve AuthID
        Syntax: get_authid <authid>
        """
        arg_list = args.split(" ")

        if len(arg_list) != 1:
            print("Invalid syntax!")
            print("Proper syntax: get_authid <authid>")
            return
        status, authid = self.__agent_client.get_authid(arg_list[0])

        print("status:", status)
        print(authid)

    def do_register_id(self, args):
        """
        Register an AuthID
        Syntax: register_id <id> <protocol> <address> <fee>
        """

        arg_list = args.split(" ")

        if len(arg_list) != 4:
            print("Invalid syntax!")
            print("Proper syntax: register_id <id> <protocol> <address> <fee>")
            return

        status, request_info = self.__agent_client.register_authid(arg_list[0], arg_list[1], arg_list[2], arg_list[3])

        print("status:", status)
        print("request info:", request_info)

    def do_transfer_id(self, args):
        """
        Transfer AuthID to a new address
        Syntax: transfer_id <id> <protocol> <address>
        """

        arg_list = args.split(" ")

        if len(arg_list) != 3:
            print("Invalid syntax!")
            print("Proper syntax: transfer_id <id> <protocol> <address>")
            return

        status, request_info = self.__agent_client.transfer_authid(arg_list[0], arg_list[1], arg_list[2])

        print("status:", status)
        print("request info:", request_info)

    def do_new_address(self, args):
        """
        Generate a new address
        Syntax: new_address <protocol>
        """

        arg_list = args.split(" ")

        if len(arg_list) != 1 or arg_list[0] == "":
            print("Invalid syntax!")
            print("Proper syntax: new_address <protocol>")
            return

        status, request_info = self.__agent_client.new_address(arg_list[0])

        print("status:", status)
        print("request info:", request_info)

    def do_generate_processors(self, args):
        """
        Generate a set of processor keys
        Syntax: generate_processors <id>
        """

        arg_list = args.split(" ")

        if len(arg_list) != 1 or arg_list[0] == "":
            print("Invalid syntax!")
            print("Proper syntax: generate_processors <id>")
            return

        status, request_info = self.__agent_client.generate_processor_keys(arg_list[0])

        print("status:", status)
        print("request info:", request_info)

    def do_create_challenge(self, args):
        """
        Create an AuthID challenge
        Syntax: create_challenge <your id> <receiver id>
        """

        arg_list = args.split(" ")

        if len(arg_list) != 2:
            print("Invalid syntax!")
            print("Proper syntax: create_challenge <your id> <receiver id>")
            return

        status, challenge = self.__agent_client.create_challenge(arg_list[0], arg_list[1])

        print("status:", status)

        if status == 201:
            print(base64.b64encode(json.dumps(challenge).encode()).decode())

    def do_sign_challenge(self, challenge):
        """
        Sign challenge
        Syntax: sign_challenge <challenge>
        """

        decoded_challenge = json.loads(base64.b64decode(challenge).decode())
        status, result = self.__agent_client.sign_challenge(decoded_challenge)

        print("status:", status)
        print("request info:", result)

    def do_verify_challenge(self, signed_challenge):
        """
        Verify signed challenge
        Syntax: verify_challenge <signed_challenge>
        """

        decoded_signed_challenge = json.loads(base64.b64decode(signed_challenge).decode())

        authid = decoded_signed_challenge["id_doc"]["id"] + "." + decoded_signed_challenge["id_doc"]["protocol"]
        print("Verifying response from", authid)

        status, result = self.__agent_client.verify_challenge(decoded_signed_challenge)

        print("status:", status)
        print("request info:", result)

    def do_verify_cert(self, cert):
        """
        Verify cert
        Syntax: verify_cert <signed_cert>
        """

        decoded_cert = json.loads(base64.b64decode(cert).decode())

        authid = decoded_cert["id_doc"]["id"] + "." + decoded_cert["id_doc"]["protocol"]
        print("Verifying cert signed by:", authid)

        status, result = self.__agent_client.verify_cert(decoded_cert)

        print("status:", status)
        print("request info:", result)

    def do_clear(self, args):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def emptyline(self):
        pass

    @staticmethod
    def request_callback(status, response: dict):
        print("\n", "Got request with status:", status, "\n", end="")

        if "signedChallenge" in response:
            print("signed challenge:\n", base64.b64encode(json.dumps(response["signedChallenge"]).encode()).decode())
        else:
            print("Got request data:\n", json.dumps(response, sort_keys=True, indent=True), end="")


if __name__ == "__main__":
    app = AgentClientCli()
    app.prompt = "authid-agent-client>"
    app.cmdloop("Starting authid angent client...")
