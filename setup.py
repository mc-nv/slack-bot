from setuptools import find_packages, setup

setup(
    name="slack-bot",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
        "slack-sdk>=3.0.0",
        "python-json-logger>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "slack-bot=slack_bot.cli:main",
        ],
    },
    python_requires=">=3.10",
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI tool for posting messages to Slack channels",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
