# TrailSafe Wildlife AI Assistant 
TrailSafe is an AI assistant designed to help hikers stay safe by providing:

● Wildlife information for a specific area or trail.  
● Safety tips for encounters with animals.   
● Recent wildlife sightings pulled from a database.   

Tech Stack:   
Backend: Python, FastAPI, FastApiMCP  
Database: SQLite  
Voice Interaction: Telnyx   


--------------------------------------------------------------------------------------------------------------------------
## Setup/Installation  
1. Clone the Repository  
```git clone https://github.com/soltisrs/TrailSafe.git```  
```cd TrailSafe```
3. Create a Python virtual environment  
```python -m venv venv```  
```source venv/bin/activate   # Linux / Mac```  
```venv\Scripts\activate      # Windows```  
4. Install Dependences  
```pip install -r requirements.txt```
5. Start FastAPI Server  
```uvicorn main:app --reload --host 0.0.0.0 --port 8000```   
6. (Optional) use ngrok for backend testing  
   ```ngrok http 8000```
--------------------------------------------------------------------------------------------------------------------------
## Endpoints / MCP Tools  
The following MCP tools are exposed by the server:  
  
Endpoint: ```/wildlife```  Operation ID: ```get_wildlife```  Description: ```Returns animals commonly seen on a given trail```    
Endpoint: ```/safety_tips```  Operation ID: ```get_safety_tips```  Description: ```Provides safety tips for a specific animal```   
Endpoint: ```/recent_sightings```  Operation ID: ```get_recent_sightings```  Description: ```Returns recent sightings filtered by trail, area, or animal``` 

Example MCP Tool Usage  
```GET /wildlife?trail=Bear%20Peak ```

``` Response: { "trail": "Bear Peak",  "animals": ["Mountain Lion", "Deer", "Raven", "Elk"] } ```

--------------------------------------------------------------------------------------------------------------------------
## Example Conservation Flow with AI Assistant 

Available on phone number: 720-912-0944  

Prompt: “Where are you hiking today?”   
Ideal Answer: ```Boulder, CO``` (can list anywhere in the United States)   
  
Prompt: “What is the name of the trail?”  
Ideal Answers: ```Green Mountain```, ```Bear Peak```  
Will default to giving information about the area if trail is not found  
  
Prompt: “Do you want to hear safety information for any of the animals?”  
Answers: ```{animal}```  
  
Prompt: “Would you like to hear about animal sightings in your area?”  
Answer Examples: Yes, have there been any ```mountain lion sightings```?”, “Yes, tell me ```all sightings``` for the trail” 
  
Prompt: “Anything else?”  
Answer Examples: “Yes, tell me safety information about ```{animal}```”  
```No``` to end the call  
  
Note: I used a small sample data table given time constraints. Future considerations include expanding dataset  


--------------------------------------------------------------------------------------------------------------------------
