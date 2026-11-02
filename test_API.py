import json
import sys
import requests

BASE_URL = "http://127.0.0.1:8000"
PREDICT_URL = "http://127.0.0.1:8000/predict"


def print_response(title: str, response: requests.Response) -> None:
    """Helper to neatly print the HTTP status code and JSON response body."""
    print(f"=== {title} ===")
    print(f"URL: {response.url}")
    print(f"Status Code: {response.status_code}")
    try:
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
    except ValueError:
        print(f"Raw Response: {response.text}")
    print("-" * 50)


def run_live_tests() -> None:
    try:
        # 1. Test GET / (System Introduction)
        resp_root = requests.get(f"{BASE_URL}/", timeout=10)
        print_response("1. GET / (System Description)", resp_root)

        # 2. Test GET /health (Health Check)
        resp_health = requests.get(f"{BASE_URL}/health", timeout=10)
        print_response("2. GET /health (Health Check)", resp_health)

        # 3. Test POST /predict with Positive Sentiment
        positive_payload = {
            "text": "I really enjoyed using this FastAPI service! It works smoothly and accurately."
        }
        resp_positive = requests.post(PREDICT_URL, json=positive_payload, timeout=30)
        print_response("3. POST /predict (Positive Sentiment)", resp_positive)

        # 4. Test POST /predict with Negative Sentiment
        negative_payload = {
            "text": "The product broke on the first day and customer support was terrible."
        }
        resp_negative = requests.post(PREDICT_URL, json=negative_payload, timeout=30)
        print_response("4. POST /predict (Negative Sentiment)", resp_negative)

        # 5. Test POST /predict with Empty Input (Validation Error Check)
        invalid_empty_payload = {"text": "   "}
        resp_empty = requests.post(PREDICT_URL, json=invalid_empty_payload, timeout=10)
        print_response("5. POST /predict (Empty Text Validation Error)", resp_empty)

        # 6. Test POST /predict with Missing 'text' Field (Validation Error Check)
        invalid_missing_payload = {}
        resp_missing = requests.post(PREDICT_URL, json=invalid_missing_payload, timeout=10)
        print_response("6. POST /predict (Missing Field Validation Error)", resp_missing)

    except requests.exceptions.ConnectionError:
        print(
            f"Error: Could not connect to {BASE_URL}.\n"
            "Please make sure all cells in API.ipynb are running first.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    run_live_tests()
