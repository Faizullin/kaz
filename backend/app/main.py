from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.v1.api import api_router as api_v1_router
from app.api.routes.ws.api import api_router as api_ws_router


# from app.api.webhook import router as webhooks_router

@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


@app.websocket("/ws")
async def send_data(websocket: WebSocket):
    print('CONNECTING...', db.exec(select(ProjectDatabase)).all())
    await websocket.accept()
    while True:
        try:
            await websocket.receive_text()
            resp = {
                "message": "message from websocket"
            }
            await websocket.send_json(resp)
        except Exception as e:
            print(e)
            break
    print("CONNECTION DEAD...")


# Include routers
app.include_router(api_v1_router)
app.include_router(api_ws_router)


@app.get("/healthcheck")
def health_check():
    return {"status": "ok"}
