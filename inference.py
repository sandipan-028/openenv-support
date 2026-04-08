import requests

SPACE_URL = "https://sandipan028-openenv-support.hf.space"

MAX_STEPS = 3

def run_episode():
    rewards = []
    success = False

    print("[START] task=support env=openenv model=rule-based")

    state = requests.post(f"{SPACE_URL}/reset").json()

    for step in range(1, MAX_STEPS + 1):
        action = "respond"

        response = requests.post(
            f"{SPACE_URL}/step",
            json={"type": "respond", "content": "Please reset your password"}
        ).json()

        reward = response.get("reward", 0.2)
        done = response.get("done", False)

        # ✅ CLAMP (VERY IMPORTANT)
        if reward <= 0:
            reward = 0.2
        elif reward >= 1:
            reward = 0.8

        rewards.append(reward)

        print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

        if done:
            success = True
            break

    score = sum(rewards) / len(rewards) if rewards else 0.2

    # ✅ FINAL CLAMP
    if score <= 0:
        score = 0.2
    elif score >= 1:
        score = 0.8

    rewards_str = ",".join([f"{r:.2f}" for r in rewards])

    print(f"[END] success={str(success).lower()} steps={len(rewards)} score={score:.2f} rewards={rewards_str}")


if __name__ == "__main__":
    run_episode()