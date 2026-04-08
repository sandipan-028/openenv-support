from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI()

class Action(BaseModel):
    type: str
    content: Optional[str] = None

# 3 REQUIRED TASKS
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


# 🔥 FINAL BULLETPROOF GRADER
def grade_response(response):
    if not response:
        raw_score = 0.0
    else:
        score = 0
        for kw in current_task["keywords"]:
            if kw.lower() in response.lower():
                score += 1

        raw_score = score / len(current_task["keywords"])

    # FORCE STRICT RANGE (0,1)
    safe_score = 0.05 + (0.90 * raw_score)

    return float(safe_score)


@app.post("/step")
def step(action: Action):
    reward = grade_response(action.content)

    # ensure completion but avoid 1.0 edge
    done = reward > 0.9

    return {
        "state": state_data,
        "reward": reward,
        "done": done
    }


@app.get("/state")
def state():
    return state_data


# REQUIRED ENTRY POINT
def main():
    return app


# REQUIRED FOR VALIDATOR
if __name__ == "__main__":
    main()