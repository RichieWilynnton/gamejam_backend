import requests
import json

BASE_URL = "http://localhost:5001"
ROOM_ID = "testRoom123"


def testCreateRoom():
    """Test creating a new game room"""
    print("\n" + "=" * 60)
    print("Testing POST /create_room")
    print("=" * 60)

    url = f"{BASE_URL}/create_room"
    payload = {"roomId": ROOM_ID}

    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"Error: {e}")
        return False


def testJoinRoom():
    """Test joining an existing room"""
    print("\n" + "=" * 60)
    print("Testing POST /join_room")
    print("=" * 60)

    url = f"{BASE_URL}/join_room"
    payload = {"roomId": ROOM_ID}

    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def testGetState():
    """Test getting game state"""
    print("\n" + "=" * 60)
    print(f"Testing GET /state/{ROOM_ID}")
    print("=" * 60)

    url = f"{BASE_URL}/state/{ROOM_ID}"

    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def testReadyUpPlayer1():
    """Test player 1 readying up"""
    print("\n" + "=" * 60)
    print(f"Testing POST /ready/{ROOM_ID} (Player 1)")
    print("=" * 60)

    url = f"{BASE_URL}/ready/{ROOM_ID}"
    payload = {"playerNum": 1}

    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def testReadyUpPlayer2():
    """Test player 2 readying up"""
    print("\n" + "=" * 60)
    print(f"Testing POST /ready/{ROOM_ID} (Player 2)")
    print("=" * 60)

    url = f"{BASE_URL}/ready/{ROOM_ID}"
    payload = {"playerNum": 2}

    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        resp_json = response.json()
        print(f"Response: {json.dumps(resp_json, indent=2)}")

        # After both players ready up, the game should start
        if response.status_code == 200:
            print("✅ Both players are ready! Game should now be active.")
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def testHandleAction():
    """Test handling an action"""
    print("\n" + "=" * 60)
    print(f"Testing POST /move/{ROOM_ID}")
    print("=" * 60)

    url = f"{BASE_URL}/action/{ROOM_ID}"

    # Create sample move data matching the expected format
    payload = {
        "board": [
            [
                {"troopType": "empty", "owner": -1, "health": 0, "isRevealed": False}
                for _ in range(8)
            ]
            for _ in range(8)
        ],
        "action": {"actionType": "endTurn"},
        "playerNum": 1,
        "playerInfo": {"money": 100},
    }

    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"Error: {e}")
        return False


def testDeleteRoom():
    """Test deleting the test room"""
    print("\n" + "=" * 60)
    print(f"Testing POST /delete_room/{ROOM_ID}")
    print("=" * 60)

    url = f"{BASE_URL}/delete_room/{ROOM_ID}"

    try:
        response = requests.post(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """Run all API tests"""
    print("\n" + "🚀 Starting API Tests")
    print("Note: Make sure Flask server is running on http://localhost:5001")
    print("Run: python main.py")

    # Test server connection
    try:
        requests.get(BASE_URL, timeout=2)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to Flask server!")
        print("Please start the server first: python main.py")
        return
    except:
        pass  # Server might return 404 for root, which is fine

    results = []

    # Run tests in order
    results.append(("Create Room", testCreateRoom()))
    results.append(("Join Room", testJoinRoom()))
    results.append(("Ready Up Player 1", testReadyUpPlayer1()))
    results.append(("Ready Up Player 2", testReadyUpPlayer2()))
    results.append(("Handle Action", testHandleAction()))
    results.append(("Get State", testGetState()))
    results.append(("Delete Room", testDeleteRoom()))

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")

    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")


if __name__ == "__main__":
    main()
