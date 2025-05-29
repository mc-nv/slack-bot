# Slack Bot

A CLI tool for posting messages to Slack channels.

## Installation

### Development Installation

```bash
pip install -e .
```

### Build and Install Wheel

```bash
# Create wheel
python setup.py bdist_wheel

# Install from wheel
pip install dist/slack_bot-0.1.0-py3-none-any.whl
```

## Usage

```bash
# Basic usage
slack-bot post --channel CHANNEL_ID --message "Your message"

# Post message from file
slack-bot post --channel CHANNEL_ID --message-file message.txt

# Post message with thread replies
slack-bot post --channel CHANNEL_ID --message "Main message" --reply-in-thread-message "First reply" --reply-in-thread-message-message "Second reply"

# Post message with thread replies from files
slack-bot post --channel CHANNEL_ID --message "Main message" --reply-in-thread-message-file reply1.txt --reply-in-thread-message-file reply2.txt

# Enable debug mode and specify log file
slack-bot post --channel CHANNEL_ID --message "Your message" --debug --log-file /path/to/logfile.log
```

### Command-line Options

- `--channel`, `-c`: Slack channel ID (required)
- `--message`, `-m`: Message to post
- `--message-file`, `-mf`: File containing message to post
- `--reply-in-thread-message`, `-rm`: Message to post in thread (can be used multiple times)
- `--reply-in-thread-message-file`, `-rmf`: File containing message to post in thread (can be used multiple times)
- `--token`, `-t`: Slack token (defaults to SLACK_TOKEN environment variable)
- `--debug`, `-d`: Enable debug mode
- `--log-file`, `-l`: Log file path (defaults to /tmp/slack_bot_TIMESTAMP.log)

## Requirements

- Python 3.10 or higher
- Slack SDK
- Click
- Python JSON Logger
- wheel (for building wheel)

## Environment Variables

- `SLACK_TOKEN`: Slack API token (can be overridden with --token option)