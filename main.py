from fastapi import FastAPI
import os
import uvicorn
import logging
import asyncio
import random
import string

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.get("/env")
def read_env():
    var1 = os.getenv('VAR1', 'Not Set')
    sec1 = os.getenv('SEC1', 'Not Set')
    return {"VAR1": var1, "SEC1": sec1}

# Background task to log a random string every 5 seconds
async def log_random_string():
    while True:
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        logging.info(f"Random String: {random_string}")
        await asyncio.sleep(5)

# Start background tasks using FastAPI's on_event feature
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(log_random_string())

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
