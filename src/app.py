"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Practice teamwork, footwork, and game strategy on the field",
        "schedule": "Wednesdays, 3:45 PM - 5:15 PM",
        "max_participants": 18,
        "participants": []
    },
    "Basketball Club": {
        "description": "Work on shooting, defense, and fast-paced game play",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": []
    },
    "Drama Club": {
        "description": "Explore acting, stage performance, and character development",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Art Studio": {
        "description": "Create paintings, sketches, and mixed-media artwork",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": []
    },
    "Math Olympiad": {
        "description": "Solve advanced problems and prepare for math competitions",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific inquiry in a hands-on setting",
        "schedule": "Wednesdays, 3:30 PM - 4:45 PM",
        "max_participants": 20,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    normalized_email = (email or "").strip().lower()
    if not normalized_email:
        raise HTTPException(status_code=400, detail="Email is required")

    activity = activities[activity_name]
    participants = [participant.lower() for participant in activity["participants"]]

    # Prevent duplicate signups for the same person, regardless of email casing
    if normalized_email in participants:
        raise HTTPException(status_code=400, detail=f"{normalized_email} is already signed up for {activity_name}")

    # Prevent signups beyond capacity
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail=f"{activity_name} is already full")

    # Add student using a normalized form to prevent case-based duplicates later
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}


@app.delete("/activities/{activity_name}/signup")
def unregister_for_activity(activity_name: str, email: str):
    """Remove a student from an activity."""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    normalized_email = (email or "").strip().lower()
    if not normalized_email:
        raise HTTPException(status_code=400, detail="Email is required")

    activity = activities[activity_name]
    participant_emails = [participant.lower() for participant in activity["participants"]]

    if normalized_email not in participant_emails:
        raise HTTPException(status_code=404, detail=f"{normalized_email} is not signed up for {activity_name}")

    activity["participants"] = [
        participant for participant in activity["participants"]
        if participant.lower() != normalized_email
    ]

    return {"message": f"Removed {normalized_email} from {activity_name}"}
