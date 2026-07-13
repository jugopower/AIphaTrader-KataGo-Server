from typing import List, Literal, Optional

from pydantic import BaseModel, Field

class Move(BaseModel):

    color: Literal["B", "W"]

    coordinate: str

class AnalyzeRequest(BaseModel):

    board_size: int = Field(default=19, ge=9, le=19)

    moves: List[Move] = []

    next_player: Literal["B", "W"] = "B"

    komi: float = 6.5

    visits: int = Field(default=100, ge=1, le=1000)

    rules: str = "japanese"

class CandidateMove(BaseModel):

    coordinate: str

    winrate: float

    score_lead: float

    policy: float

    visits: int

class AnalyzeResponse(BaseModel):

    status: str

    source: str

    board_size: int

    current_move: int

    next_player: str

    winrate_black: float

    winrate_white: float

    score_lead: float

    candidates: List[CandidateMove]

    message: Optional[str] = None
