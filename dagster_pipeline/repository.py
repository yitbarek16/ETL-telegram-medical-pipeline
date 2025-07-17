# dagster_pipeline/repository.py

from dagster import repository
from .pipeline_job import pipeline_job

@repository
def telegram_pipeline_repo():
    return [pipeline_job]
