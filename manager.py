import json
import time
import urllib.request
import urllib.parse
from datetime import datetime


def send_message(token: str, chat_id: str, text: str) -> None:
    """Send a text message to the specified chat."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
    with urllib.request.urlopen(url, data=data) as response:
        response.read()


def schedule_message(token: str, chat_id: str, text: str, send_time: float) -> None:
    """Schedule a message to be sent at the specified UNIX timestamp."""
    delay = send_time - time.time()
    if delay > 0:
        time.sleep(delay)
    send_message(token, chat_id, text)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simple Telegram channel manager.")
    parser.add_argument("token", help="Telegram bot token")
    parser.add_argument("chat_id", help="ID of the channel or chat")
    parser.add_argument("message", help="Message text")
    parser.add_argument("--at", type=float, default=time.time(), help="UNIX timestamp when the message should be sent")

    args = parser.parse_args()
    schedule_message(args.token, args.chat_id, args.message, args.at)
