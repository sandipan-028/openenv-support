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


# ✅ STRICT (0,1) RANGE GRADER
def grade_response(response):
    if not response:
        return 0.2

    score = 0
    for kw in current_task["keywords"]:
        if kw.lower() in response.lower():
            score += 1

    total = len(current_task["keywords"])
    raw = score / total

    if raw <= 0:
        return 0.2
    elif raw >= 1:
        return 0.8
    else:
        return round(raw, 2)


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


def main():
    return app


if __name__ == "__main__":
    main()