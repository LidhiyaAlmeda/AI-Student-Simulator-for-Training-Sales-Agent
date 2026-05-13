import requests

BASE_URL = "http://127.0.0.1:8000"

def get_ai_response(user_input, persona_details):
    try:
        payload = {
            "message": user_input,
            "persona": persona_details
        }
        # Timeout 10 seconds పెట్టాను
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # టెక్స్ట్ మరియు స్కోర్ రెండూ వచ్చేలా సెట్ చేశాను
            return {
                "text": data.get("response", "No reply."),
                "score": data.get("score", None) # బ్యాకెండ్ స్కోర్ ఇస్తే ఇక్కడ వస్తుంది
            }
        else:
            return {"text": "⚠️ Student is not responding properly.", "score": None}
    except Exception:
        return {"text": "🔌 Connection Error: Start the Backend Server!", "score": None}
