#src logic.py

from src.db import DatabaseManager

# ----------------------
# User Class
# ----------------------
class User:
    """
    Acts as a bridge between frontend (streamlit/FastAPI ) and the database.
    """
    def __init__(self, db: DatabaseManager):
        self.db = db

    def create(self, username: str, role: str = "voter"):
        return self.db.create_user(username, role)

    def read(self):
        return self.db.read_users()

    def update(self, user_id: str, new_username: str):
        return self.db.update_user(user_id, new_username)

    def delete(self, user_id: str):
        return self.db.delete_user(user_id)


# ----------------------
# Election Class
# ----------------------

class Election:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def create(self, title: str, start_date: str, end_date: str):
        return self.db.create_election(title, start_date, end_date)

    def read(self):
        return self.db.read_elections()

    def update(self, election_id: int, new_title: str):
        return self.db.update_election(election_id, new_title)

    def delete(self, election_id: int):
        return self.db.delete_election(election_id)


# ----------------------
# Candidate Class
# ----------------------

class Candidate:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def create(self, name: str, election_id: int):
        return self.db.create_candidate(name, election_id)

    def read(self):
        return self.db.read_candidates()

    def update(self, candidate_id: int, new_name: str):
        return self.db.update_candidate(candidate_id, new_name)

    def delete(self, candidate_id: int):
        return self.db.delete_candidate(candidate_id)


# ----------------------
# Vote Class
# ----------------------


class Vote:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def create(self, user_id: str, election_id: int, candidate_id: int):
        return self.db.create_vote(user_id, election_id, candidate_id)

    def read(self):
        return self.db.read_votes()

    def update(self, vote_id: int, new_candidate_id: int):
        return self.db.update_vote(vote_id, new_candidate_id)

    def delete(self, vote_id: int):
        return self.db.delete_vote(vote_id)


# ----------------------
# Voting System Main Class
# ----------------------


class VotingSystem:
    def __init__(self):
        self.db = DatabaseManager()
        self.users = User(self.db)
        self.elections = Election(self.db)
        self.candidates = Candidate(self.db)
        self.votes = Vote(self.db)

    def get_results(self, election_id: int):
        return self.db.get_results(election_id)

    def declare_winner(self, election_id: int):
        results = self.db.get_results(election_id)
        if not results:
            return {"Success": False, "Message": "No votes found for this election"}

        max_votes = max(results.values())
        winners = [candidate for candidate, votes in results.items() if votes == max_votes]

        return {"Success": True, "Winners": winners, "Votes": max_votes}


