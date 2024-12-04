import pyotp
import os
from dotenv import load_dotenv
import pexpect
import logging
import re
import sys
import io


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    load_dotenv()

    secret_key = os.getenv("SECRET_KEY")
    if secret_key is None:
        logger.error("SECRET_KEY environment variable is not set!")
        exit(1)

    totp = pyotp.TOTP(secret_key)
    otp = totp.now()
    logger.info(f"Generated OTP: {otp}")

    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    if username is None or password is None:
        logger.error("USERNAME or PASSWORD environment variables are not set!")
        exit(1)

    username = username.strip()
    password = password.strip()
    otp = otp.strip()

    try:
        child = pexpect.spawn("cloudopscli login", timeout=30)

        child.logfile = io.BytesIO()
        child.interact()
        
        child.expect(re.compile(r"Enter\s+your\s+Company\s+Username", re.IGNORECASE))
        child.sendline(username)

        child.expect(re.compile(r"Enter\s+the\s+Password\s+of", re.IGNORECASE))
        child.sendline(password)

        child.expect(re.compile(r"Enter\s+your\s+6\s+digit\s+OTP", re.IGNORECASE))
        child.sendline(otp)
    

        output = child.before

        if isinstance(output, bytes):
            output = output.decode('utf-8')

        logger.info(f"STDOUT: {output}")

    except pexpect.TIMEOUT:
        logger.error("cloudopscli login process timed out. Consider reviewing the prompts and increasing the timeout duration.")
        exit(1)
    except pexpect.EOF:
        logger.error("Unexpected end of input from cloudopscli.")
        exit(1)
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()