import sys
import getopt

from setuptools import setup, find_packages

arguments = []
for arg in sys.argv:
    if arg.startswith("--version"):
        arguments.append(arg)

if len(arguments) > 0:
    sys.argv.remove(arguments[0])

optlist, _ = getopt.getopt(arguments, "", ["version="])

version = "0.0.0"
if len(optlist) > 0 and optlist[0][0] == "--version":
    version = optlist[0][1]

setup(
    name="levatas-alira-cli",
    version=version,
    description="Alira CLI",
    url="https://github.com/vinsa-ai/alira-cli",
    author="Levatas",
    author_email="svpino@gmail.com",
    packages=find_packages(exclude=["license", "libs"]),
    include_package_data=True,
    install_requires=[
        "Click",
        "Docker",
        "python-dateutil",
        "cryptography>=37.0.0",
        "levatas-alira-licensing",
    ],
    entry_points={
        "console_scripts": [
            "alr = levatas_alira_cli.alr:cli",
        ],
    },
)
