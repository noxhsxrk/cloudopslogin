import pyotp
import os
from dotenv import load_dotenv
import pexpect
import logging
import re
import sys

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    load_dotenv()

    secret_key = os.getenv("SECRET_KEY")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    if not all([secret_key, username, password]):
        logger.error("Required environment variables are not set. Please set SECRET_KEY, USERNAME, and PASSWORD.")
        sys.exit(1)

    try:
        child = pexpect.spawn("cloudopscli login", timeout=30)
        
        child.logfile_read = None

        index = child.expect([
            re.compile(rb"Enter\s+your\s+Company\s+Username", re.IGNORECASE),
            re.compile(rb"Token\s+is\s+still\s+valid", re.IGNORECASE)
        ])

        if index == 0:
            logger.info("Performing full login...")
            child.sendline(username.strip())

            child.expect(re.compile(rb"Enter\s+the\s+Password\s+of", re.IGNORECASE))
            child.sendline(password.strip())

            totp = pyotp.TOTP(secret_key.strip())
            otp = totp.now()
            child.expect(re.compile(rb"Enter\s+your\s+6\s+digit\s+OTP", re.IGNORECASE))
            child.sendline(otp.strip())

            logger.info("Login details submitted.")

        elif index == 1:
            logger.info("Token is still valid. Proceeding directly to interactive session.")

        logger.info("Handing over control to cloudopscli. (To exit, press Ctrl+])")
        child.interact()

        child.close()

    except pexpect.exceptions.TIMEOUT:
        logger.error("The login process timed out. `cloudopscli` did not respond in time.")
        sys.exit(1)

    except pexpect.exceptions.EOF:
        logger.error("Unexpected exit from `cloudopscli`. The process may have crashed or finished unexpectedly.")
        logger.info("Output before exit:\n%s", child.before.decode('utf-8', errors='ignore') if child.before else '')
        sys.exit(1)

    except Exception as e:
        logger.exception("An unexpected error occurred: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()