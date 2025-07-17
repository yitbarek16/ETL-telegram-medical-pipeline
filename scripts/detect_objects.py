from ultralytics import YOLO
import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)

# Load YOLOv8 model (n = nano, faster; use yolov8m.pt or yolov8x.pt for accuracy)
model = YOLO("yolov8n.pt")

# Scan images in all subdirectories under data/raw/
image_paths = list(Path("data/raw/images").rglob("*.jpg")) + list(Path("data/raw/images").rglob("*.png"))

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Ensure the image_detections table exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw.image_detections (
        id SERIAL PRIMARY KEY,
        message_id INT,
        object_class TEXT,
        confidence FLOAT
    );
""")
conn.commit()

# Run detection and insert results
for image_path in image_paths:
    filename = image_path.name

    # Skip files not following expected naming
    if not filename.startswith("message_") or "_" not in filename:
        continue

    try:
        message_id = int(filename.split("_")[1].split(".")[0])
    except (IndexError, ValueError):
        print(f"⚠️ Skipping {filename}: unable to extract message_id")
        continue

    results = model(str(image_path))

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0].item())  # class index
            conf = float(box.conf[0].item())  # confidence score
            label = model.names[cls]  # class name

            # Insert into database
            cursor.execute(
                """
                INSERT INTO raw.image_detections (message_id, object_class, confidence)
                VALUES (%s, %s, %s)
                """,
                (message_id, label, conf)
            )

conn.commit()
cursor.close()
conn.close()
print("✅ Detection complete and saved to PostgreSQL.")
