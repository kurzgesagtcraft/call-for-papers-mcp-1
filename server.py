from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import uvicorn
import traceback
from app import getEvents

app = FastAPI()

# Model for tool parameters
class ToolCallParams(BaseModel):
    method: str
    params: Dict[str, Any]
    id: Optional[str] = None
    jsonrpc: Optional[str] = "2.0"

# Tools definitions - matches smithery.json
TOOLS = [
    {
        "name": "getEvents",
        "description": "Search for conferences matching specific keywords",
        "parameters": [
            {
                "name": "keywords",
                "type": "string",
                "description": "Keywords to search for conferences (e.g., 'ai agent', 'machine learning')",
                "required": True
            },
            {
                "name": "limit",
                "type": "number",
                "description": "Maximum number of events to return",
                "required": False,
                "default": 10
            }
        ],
        "returns": {
            "type": "object",
            "description": "Conference search results"
        }
    }
]

@app.get("/")
async def root():
    return {"message": "Conference Searcher MCP is running"}

@app.post("/tools/list")
async def tools_list():
    return {
        "jsonrpc": "2.0",
        "result": TOOLS,
        "id": None
    }

@app.post("/tools/call")
async def tools_call(request: Request):
    try:
        # Parse the incoming JSON-RPC request
        data = await request.json()
        method = data.get("method")
        params = data.get("params", {})
        req_id = data.get("id")
        
        if method != "getEvents":
            raise HTTPException(status_code=400, detail=f"Method '{method}' not supported")
        
        # Extract parameters
        keywords = params.get("keywords")
        limit = params.get("limit", 10)
        
        if not keywords:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": "Invalid params: 'keywords' is required"
                },
                "id": req_id
            }
        
        # Call the actual function
        result = getEvents(keywords, limit)
        
        # Return JSON-RPC formatted response
        return {
            "jsonrpc": "2.0",
            "result": result,
            "id": req_id
        }
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        print(traceback.format_exc())
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            },
            "id": req_id if "req_id" in locals() else None
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
