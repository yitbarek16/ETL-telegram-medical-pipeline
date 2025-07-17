from fastapi import FastAPI, HTTPException, Query
from typing import List

from fastapi_app import crud, schemas

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Analytical APIs"}

@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct])
def top_products(limit: int = Query(10, ge=1, le=100)):
    products = crud.get_top_products(limit)
    return products

@app.get("/api/channels/{channel_name}/activity", response_model=List[schemas.ChannelActivity])
def channel_activity(channel_name: str):
    activity = crud.get_channel_activity(channel_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Channel not found or no activity")
    return activity

@app.get("/api/search/messages", response_model=List[schemas.Message])
def search_messages(query: str = Query(..., min_length=2)):
    results = crud.search_messages(query)
    return results
