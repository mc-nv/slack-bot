import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import click
from pythonjsonlogger import jsonlogger
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def setup_logging(debug: bool, log_file: str = None):
    """Configure logging with both console and file handlers."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # Clear any existing handlers
    logger.handlers = []

    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = jsonlogger.JsonFormatter()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_formatter = jsonlogger.JsonFormatter()
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        logger.debug(f"Logging to file: {log_file}")


def read_message_file(file_path):
    """Read message from file."""
    try:
        with open(file_path, "r") as f:
            return f.read().strip()
    except Exception as e:
        logger.error("Failed to read message file", extra={"error": str(e)})
        raise click.ClickException(f"Failed to read message file: {str(e)}")


@click.group()
def main():
    """Slack Bot - A CLI tool for posting messages to Slack channels"""
    pass


@main.command()
@click.option("--debug", "-d", is_flag=True, default=False, help="Debug mode")
@click.option(
    "--log-file",
    "-l",
    help="Log file path",
    default=f"/tmp/slack_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
)
@click.option("--channel", "-c", "--user", "-u", required=True, help="Slack channel ID")
@click.option("--message", "-m", help="Message to post")
@click.option(
    "--message-file",
    "-mf",
    type=click.Path(exists=True),
    help="File containing message to post",
)
@click.option(
    "--reply-in-thread-message",
    "-rm",
    multiple=True,
    help="Message to post in thread (can be used multiple times)",
)
@click.option(
    "--reply-in-thread-message-file",
    "-rmf",
    type=click.Path(exists=True),
    multiple=True,
    help="File containing message to post in thread (can be used multiple times)",
)
@click.option("--token", "-t", help="Slack token", default=os.getenv("SLACK_TOKEN"))
def post(
    debug,
    log_file,
    channel,
    message,
    message_file,
    reply_in_thread_message,
    reply_in_thread_message_file,
    token,
):
    """Post a message to a Slack channel with optional thread replies"""
    setup_logging(debug, log_file)
    logger = logging.getLogger()
    logger.debug("Debug mode enabled" if debug else "Debug mode disabled")

    if not message and not message_file:
        raise click.ClickException(
            "Either --message or --message-file must be provided"
        )

    if message_file:
        message = read_message_file(message_file)

    try:
        client = WebClient(token=token)

        # Post the main message
        response = client.chat_postMessage(channel=channel, text=message)
        thread_ts = response["ts"]

        logger.debug(
            "Main message response",
            extra={"response": response},
        )

        logger.info(
            "Main message posted successfully",
            extra={"channel": channel, "content": message, "ts": thread_ts},
        )

        # Post thread replies if any
        thread_messages = []

        # Add direct messages
        thread_messages.extend(reply_in_thread_message)

        # Add messages from files
        for file_path in reply_in_thread_message_file:
            thread_messages.append(read_message_file(file_path))

        # Post each thread message
        for thread_message in thread_messages:
            thread_response = client.chat_postMessage(
                channel=channel,
                text=thread_message,
                thread_ts=thread_ts,
            )

            logger.debug(
                "Thread reply response",
                extra={"response": thread_response},
            )

            logger.info(
                "Thread reply posted successfully",
                extra={
                    "channel": channel,
                    "content": thread_message,
                    "thread_ts": thread_ts,
                    "ts": thread_response["ts"],
                },
            )

        click.echo(f"Message posted successfully to channel {channel}")
        if thread_messages:
            click.echo(f"Posted {len(thread_messages)} replies in thread")

    except SlackApiError as e:
        logger.error(
            "Failed to post message", extra={"error": str(e), "channel": channel}
        )
        raise click.ClickException(f"Failed to post message: {str(e)}")


if __name__ == "__main__":
    main()

# add flag --reploy-in-thread-message and --reploy-in-thread-message-file that can form an array of messages to post in thread
