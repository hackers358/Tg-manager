import os
import time
import urllib.request
import urllib.parse


# Bot token can be provided via the command line or the TG_TOKEN
# environment variable. This avoids hard-coding sensitive data.
DEFAULT_TOKEN = os.environ.get("TG_TOKEN")


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
    parser.add_argument(
        "token",
        nargs="?",
        default=DEFAULT_TOKEN,
        help="Telegram bot token (or set TG_TOKEN environment variable)",
    )
    parser.add_argument("chat_id", help="ID of the channel or chat")
    parser.add_argument("message", help="Message text")
    parser.add_argument("--at", type=float, default=time.time(), help="UNIX timestamp when the message should be sent")

    args = parser.parse_args()

    token = args.token
    if not token:
        parser.error("Bot token must be supplied via argument or TG_TOKEN")

    schedule_message(token, args.chat_id, args.message, args.at)
