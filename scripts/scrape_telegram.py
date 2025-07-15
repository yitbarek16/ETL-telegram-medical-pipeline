# scripts/scrape_telegram.py

import os
import json
import logging
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto

# Load secrets from .env
load_dotenv()
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

# Define channels to scrape
CHANNELS = [
    "lobelia4cosmetics",
    "tikvahpharma",
    "CheMed123",
    "Thequorachannel",
    "tenamereja"
]

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set output paths
TODAY = date.today().isoformat()
BASE_JSON_PATH = Path("data/raw/telegram_messages") / TODAY
BASE_IMG_PATH = Path("data/raw/images") / TODAY
BASE_JSON_PATH.mkdir(parents=True, exist_ok=True)

async def scrape_channel(client, channel):
    messages_data = []
    try:
        async for msg in client.iter_messages(channel, limit=100):
            message_dict = {
                "id": msg.id,
                "date": msg.date.isoformat() if msg.date else None,
                "message": msg.text,
                "channel": channel,
                "has_media": bool(msg.media),
                "media_type": type(msg.media).__name__ if msg.media else None,
                "image_path": None
            }

            # Check if message has an image and download it
            if isinstance(msg.media, MessageMediaPhoto):
                img_dir = BASE_IMG_PATH / channel
                img_dir.mkdir(parents=True, exist_ok=True)
                img_path = img_dir / f"message_{msg.id}.jpg"
                try:
                    await msg.download_media(file=img_path)
                    message_dict["image_path"] = str(img_path)
                    logger.info(f"📸 Downloaded image from {channel} msg {msg.id}")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to download image from {channel} msg {msg.id}: {e}")

            messages_data.append(message_dict)

        # Write message data to JSON
        out_file = BASE_JSON_PATH / f"{channel}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(messages_data, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Scraped {len(messages_data)} messages from {channel}")

    except Exception as e:
        logger.error(f"❌ Error scraping {channel}: {e}")

async def main():
    async with TelegramClient("session", API_ID, API_HASH) as client:
        for channel in CHANNELS:
            await scrape_channel(client, channel)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
