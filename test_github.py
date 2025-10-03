import requests
import os

def test_github_token():
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("No GitHub token found")
        return False
        
    try:
        response = requests.get('https://api.github.com/user', 
                              headers={'Authorization': f'token {token}'})
        print(f'Status: {response.status_code}')
        if response.status_code == 200:
            user_data = response.json()
            print(f'✅ GitHub token valid - User: {user_data.get("login")}')
            return True
        else:
            print(f'❌ GitHub token error: {response.text}')
            return False
    except Exception as e:
        print(f'❌ GitHub test error: {e}')
        return False

if __name__ == "__main__":
    test_github_token()