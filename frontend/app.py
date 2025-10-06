# frontend/app.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("🗳️ TrueVote - Online Voting System")

menu = ["Users", "Elections", "Candidates", "Voting", "Results"]
choice = st.sidebar.selectbox("Select Action", menu)

# ---------------- Users ----------------
if choice == "Users":
    st.header("👤 Manage Users")

    with st.form("create_user"):
        username = st.text_input("Username")
        role = st.selectbox("Role", ["voter", "admin"])
        submit = st.form_submit_button("Create User")
        if submit:
            response = requests.post(f"{API_URL}/users", json={"username": username, "role": role})
            st.json(response.json())

    if st.button("View All Users"):
        response = requests.get(f"{API_URL}/users")
        st.json(response.json())

# ---------------- Elections ----------------
elif choice == "Elections":
    st.header("🗳️ Manage Elections")

    with st.form("create_election"):
        title = st.text_input("Election Title")
        start_date = st.text_input("Start Date (YYYY-MM-DD HH:MM:SS)")
        end_date = st.text_input("End Date (YYYY-MM-DD HH:MM:SS)")
        submit = st.form_submit_button("Create Election")
        if submit:
            data = {"title": title, "start_date": start_date, "end_date": end_date}
            response = requests.post(f"{API_URL}/elections", json=data)
            st.json(response.json())

    if st.button("View Elections"):
        response = requests.get(f"{API_URL}/elections")
        st.json(response.json())

# ---------------- Candidates ----------------
elif choice == "Candidates":
    st.header("👥 Manage Candidates")

    with st.form("create_candidate"):
        name = st.text_input("Candidate Name")
        election_id = st.number_input("Election ID", min_value=1, step=1)
        submit = st.form_submit_button("Add Candidate")
        if submit:
            data = {"name": name, "election_id": election_id}
            response = requests.post(f"{API_URL}/candidates", json=data)
            st.json(response.json())

    if st.button("View Candidates"):
        response = requests.get(f"{API_URL}/candidates")
        st.json(response.json())

# ---------------- Voting ----------------
elif choice == "Voting":
    st.header("🗳️ Cast Your Vote")

    with st.form("cast_vote"):
        user_id = st.text_input("Enter User ID")
        election_id = st.number_input("Election ID", min_value=1, step=1)
        candidate_id = st.number_input("Candidate ID", min_value=1, step=1)
        submit = st.form_submit_button("Vote")
        if submit:
            data = {"user_id": user_id, "election_id": election_id, "candidate_id": candidate_id}
            response = requests.post(f"{API_URL}/vote", json=data)
            st.json(response.json())

# ---------------- Results ----------------
elif choice == "Results":
    st.header("📊 View Results")

    election_id = st.number_input("Election ID", min_value=1, step=1)
    if st.button("Get Results"):
        response = requests.get(f"{API_URL}/results/{election_id}")
        st.json(response.json())
