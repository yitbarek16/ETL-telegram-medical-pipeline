# ETL Telegram Medical Pipeline

This project builds a full ETL (Extract, Transform, Load) pipeline to collect, process, and model message data from public Telegram channels related to healthcare and medical topics. It is containerized with Docker, leverages PostgreSQL for storage, and uses dbt for data modeling and transformation.

---

## what i did in this project

### Project Setup & Data Ingestion

- Initialized Git and GitHub repository for version control.
- Created a Docker-based development environment using `docker-compose`, with:
  - `db`: PostgreSQL 14 database.
  - `python`: Python 3 container with required dependencies.
- Created `.env` to securely store credentials (`POSTGRES_USER`, `POSTGRES_PASSWORD`, etc.).
- Used `telethon` to collect message history from public Telegram channels.
- Stored messages in newline-delimited `.jsonl` format in a structured data lake (`/data/channel_name/date.jsonl`).
- Built a Python script to load raw JSONL files into a `raw.telegram_messages` table in PostgreSQL.

### Raw Layer and Schema Setup 

- Designed and created PostgreSQL schemas:
  - `raw` – Stores raw ingested messages.
  - `raw_staging` – For cleaned staging models.
  - `raw_analytics` – Final fact/dimension models.
- Verified data load into `raw.telegram_messages` using SQL CLI.
- Ensured that Docker volumes and working directories allow seamless container access to the database and source files.

### Data Modeling & Transformation with dbt

- Installed and initialized a `dbt` project inside the Python container.
- Created **staging models**:
  - `stg_telegram_messages.sql`: Casts data types, extracts relevant fields, normalizes JSON structure.
- Built **mart models** using a **star schema**:
  - `dim_channels`: Channel metadata.
  - `dim_dates`: Calendar dimension.
  - `fct_messages`: Fact table with foreign keys and message metrics.
- Ran transformation pipelines using:
  ```bash
  dbt run --select staging
  dbt run --select marts

## Analytical Data Modeling with dbt

** Goal:**  
Transform raw Telegram messages and YOLOv5 image detection data into clean, analytical models using [dbt].

### Setup

- Installed `dbt-postgres`
- Configured `profiles.yml` to connect to PostgreSQL
- Defined models in the following structure:


###  Summary of Models

| Model Name              | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `stg_telegram_messages` | Cleaned and standardized Telegram messages                                  |
| `stg_image_detections`  | Cleaned YOLOv5 output (object classes and bounding boxes)                   |
| `fct_messages`          | Fact table with metadata like `channel_id`, `message_id`, `media_type`, etc. |
| `fct_image_detections`  | Analytical view to count and explore object detection results per message   |

##  Analytical API with FastAPI

** Goal:**  
Build a REST API that serves analytical insights from DBT-transformed data.

###  Tech Stack

- FastAPI  
- Uvicorn  
- psycopg2-binary  

## Pipeline Orchestration with Dagster

**Goal:**  
Convert the data pipeline into a robust, observable job using [Dagster](https://dagster.io/).

### Setup

```bash
pip install dagster dagster-webserver
