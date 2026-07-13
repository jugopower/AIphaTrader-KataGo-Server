from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.schemas import AnalyzeRequest, AnalyzeResponse, CandidateMove

app = FastAPI(

    title="AlphaTrader KataGo Server",

    version="0.1.1",

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

        "build": "Build017.3A",

    }

@app.get("/health")

def health():

    return {

        "status": "healthy",

        "katago_ready": False,

        "mode": "demo",

        "build": "Build017.3A",

    }

@app.post("/analyze", response_model=AnalyzeResponse)

def analyze(request: AnalyzeRequest):

    move_count = len(request.moves)

    base_black = 0.50

    adjustment = min(move_count * 0.001, 0.08)

    if request.next_player == "B":

        winrate_black = base_black + adjustment

    else:

        winrate_black = base_black - adjustment

    winrate_black = max(0.05, min(0.95, winrate_black))

    winrate_white = 1.0 - winrate_black

    candidates = [

        CandidateMove(

            coordinate="Q16",

            winrate=round(winrate_black, 3),

            score_lead=1.2,

            policy=0.34,

            visits=min(request.visits, 100),

        ),

        CandidateMove(

            coordinate="D4",

            winrate=round(max(0.01, winrate_black - 0.04), 3),

            score_lead=0.6,

            policy=0.23,

            visits=max(1, min(request.visits // 2, 60)),

        ),

        CandidateMove(

            coordinate="K10",

            winrate=round(max(0.01, winrate_black - 0.08), 3),

            score_lead=-0.2,

            policy=0.15,

            visits=max(1, min(request.visits // 3, 40)),

        ),

    ]

    return AnalyzeResponse(

        status="ok",

        source="Build017.3A-demo",

        board_size=request.board_size,

        current_move=move_count,

        next_player=request.next_player,

        winrate_black=round(winrate_black, 3),

        winrate_white=round(winrate_white, 3),

        score_lead=1.2 if request.next_player == "B" else -1.2,

        candidates=candidates,

        message="示範分析資料，尚未連接真正 KataGo。",

    )
