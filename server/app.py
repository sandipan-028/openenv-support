from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI()

class Action(BaseModel):
    type: str
    content: Optional[str] = None

TASKS = [
    {"ticket": "I forgot my password", "keywords": ["password", "reset"]},
    {"ticket": "Payment deducted but failed", "keywords": ["refund", "payment"]},
    {"ticket": "App crashes on Android", "keywords": ["android", "fix"]}
]

state_data = {}
current_task = None

@app.get("/")
def home():
    return {"status": "running"}

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

def grade_response(response):
    if not response:
        return 0.0

    score = 0
    for kw in current_task["keywords"]:
        if kw.lower() in response.lower():
            score += 1

    return min(score / len(current_task["keywords"]), 1.0)

@app.post("/step")
def step(action: Action):
    reward = grade_response(action.content)
    done = reward > 0.7

    return {
        "state": state_data,
        "reward": float(reward),
        "done": done
    }

@app.get("/state")
def state():
    return state_data

# REQUIRED
def main():
    return app