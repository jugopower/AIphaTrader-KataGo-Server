from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(

    title="AlphaTrader KataGo Server",

    version="0.1.0",

)

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],

)

@app.get("/")

def root():

    return {

        "status": "ok",

        "service": "AlphaTrader-KataGo-Server",

        "message": "API server is running",

        "katago_ready": False,

    }

@app.get("/health")

def health():

    return {

        "status": "healthy",

        "katago_ready": False,

        "mode": "demo",

    }
