from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI()

# -------- MODEL --------
class Action(BaseModel):
    type: str
    content: Optional[str] = None

# -------- TASKS (3 REQUIRED) --------
TASKS = [
    {
        "ticket": "I forgot my password",
        "keywords": ["password", "reset"]
    },
    {
        "ticket": "Payment deducted but failed",
        "keywords": ["refund", "payment"]
    },
    {
        "ticket": "App crashes on Android",
        "keywords": ["android", "fix"]
    }
]

state_data = {}
current_task = None

# -------- RESET --------
@app.post("/reset")
def reset():
    global state_data, current_task
    current_task = random.choice(TASKS)

    state_data = {
        "ticket": current_task["ticket"],
        "history": [],
        "retrieved_docs": [],
        "resolved": False
    }

    return state_data

# -------- GRADER --------
def grade_response(response):
    if not response:
        return 0.0

    score = 0
    for kw in current_task["keywords"]:
        if kw.lower() in response.lower():
            score += 1

    return min(score / len(current_task["keywords"]), 1.0)

# -------- STEP --------
@app.post("/step")
def step(action: Action):
    global state_data

    reward = 0.0
    done = False

    if action.type == "respond":
        reward = grade_response(action.content)

        if reward > 0.7:
            done = True
            state_data["resolved"] = True

    return {
        "state": state_data,
        "reward": float(reward),
        "done": done
    }

# -------- STATE --------
@app.get("/state")
def state():
    return state_data