# Frontend ---> API ----> logic ----> db ----> Response
#api/main.py

from fastapi import FASTAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys,os


# Import Taskmanager from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import VotingSystem,User

#---------------------App Setup------------

app=FASTAPI(title="TrueVote  API ",version ="1.0")

#----------------------Allow frontend (Streamlit/React) to call the API---------

app.add_middleware(
    CORSMiddleware,
    allow_origin=["*"], # allow all origins (frontend apps)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

voting_system = VotingSystem()
userr=User()
#----------Data Models----------

class VoteRequest(BaseModel):
    """
    Schema for creating a task
    """
    user_id: str
    election_id: int
    candidate_id: int

class ResultsRequest(BaseModel):
    election_id: int

class UserCreate(BaseModel):
    username: str
    role: str = "voter"  # default role

class UserUpdate(BaseModel):
    username: str
    role: str

# --------------------- API Endpoints ---------------------
@app.post("/vote")
def cast_vote(vote: VoteRequest):
    try:
        result = voting_system.cast_vote(
            user_id=vote.user_id,
            election_id=vote.election_id,
            candidate_id=vote.candidate_id
        )
        return {"message": "Vote cast successfully", "vote": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/results/{election_id}")
def get_results(election_id: int):
    try:
        results = voting_system.get_results(election_id)
        if not results:
            return {
                "election_id": election_id,
                "results": results,
                "winner": None,
                "message": "No votes have been cast yet"
            }

        # Determine winner(s)
        max_votes = max(results.values())
        winners = [name for name, votes in results.items() if votes == max_votes]

        return {
            "election_id": election_id,
            "results": results,
            "winner": winners,
            "votes": max_votes
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# --------------------- Create User ---------------------
@app.post("/users")
def create_user(user: UserCreate):
    try:
        result = userr.create(user.username, user.role)
        return {"message": "User created successfully", "user": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --------------------- Get All Users ---------------------
@app.get("/users")
def get_users():
    try:
        users = userr.read()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --------------------- Update User ---------------------
@app.put("/users/{user_id}")
def update_user(user_id: str, user: UserUpdate):
    try:
        result = userr.update(user_id, user.username, user.role)
        return {"message": "User updated successfully", "user": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --------------------- Delete User ---------------------
@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    try:
        result = userr.delete(user_id)
        return {"message": "User deleted successfully", "deleted": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
if __name__=="__main__":
    import uvicorn 
    uvicorn.run("api.main:app",host="0.0.0.0",port=8000,reload=True)