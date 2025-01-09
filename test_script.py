import requests

# API 기본 URL
BASE_URL = "http://localhost:8000"

def test_signup_and_login():
    # 1. 회원가입 테스트
    signup_data = {
        "username": "testuser",
        "password": "testpass"
    }
    
    print("\n1. 회원가입 테스트")
    response = requests.post(f"{BASE_URL}/users/", params=signup_data)
    print("회원가입 응답:", response.json())
    
    # 2. 로그인 테스트
    print("\n2. 로그인 테스트")
    login_data = {
        "username": "testuser",
        "password": "testpass",
        "grant_type": "password"  # OAuth2 요구사항
    }
    response = requests.post(f"{BASE_URL}/token", data=login_data)
    print("로그인 응답:", response.json())
    
    # 토큰 저장
    token = response.json()["access_token"]
    
    # 3. 보호된 경로 테스트
    print("\n3. 보호된 경로 테스트")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/protected", headers=headers)
    print("보호된 경로 응답:", response.json())

def test_error_cases():
    print("\n4. 에러 케이스 테스트")
    
    # 잘못된 로그인
    print("\n4.1 잘못된 비밀번호로 로그인")
    login_data = {
        "username": "testuser",
        "password": "wrongpass",
        "grant_type": "password"
    }
    response = requests.post(f"{BASE_URL}/token", data=login_data)
    print("응답 상태:", response.status_code)
    print("응답 내용:", response.json())
    
    # 잘못된 토큰으로 접근
    print("\n4.2 잘못된 토큰으로 보호된 경로 접근")
    headers = {"Authorization": "Bearer wrongtoken"}
    response = requests.get(f"{BASE_URL}/protected", headers=headers)
    print("응답 상태:", response.status_code)
    print("응답 내용:", response.json())

if __name__ == "__main__":
    try:
        # 정상 케이스 테스트
        test_signup_and_login()
        
        # 에러 케이스 테스트
        test_error_cases()
        
    except requests.exceptions.RequestException as e:
        print(f"\n에러 발생: {e}")
    except Exception as e:
        print(f"\n예상치 못한 에러: {e}")