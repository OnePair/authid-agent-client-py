from authid_agent_client.authid_agent_client import AuthIDAgentClient

authid_agent_client = AuthIDAgentClient()


def get_id_test():
    status, authid = authid_agent_client.get_authid("user11.btc")

    print("request status:", status)
    print("id:", authid)


def new_address_test():
    status, address = authid_agent_client.new_address("btc")

    print("request status:", status)
    print("address:", address)


if __name__ == "__main__":
    print("running tests")

    # get_id_test()
    new_address_test()
