from dagster import job, op

import subprocess

@op
def scrape_telegram_data():
    subprocess.run(["python", "scripts/scrape_telegram.py"], check=True)

@op
def load_raw_to_postgres(_):
    subprocess.run(["python", "scripts/load_to_postgres.py"], check=True)

@op
def run_dbt_transformations(_):
    subprocess.run(["dbt", "run", "--profiles-dir", ".", "--project-dir", "."], check=True)

@op
def run_yolo_enrichment(_):
    subprocess.run(["python", "scripts/detect_objects.py"], check=True)

@job
def pipeline_job():
    run_yolo_enrichment(
        run_dbt_transformations(
            load_raw_to_postgres(
                scrape_telegram_data()
            )
        )
    )
