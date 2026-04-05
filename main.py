import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Jura Bot OK 🚀"}

@app.post("/webhook/bot")
async def webhook(request: Request):
    try:
        data = await request.json()
        print(f"Webhook received: {data}")  # logs
        return {"ok": True}
    except Exception as e:
        print(f"Webhook error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
