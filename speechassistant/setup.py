import subprocess

from setuptools import setup

setup(
    name="Jarvis",
    version="0.1",
    packages=["src"],
    url="https://github.com/JakobPriesner/Jarvis",
    license="",
    author="Jakob Priesner",
    author_email="jakob.priesner@outlook.de",
    description="",
)

subprocess.call(
    [
        "wget",
        "-qO",
        "-",
        "https://raw.githubusercontent.com/tvdsluijs/sh-python-installer/main/python.sh",
        "|",
        "sudo",
        "bash",
        "-s",
        "3.10.7",
    ]
)
