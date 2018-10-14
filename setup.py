from setuptools import find_packages
from setuptools import setup

setup(
    author="OnePair",
    name="authid-agent-client",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "authid-cli = authid_agent_client.cli.agent_client_cli:run_cli"
        ]
    }
)
