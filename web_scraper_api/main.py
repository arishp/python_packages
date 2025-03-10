from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests
import numpy as np
import database

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    database.create_table()

@app.get("/scrape/{url}")
async def scrape_data(url: str):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Example: Scrape titles and values from a hypothetical website
        titles = [item.text.strip() for item in soup.find_all("h2")] #Change to your website structure.
        values = [float(item.text.strip().replace("$", "")) for item in soup.find_all("p")] #Change to your website structure.

        for title, value in zip(titles, values):
            database.insert_data(title, value)

        return {"message": "Data scraped and stored successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/data")
async def get_data():
    data = database.get_all_data()
    return {"data": data}

@app.get("/analysis")
async def analyze_data():
    data = database.get_all_data()
    if not data:
        return {"error": "No data available"}

    values = [row[2] for row in data] # Extract the value column.
    average = np.mean(values)
    median = np.median(values)
    std_dev = np.std(values)

    return {
        "average": average,
        "median": median,
        "standard_deviation": std_dev,
        "average_from_database": database.get_average_value()
    }