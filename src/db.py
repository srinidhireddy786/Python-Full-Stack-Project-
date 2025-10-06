# src/db.py
import os
from supabase import create_client
from dotenv import load_dotenv

class DatabaseManager:
    def __init__(self):
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        if not url or not key:
            raise ValueError("SUPABASE_URL or SUPABASE_KEY not set in .env file")

        self.supabase = create_client(url, key)

    # ---------------- USERS ----------------
    def create_user(self, username: str, role: str = "voter"):
        return self.supabase.table("users").insert({"username": username, "role": role}).execute().data

    def read_users(self):
        return self.supabase.table("users").select("*").execute().data

    def update_user(self, user_id: str, new_username: str):
        return self.supabase.table("users").update({"username": new_username}).eq("user_id", user_id).execute().data

    def delete_user(self, user_id: str):
        return self.supabase.table("users").delete().eq("user_id", user_id).execute().data

    # ---------------- ELECTIONS ----------------
    def create_election(self, title: str, start_date: str, end_date: str):
        return self.supabase.table("elections").insert({"title": title, "start_date": start_date, "end_date": end_date}).execute().data

    def read_elections(self):
        return self.supabase.table("elections").select("*").execute().data

    def update_election(self, election_id: int, new_title: str):
        return self.supabase.table("elections").update({"title": new_title}).eq("election_id", election_id).execute().data

    def delete_election(self, election_id: int):
        return self.supabase.table("elections").delete().eq("election_id", election_id).execute().data

    # ---------------- CANDIDATES ----------------
    def create_candidate(self, name: str, election_id: int):
        return self.supabase.table("candidates").insert({"name": name, "election_id": election_id}).execute().data

    def read_candidates(self):
        return self.supabase.table("candidates").select("*").execute().data

    def update_candidate(self, candidate_id: int, new_name: str):
        return self.supabase.table("candidates").update({"name": new_name}).eq("candidate_id", candidate_id).execute().data

    def delete_candidate(self, candidate_id: int):
        return self.supabase.table("candidates").delete().eq("candidate_id", candidate_id).execute().data

    # ---------------- VOTES ----------------
    def create_vote(self, user_id: str, election_id: int, candidate_id: int):
        return self.supabase.table("votes").insert({"user_id": user_id, "election_id": election_id, "candidate_id": candidate_id}).execute().data

    def read_votes(self):
        return self.supabase.table("votes").select("*").execute().data

    def update_vote(self, vote_id: int, new_candidate_id: int):
        return self.supabase.table("votes").update({"candidate_id": new_candidate_id}).eq("vote_id", vote_id).execute().data

    def delete_vote(self, vote_id: int):
        return self.supabase.table("votes").delete().eq("vote_id", vote_id).execute().data

    # ---------------- RESULTS ----------------
    def get_results(self, election_id: int):
        response = self.supabase.table("votes").select("candidate_id, candidates(name)").eq("election_id", election_id).execute()
        results = {}
        for vote in response.data:
            name = vote["candidates"]["name"]
            results[name] = results.get(name, 0) + 1
        return results
