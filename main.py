import subprocess
import pyotp
import os
import re
import webbrowser
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
if secret_key is None:
    print("ERROR: SECRET_KEY environment variable is not set!")
    exit(1)

totp = pyotp.TOTP(secret_key)
otp = totp.now()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
if username is None or password is None:
    print("ERROR: USERNAME or PASSWORD environment variables are not set!")
    exit(1)

inputs = f"{username}\n{password}\n{otp}\n"

process = subprocess.Popen(
    ["cloudopscli", "login"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

stdout, stderr = process.communicate(input=inputs)

print("STDOUT:", stdout)
if stderr:
    print("STDERR:", stderr)

url_match = re.search(r"(https://signin\.aws\.amazon\.com/[^ ]+)", stdout)
if url_match:
    aws_console_url = url_match.group(1)
    print(f"Opening the URL: {aws_console_url}")
    webbrowser.open(aws_console_url)
else:
    print("AWS Console URL not found in the output.")
