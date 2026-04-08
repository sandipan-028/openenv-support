import requests
import os
from openai import OpenAI

SPACE_URL = os.getenv("SPACE_URL", "https://sandipan028-openenv-support.hf.space")

# ✅ REQUIRED ENV
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY,
)

MAX_STEPS = 5

def format_reward(r):
    return f"{r:.2f}"

def main():
    step_count = 0
    rewards = []
    success = False

    try:
        state = requests.post(f"{SPACE_URL}/reset").json()

        print("[START] task=support env=openenv model=llm")

        done = False

        while not done and step_count < MAX_STEPS:
            step_count += 1

            # ✅ LLM CALL (MANDATORY)
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": state["ticket"]}],
            )

            text = response.choices[0].message.content

            action = {
                "type": "respond",
                "content": text
            }

            result = requests.post(f"{SPACE_URL}/step", json=action).json()

            reward = float(result.get("reward", 0.0))
            done = bool(result.get("done", False))
            state = result.get("state", {})

            rewards.append(reward)

            print(
                f"[STEP] step={step_count} action=respond "
                f"reward={format_reward(reward)} done={str(done).lower()} error=null"
            )

        score = sum(rewards) / max(len(rewards), 1)
        success = True if score > 0 else False

    except Exception:
        print("[END] success=false steps=0 score=0.00 rewards=")
        return

    rewards_str = ",".join(format_reward(r) for r in rewards)

    print(
        f"[END] success={str(success).lower()} "
        f"steps={step_count} score={format_reward(score)} rewards={rewards_str}"
    )

if __name__ == "__main__":
    main()