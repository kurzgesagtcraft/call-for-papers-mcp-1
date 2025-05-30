import os
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/papers")
async def get_call_for_papers():
    # 实现获取征稿信息的逻辑
    return {"message": "Call for papers endpoint"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 3002)))