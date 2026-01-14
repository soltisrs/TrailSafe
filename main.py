from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
import sqlite3
# from datetime import datetime, timedelta
# from typing import Optional

app = FastAPI()


DB_PATH = "wildlife.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/wildlife", operation_id="get_wildlife")
def wildlife(trail: str):
    # Sample data – we’ll replace with real API or database later
    sample_data = {
        "Green Mountain": ["Black Bear", "Elk", "Red Fox"],
        "Bear Peak": ["Mountain Lion", "Deer", "Raven", "Elk"]
    }
    animals = sample_data.get(trail, ["No data for this trail"])
    return {"trail": trail, "animals": animals}

@app.get("/safety_tips", operation_id="get_safety_tips")
def safety_tips(animal: str):
    sample_data = {
        "Black Bear": "Stay calm, don't run (they're fast!), talk calmly to identify yourself as human, make yourself look big, and back away slowly, giving the bear an escape route",
        "Elk": "Never approach, feed, or corner them, keep pets leashed, stay near your vehicle or large obstacles, and be extra cautious driving at dawn/dusk as they become aggressive when threatened or protecting young",
        "Red Fox": "never feed or approach them, keep pets supervised, and make noise to scare them off",
        "Mountain Lion": "Stay calm and don't run. Appear large by raising your arms. Speak loudly and don't crouch. Throw things if it approaches"
    }
    safety_tips = sample_data.get(animal,["No data for this animal"])
    return {"animal": animal, "safety_tips": safety_tips}




@app.get("/recent_sightings", operation_id="get_recent_sightings")
def recent_sightings(
    area: str = None,
    trail: str = None,
    animal: str = None
):
    conn = sqlite3.connect("wildlife.db")
    cursor = conn.cursor()

    # Base query
    query = "SELECT area, trail, animal, date FROM sightings"
    params = []
    conditions = []

    # Add filters dynamically
    if area:
        conditions.append("area = ?")
        params.append(area)
    if trail:
        conditions.append("trail = ?")
        params.append(trail)
    if animal:
        conditions.append("animal = ?")
        params.append(animal)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return {
        "count": len(rows),
        "sightings": [
            {"area": r[0], "trail": r[1], "animal": r[2], "date": r[3]} for r in rows
        ]
    }

mcp = FastApiMCP(app,include_operations=['get_recent_sightings','get_wildlife','get_safety_tips'])
mcp.mount()
