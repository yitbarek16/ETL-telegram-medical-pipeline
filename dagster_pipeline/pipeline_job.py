# dagster_pipeline/pipeline_job.py

from dagster import op, job
import subprocess

@op
def scrape_telegram_data():
    # Run your telegram scraping script (adjust the command if needed)
    result = subprocess.run(["bash", "scripts/scrape_telegram.sh"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Scraping failed: {result.stderr}")
    print(result.stdout)
    return "Scraping done"

@op
def load_raw_to_postgres():
    # Run your raw data loading script
    result = subprocess.run(["bash", "scripts/load_raw_to_postgres.sh"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Loading raw to Postgres failed: {result.stderr}")
    print(result.stdout)
    return "Load to Postgres done"

@op
def run_dbt_transformations():
    # Run your dbt transformations
    result = subprocess.run(["dbt", "run"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"DBT run failed: {result.stderr}")
    print(result.stdout)
    return "DBT transformations done"

@op
def run_yolo_enrichment():
    # Run your YOLO enrichment script
    result = subprocess.run(["bash", "scripts/run_yolo.sh"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"YOLO enrichment failed: {result.stderr}")
    print(result.stdout)
    return "YOLO enrichment done"

@job
def pipeline_job():
    scrape_result = scrape_telegram_data()
    load_result = load_raw_to_postgres()
    dbt_result = run_dbt_transformations()
    yolo_result = run_yolo_enrichment()
