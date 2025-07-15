import os
import json
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
from datetime import date

# Load DB credentials
load_dotenv()
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_NAME = os.getenv("POSTGRES_DB", "telegram_db")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)
load_dotenv()
print("DB_HOST:", os.getenv("POSTGRES_HOST"))  # Add this line
print("DB_NAME:", os.getenv("POSTGRES_DB"))  # Add this line
TODAY = date.today().isoformat()
RAW_PATH = Path(f"data/raw/telegram_messages/{TODAY}")

def load_json_to_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    cur = conn.cursor()

    for file in RAW_PATH.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            messages = json.load(f)
            for msg in messages:
                cur.execute("""
                    INSERT INTO raw.telegram_messages
                    (id, channel, date, message, has_media, media_type, image_path)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (
                    msg.get("id"),
                    msg.get("channel"),
                    msg.get("date"),
                    msg.get("message"),
                    msg.get("has_media"),
                    msg.get("media_type"),
                    msg.get("image_path")
                ))
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Loaded raw messages into PostgreSQL")

if __name__ == "__main__":
    load_json_to_db()
