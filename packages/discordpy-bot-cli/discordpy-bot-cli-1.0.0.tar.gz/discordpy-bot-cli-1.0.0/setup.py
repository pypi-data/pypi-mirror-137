from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = "discordpy-bot-cli",
    version = "1.0.0",
    author = "Areen Rath",
    description = "CLI for helping in making Discord bots easily",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = ["cli"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires = ">=3.6",
    install_requires = ["discord.py", "heroku"],
    entry_points={
        "console_scripts": ["dcpy = cli.cli:start"]
    }
)