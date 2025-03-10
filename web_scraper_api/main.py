from fastapi import FastAPI
from contextlib import asynccontextmanager
from bs4 import BeautifulSoup
import requests
import numpy as np
import database

url = "https://en.wikipedia.org/wiki/MS_Dhoni"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    database.create_table()
    yield  # Wait here until the app is shutting down

app = FastAPI(lifespan=lifespan)

# app = FastAPI()

# @app.on_event("startup")
# async def startup_event():
#     database.create_table()

# @app.get("/scrape/{url}")
# async def scrape_data(url: str):
@app.get("/scrape")
async def scrape_data():
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Example: Scrape titles and values from a hypothetical website
        titles = [item.text.strip() for item in soup.find_all("h2")] #Change to your website structure.
        # values = [float(item.text.strip().replace("$", "")) for item in soup.find_all("p")] #Change to your website structure.
        values = [item.text.strip() for item in soup.find_all("p")] #Change to your website structure.

        for title, value in zip(titles, values):
            database.insert_data(title, value)

        return {"message": "Data scraped and stored successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/data")
async def get_data():
    data = database.get_all_data()
    return {"data": data}
