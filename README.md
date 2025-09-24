# TrueVote a voting platform

TrueVote is a secure, scalable, and user-friendly online voting system designed to simplify the election process for organizations, schools, and communities. It allows administrators to create and manage elections, register candidates, and monitor results, while voters can cast their votes easily and securely from any device.


## Features

- **User Authentication**: Secure login for voters and admins via Supabase Auth.

- **Election Management** : Admins can create elections with start/end dates and add candidates.

- **Voting Module** : Voters can view active elections and cast a single vote per election.

- **Result Calculation**: Automatic vote tallying and real-time results display.

- **Role-Based Access**: Admins have full management privileges, voters have restricted access.

- **Data Security**: One vote per user per election, with all data stored securely in a relational database.

## Project Structure

TrueVote/
|
|---src/          # core application logic
|   |---logic.py  # Business logic and task opearations
|   |__db.py      # Database operations
|
|----api/         # Backend API
|   |__main.py    # FastAPI endpoints
|
|----frontend/    # Frontend application
|   |__app.py     # Streamlit web interface
|
|___requirements.txt # Python Dependencies
|
|___README.md        # Project documentation
|
|___.env             # Python Variables


## Quick Start

### Prerequisites

-Python 3.8 or higher
-A Supabase account
-Git(Push,cloning)

### 1. Clone or Download the project
# Option 1: Clone with Git
git clone <repository-url>

# Option 2: Download and extract the ZIP file

### 2. Install Dependencies

# Install all required python packages
pip install -r requirements.txt

### 3.Set up Supabase Database

1.Create a Supabase Project:

2.Create the users,elections,candidates,votes Table:

-Go to the SQL Editor in your Supabase dashboard
-Run this SQL command:

```sql
CREATE TABLE users (
    user_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) UNIQUE NOT NULL,
    role TEXT CHECK (role IN ('admin','voter')) DEFAULT 'voter'
);
CREATE TABLE elections (
    election_id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL
);

CREATE TABLE candidates (
    candidate_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    election_id BIGINT REFERENCES elections(election_id) ON DELETE CASCADE
);

CREATE TABLE votes (
    vote_id BIGSERIAL PRIMARY KEY,
    user_id uuid REFERENCES users(user_id),
    election_id BIGINT REFERENCES elections(election_id),
    candidate_id BIGINT REFERENCES candidates(candidate_id),
    UNIQUE(user_id, election_id)  -- Prevents duplicate voting
);

```

3. **Get your credentials:

### 4. Configure Environment Variables

1.Create a new `.env` file in the project root 

2.Add your Supabase credentials to `.env`:
SUPABASE_URL="https://oqoekskjzqrbxaxsejlt.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9xb2Vrc2tqenFyYnhheHNlamx0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODI1NzYsImV4cCI6MjA3MzY1ODU3Nn0.cH0WWp0apXulHB6A5GuKiFKVvg1DkKxTTd59CFfbJhQ"


### 5. Run the Application 

## Streamlit Frontend
streamlit run frontend/app.py

The app will open in your browser at `http://localhost:8501`

## FastAPI Backend

cd api
python main.py

The API will be available at `http://localhost:8000`

# How to use

## Technical Details

### Technologies Used 

- **Frontend**: Streamlit (Python web framework)
- **Backend**: FastAPI (Python REST API framework)
-**Database**: Supabase (PostgreSQL-based backend-as-a-service)
-**Language**:Python 3.8++

### Key Components

1. **`src/db.py`**:Database operations
  --Handles all CRUD operations with Supabase

2. **`src/logic.py`**: Business logic
    -   Task validation and processing 

##  Troubleshooting

## Common Issues

1. **"Module not found" errors**
    -Make sure you've installed all dependencies: `pip install -r requirements.txt`
    -Check that you're running commands from the correct directory 

## Future Enhancements

-Ideas for extending this project:
-**Security**: Two-factor authentication, encrypted votes, audit logs

-**User Experience**: Mobile-friendly design, candidate profiles, vote confirmation emails

-**Admin Features:** Real-time dashboards, charts, export results, election history

-**Advanced Voting:** Support multiple elections/categories, weighted voting

-**Notifications**: Email/SMS reminders, vote alerts

-**Integration & Scalability:** APIs, cloud deployment, integration with external databases

## Support 

If you encounter any issues or have questions:

Mobile number:9618273065
Email:srinidhireddyyy786@gmail.com

