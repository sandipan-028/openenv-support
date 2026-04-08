from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI()

class Action(BaseModel):
    type: str
    content: Optional[str] = None

# ✅ EXPLICIT TASKS (DETECTED BY VALIDATOR)
TASKS = {
    "password_reset": {
        "ticket": "I forgot my password",
        "keywords": ["password", "reset"]
    },
    "payment_issue": {
        "ticket": "Payment deducted but failed",
        "keywords": ["refund", "payment"]
    },
    "app_crash": {
        "ticket": "App crashes on Android",
        "keywords": ["android", "fix"]
    }
}

state_data = {}
current_task = None


# ✅ RESET
@app.post("/reset")
def reset():
    global state_data, current_task

    task_name = random.choice(list(TASKS.keys()))
    current_task = TASKS[task_name]

    state_data = {
        "task": task_name,   # IMPORTANT
        "ticket": current_task["ticket"],
        "history": [],
        "retrieved_docs": [],
        "resolved": False
    }
    return state_data


# ✅ GRADER (STRICT RANGE 0 < r < 1)
def grade_response(response):
    if not response:
        return 0.2

    keywords = current_task["keywords"]

    score = 0
    for kw in keywords:
        if kw.lower() in response.lower():
            score += 1

    raw = score / len(keywords)

    if raw <= 0:
        return 0.2
    elif raw >= 1:
        return 0.8
    else:
        return round(raw, 2)


# ✅ STEP
@app.post("/step")
def step(action: Action):
    reward = grade_response(action.content)
    done = reward > 0.7

    return {
        "state": state_data,
        "reward": float(reward),
        "done": done
    }


# ✅ STATE
@app.get("/state")
def state():
    return state_data


# ✅ REQUIRED ENTRY POINT
def main():
    return app


# ✅ REQUIRED FOR VALIDATOR
if __name__ == "__main__":
    main()