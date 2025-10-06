# api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.logic import VotingSystem, User
from src.db import DatabaseManager

# Initialize DB and voting system
db = DatabaseManager()
voting_system = VotingSystem()
userr = User(db)

app = FastAPI(title="TrueVote API", version="1.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Data Models ----------------
class VoteRequest(BaseModel):
    user_id: str
    election_id: int
    candidate_id: int

class UserCreate(BaseModel):
    username: str
    role: str = "voter"

class UserUpdate(BaseModel):
    username: str
    role: str

class ElectionCreate(BaseModel):
    title: str
    start_date: str
    end_date: str

class CandidateCreate(BaseModel):
    name: str
    election_id: int

# ---------------- API Endpoints ----------------
# ---------- Voting ----------
@app.post("/vote")
def cast_vote(vote: VoteRequest):
    try:
        result = voting_system.cast_vote(vote.user_id, vote.election_id, vote.candidate_id)
        return {"message": "Vote cast successfully", "vote": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/results/{election_id}")
def get_results(election_id: int):
    try:
        results = voting_system.get_results(election_id)
        if not results:
            return {"election_id": election_id, "results": {}, "winner": None, "message": "No votes yet"}
        max_votes = max(results.values())
        winners = [name for name, votes in results.items() if votes == max_votes]
        return {"election_id": election_id, "results": results, "winner": winners, "votes": max_votes}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------- Users ----------
@app.post("/users")
def create_user(user: UserCreate):
    try:
        result = userr.create(user.username, user.role)
        return {"message": "User created", "user": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users")
def get_users():
    try:
        return {"users": userr.read()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/users/{user_id}")
def update_user(user_id: str, user: UserUpdate):
    try:
        result = userr.update(user_id, user.username)
        return {"message": "User updated", "user": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    try:
        result = userr.delete(user_id)
        return {"message": "User deleted", "deleted": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------- Elections ----------
@app.post("/elections")
def create_election(election: ElectionCreate):
    try:
        result = voting_system.elections.create(election.title, election.start_date, election.end_date)
        return {"message": "Election created", "election": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/elections")
def get_elections():
    try:
        return {"elections": voting_system.elections.read()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------- Candidates ----------
@app.post("/candidates")
def create_candidate(candidate: CandidateCreate):
    try:
        result = voting_system.candidates.create(candidate.name, candidate.election_id)
        return {"message": "Candidate created", "candidate": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/candidates")
def get_candidates():
    try:
        return {"candidates": voting_system.candidates.read()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
