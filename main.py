# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# # ---- Request model ----
# class WildlifeRequest(BaseModel):
#     location: str
#     trail: str | None = None

# # ---- MCP Tool Endpoint ----
# @app.post("/get_common_wildlife")
# def get_common_wildlife(request: WildlifeRequest):
#     # TEMP: hardcoded response (totally fine for the challenge)
#     animals = [
#         "mule deer",
#         "elk",
#         "prairie dogs",
#         "red-tailed hawks",
#         "black bears (rare, but possible)"
#     ]

#     return {
#         "location": request.location,
#         "trail": request.trail,
#         "common_wildlife": animals,
#         "safety_note": "Keep distance from wildlife and store food properly."
#     }

from fastapi import FastAPI, Query, Header, HTTPException
import sqlite3
from datetime import datetime, timedelta
from typing import Optional
from fastapi.responses import JSONResponse

DB_PATH = "wildlife.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello, Telnyx!"}

# MCP tools listing
@app.get("/tools")
def list_tools():
    tools = [
        {
            "name": "wildlife_lookup",
            "description": "Get common animals for a trail",
            "url": "https://hyperbatically-nonpungent-randy.ngrok-free.dev/wildlife",
            "method": "GET",
            "parameters": [{"name": "trail", "type": "string", "required": True}]
        },
        {
            "name": "get_safety_tips",
            "description": "Get safety tips for a specific animal",
            "url": "https://hyperbatically-nonpungent-randy.ngrok-free.dev/safety_tips",
            "method": "GET",
            "parameters": [{"name": "animal", "type": "string", "required": True}]
        },
        {
            "name": "recent_sightings",
            "description": "Get recent wildlife sightings",
            "url": "https://hyperbatically-nonpungent-randy.ngrok-free.dev/recent_sightings",
            "method": "GET",
            "parameters": [
                {"name": "area", "type": "string", "required": False},
                {"name": "trail", "type": "string", "required": False},
                {"name": "animal", "type": "string", "required": False}
            ]
        }
    ]
    return JSONResponse({"tools": tools})

#TELNYX_SECRET = "wildlife"

# @app.get("/tools")
# def list_tools(authorization: str | None = Header(None)):
#     if authorization != TELNYX_SECRET:
#         raise HTTPException(status_code=401, detail="Unauthorized")

#     return JSONResponse({
#         "tools": [
#             {
#                 "name": "wildlife_lookup",
#                 "description": "Get common animals for a trail",
#                 "url": "https://hyperbatically-nonpungent-randy.ngrok-free.dev/wildlife",
#                 "method": "GET",
#                 "parameters": [{"name": "trail", "type": "string", "required": True}]
#             },
#             {
#                 "name": "get_safety_tips",
#                 "description": "Get safety tips for a specific animal",
#                 "url": "https://hyperbatically-nonpungent-randy.ngrok-free.dev/safety_tips",
#                 "method": "GET",
#                 "parameters": [{"name": "animal", "type": "string", "required": True}]
#             },
#             {
#                 "name": "recent_sightings",
#                 "description": "Get recent wildlife sightings",
#                 "url": "https://hyperbatically-nonpungent-randy.ngrok-free.dev/recent_sightings",
#                 "method": "GET",
#                 "parameters": [
#                     {"name": "area", "type": "string", "required": False},
#                     {"name": "trail", "type": "string", "required": False},
#                     {"name": "animal", "type": "string", "required": False}
#                 ]
#             }
#         ]
#     })


@app.get("/wildlife")
def wildlife(trail: str):
    # Sample data – we’ll replace with real API or database later
    sample_data = {
        "Green Mountain": ["Black Bear", "Elk", "Red Fox"],
        "Bear Peak": ["Mountain Lion", "Deer", "Raven", "Elk"]
    }
    animals = sample_data.get(trail, ["No data for this trail"])
    return {"trail": trail, "animals": animals}

@app.get("/safety_tips")
def safety_tips(animal: str):
    sample_data = {
        "Black Bear": "Stay calm, don't run (they're fast!), talk calmly to identify yourself as human, make yourself look big, and back away slowly, giving the bear an escape route",
        "Elk": "Never approach, feed, or corner them, keep pets leashed, stay near your vehicle or large obstacles, and be extra cautious driving at dawn/dusk as they become aggressive when threatened or protecting young",
        "Red Fox": "never feed or approach them, keep pets supervised, and make noise to scare them off",
        "Mountain Lion": "Stay calm and don't run. Appear large by raising your arms. Speak loudly and don't crouch. Throw things if it approaches"
    }
    safety_tips = sample_data.get(animal,["No data for this animal"])
    return {"animal": animal, "safety_tips": safety_tips}




@app.get("/recent_sightings")
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



    # @app.get("/recent_sightings")
# def recent_sightings(trail: str = None, area: str = None):
#     conn = sqlite3.connect("wildlife.db")
#     cursor = conn.cursor()

#     # Simplified query with no date filtering
#     query = """
#         SELECT area, trail, animal, date
#         FROM sightings
#     """

#     # Add filters if provided
#     filters = []
#     params = []

#     if trail:
#         filters.append("trail = ?")
#         params.append(trail)
#     if area:
#         filters.append("area = ?")
#         params.append(area)

#     if filters:
#         query += " WHERE " + " AND ".join(filters)

#     cursor.execute(query, params)
#     rows = cursor.fetchall()
#     conn.close()

#     sightings = [{"area": r[0], "trail": r[1], "animal": r[2], "date": r[3]} for r in rows]
#     return {"count": len(sightings), "sightings": sightings}
    

# @app.get("/recent_sightings")
# def recent_sightings(area: str, animal: str = None):
#     conn = sqlite3.connect("wildlife.db")
#     cursor = conn.cursor()
#     query = "SELECT area, trail, animal, date FROM sightings WHERE area = ?"
#     params = [area]

#     if animal:
#         query += " AND animal = ?"
#         params.append(animal)

#     cursor.execute(query, params)
#     rows = cursor.fetchall()
#     conn.close()
#     return {"count": len(rows), "sightings": [{"area": r[0], "trail": r[1], "animal": r[2], "date": r[3]} for r in rows]}