from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI()

# -------- ACTION MODEL --------
class Action(BaseModel):
    type: str
    content: Optional[str] = None

# -------- TASKS (3 REQUIRED) --------
TASKS = [
    {"ticket": "I forgot my password", "keywords": ["password", "reset"]},
    {"ticket": "Payment deducted but failed", "keywords": ["refund", "payment"]},
    {"ticket": "App crashes on Android", "keywords": ["android", "fix"]}
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

# -------- GRADER (NO DECIMALS, ONLY 0 or 1) --------
def grade_response(response):
    if not response:
        return 0  # integer

    for kw in current_task["keywords"]:
        if kw.lower() in response.lower():
            return 1  # integer

    return 0

# -------- STEP --------
@app.post("/step")
def step(action: Action):
    reward = grade_response(action.content)

    done = reward == 1

    return {
        "state": state_data,
        "reward": reward,   # integer only
        "done": done
    }

# -------- STATE --------
@app.get("/state")
def state():
    return state_data

# -------- REQUIRED ENTRY --------
def main():
    return app

# -------- REQUIRED FOR VALIDATOR --------
if __name__ == "__main__":
    main()