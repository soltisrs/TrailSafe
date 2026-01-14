from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
import sqlite3

# -------------------------------------------------
# Create the FastAPI application
# This is the core web server that will expose
# HTTP endpoints and MCP tools
# -------------------------------------------------
app = FastAPI()

# -------------------------------------------------
# Database configuration
# SQLite is used here for simplicity
# -------------------------------------------------
DB_PATH = "wildlife.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
# -------------------------------------------------
# MCP Tool: Get wildlife commonly found on a trail
# This endpoint is exposed to the MCP server so
# the voice AI can answer questions like:
#   "What animals are on Bear Peak?"
# -------------------------------------------------
@app.get("/wildlife", operation_id="get_wildlife")
def wildlife(trail: str):
    # Sample data
    sample_data = {
        "Green Mountain": ["Black Bear", "Elk", "Red Fox"],
        "Bear Peak": ["Mountain Lion", "Deer", "Raven", "Elk"]
    }
    # Look up animals for the given trail
    # If the trail is unknown, search the general area
    animals = sample_data.get(trail, ["No data for this trail"])
    return {"trail": trail, "animals": animals}
# -------------------------------------------------
# MCP Tool: Get safety tips for a specific animal
# Used by the voice assistant when a user asks:
#   "What should I do if I see a bear?"
# -------------------------------------------------
@app.get("/safety_tips", operation_id="get_safety_tips")
def safety_tips(animal: str):
    # Small sample data for now. Future considerations include expanding this. 
    # AI Assistant will use LLM to look up anyanimals not included
    sample_data = {
        "Black Bear": "Stay calm, don't run (they're fast!), talk calmly to identify yourself as human, make yourself look big, and back away slowly, giving the bear an escape route",
        "Elk": "Never approach, feed, or corner them, keep pets leashed, stay near your vehicle or large obstacles, and be extra cautious driving at dawn/dusk as they become aggressive when threatened or protecting young",
        "Red Fox": "never feed or approach them, keep pets supervised, and make noise to scare them off",
        "Mountain Lion": "Stay calm and don't run. Appear large by raising your arms. Speak loudly and don't crouch. Throw things if it approaches"
    }
    # Return safety tips if we have them, otherwise a fallback message
    safety_tips = sample_data.get(animal,["No data for this animal"])
    return {"animal": animal, "safety_tips": safety_tips}
# -------------------------------------------------
# MCP Tool: Query recent wildlife sightings
# This endpoint dynamically builds a SQL query
# based on which filters the user provides
# -------------------------------------------------
@app.get("/recent_sightings", operation_id="get_recent_sightings")
def recent_sightings(
    area: str = None,
    trail: str = None,
    animal: str = None
):
    # Open a database connection
    conn = sqlite3.connect("wildlife.db")
    cursor = conn.cursor()

    # Base query
    query = "SELECT area, trail, animal, date FROM sightings"
    params = []
    conditions = []

    # Add SQL WHERE clauses dynamically
    # based on which parameters are provided
    if area:
        conditions.append("area = ?")
        params.append(area)
    if trail:
        conditions.append("trail = ?")
        params.append(trail)
    if animal:
        conditions.append("animal = ?")
        params.append(animal)
        
    # If any filters were added, attach them
    # to the base query using AND logic
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    # Execute the query safely with parameters
    cursor.execute(query, params)
    rows = cursor.fetchall()
    # Close the database connection
    conn.close()

    # Format database rows into JSON-friendly objects
    return {
        "count": len(rows),
        "sightings": [
            {"area": r[0], "trail": r[1], "animal": r[2], "date": r[3]} for r in rows
        ]
    }

@app.post("/webhooks/telnyx/inbound")
async def telnyx_inbound(request: Request):
    """
    Handles inbound requests from Telnyx (required by Voice API Application).
    Responds with a simple greeting or can trigger MCP tools.
    """
    body = await request.json()
    print("Inbound Telnyx payload:", body)  # log for debugging

    # Respond with simple text-to-speech
    return {
        "actions": [
            {"say": {"text": "TrailSafe is online. Ask me about wildlife or safety tips!"}}
        ]
    }
# -------------------------------------------------
# MCP Server Setup
# This exposes selected FastAPI endpoints
# as callable MCP tools for the voice AI
# ----------------------------------------
mcp = FastApiMCP(app,include_operations=['get_recent_sightings','get_wildlife','get_safety_tips'])
# Mount the MCP server so it is available at /mcp
mcp.mount()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)
