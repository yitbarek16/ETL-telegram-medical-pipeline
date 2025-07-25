# dagster_pipeline/repository.py

from .pipeline_job import pipeline_job
from dagster import Definitions


defs = Definitions(
    jobs=[pipeline_job],
)
