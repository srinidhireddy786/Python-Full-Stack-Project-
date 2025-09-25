# db_manager.py
import os
from supabase import create_client
from dotenv import load_dotenv

#load environment variables
load_dotenv()
url=os.getenv("https://oqoekskjzqrbxaxsejlt.supabase.co")
key=os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9xb2Vrc2tqenFyYnhheHNlamx0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODI1NzYsImV4cCI6MjA3MzY1ODU3Nn0.cH0WWp0apXulHB6A5GuKiFKVvg1DkKxTTd59CFfbJhQ")

supabase=create_client(url,key)

# Users Table crud
def create_user(username: str, role: str = "voter"):
    return supabase.table("users").insert(
        {"username": username,
          "role": role}).execute()

def read_users():
    return supabase.table("users").select("*").execute()

def update_user(user_id: str, new_username: str):
    return supabase.table("users").update({"username": new_username}).eq("user_id", user_id).execute()

def delete_user(user_id: str):
    return supabase.table("users").delete().eq("user_id", user_id).execute()

# ELECTIONS TABLE CRUD
def create_election(title: str, start_date: str, end_date: str):
    return supabase.table("elections").insert(
        {"title": title,
          "start_date": start_date,
            "end_date": end_date}
    ).execute()

def read_elections():
    return supabase.table("elections").select("*").execute()

def update_election(election_id: int, new_title: str):
    return supabase.table("elections").update({"title": new_title}).eq("election_id", election_id).execute()

def delete_election(election_id: int):
    return supabase.table("elections").delete().eq("election_id", election_id).execute()


# CANDIDATES TABLE CRUD

def create_candidate(name: str, election_id: int):
    return supabase.table("candidates").insert({"name": name, "election_id": election_id}).execute()

def read_candidates():
    return supabase.table("candidates").select("*").execute()

def update_candidate(candidate_id: int, new_name: str):
    return supabase.table("candidates").update({"name": new_name}).eq("candidate_id", candidate_id).execute()

def delete_candidate(candidate_id: int):
    return supabase.table("candidates").delete().eq("candidate_id", candidate_id).execute()


# VOTES TABLE CRUD

def create_vote(user_id: str, election_id: int, candidate_id: int):
    return supabase.table("votes").insert(
        {"user_id": user_id,
          "election_id": election_id,
            "candidate_id": candidate_id}
    ).execute()

def read_votes():
    return supabase.table("votes").select("*").execute()

def update_vote(vote_id: int, new_candidate_id: int):
    return supabase.table("votes").update({"candidate_id": new_candidate_id}).eq("vote_id", vote_id).execute()

def delete_vote(vote_id: int):
    return supabase.table("votes").delete().eq("vote_id", vote_id).execute()


# RESULTS

def get_results(election_id: int):
    response = supabase.table("votes").select("candidate_id, candidates(name)").eq("election_id", election_id).execute()
    results = {}
    for vote in response.data:
        name = vote["candidates"]["name"]
        results[name] = results.get(name, 0) + 1
    return results