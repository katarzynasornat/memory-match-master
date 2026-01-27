import httpx

BASE_URL = "http://localhost:3000"

def test_submission():
    with httpx.Client() as client:
        # 1. Login
        print("Testing Login...")
        login_resp = client.post(f"{BASE_URL}/auth/login", json={
            "email": "tester@example.com",
            "password": "password123"
        })
        
        if login_resp.status_code != 200:
            print(f"Login failed: {login_resp.text}")
            return
        
        auth_data = login_resp.json()
        token = auth_data["token"]
        email = auth_data["user"]["email"]
        print(f"Logged in as {email}, token: {token}")

        # 2. Submit Score
        print("\nTesting Score Submission...")
        submit_resp = client.post(
            f"{BASE_URL}/leaderboard",
            json={"email": email, "score": 1337, "round": 10},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"Status: {submit_resp.status_code}")
        print(f"Response: {submit_resp.text}")

        # 3. Check Leaderboard
        print("\nFetching Leaderboard...")
        lb_resp = client.get(f"{BASE_URL}/leaderboard")
        entries = lb_resp.json()
        print(f"Leaderboard size: {len(entries)}")
        
        found = any(entry["score"] == 1337 and entry["email"] == email for entry in entries)
        if found:
            print("SUCCESS: 1337 points found on leaderboard!")
        else:
            print("FAILURE: 1337 points NOT found on leaderboard.")
            print("Current Entries:")
            for e in entries:
                print(f" - {e['email']}: {e['score']}")

if __name__ == "__main__":
    test_submission()
