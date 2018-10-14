from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    author="OnePair",
    name="authid-agent-client",
    version="0.0.1",
    packages=find_packages(),
    install_requires=required,
    entry_points={
        "console_scripts": [
            "authid-cli = authid_agent_client.cli.agent_client_cli:run_cli"
        ]
    }
)
