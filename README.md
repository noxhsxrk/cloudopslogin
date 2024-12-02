# AWS Console Login Automation

This script automates the AWS Console login process using cloudopscli, handling 2FA authentication automatically.

## Prerequisites

- Python 3.x
- cloudopscli installed and configured
- AWS account credentials
- 2FA secret key

## Installation

1. Clone this repository:

```bash
git clone https://github.com/noxhsxrk/cloudopslogin.git
cd cloudopslogin
```

2. Install the package and its dependencies:

```bash
pip install -e .
```

3. Create a `.env` file in your home directory or project directory with your credentials:

```plaintext
USERNAME=your_username
PASSWORD=your_password
SECRET_KEY=your_2fa_secret_key
```

## Usage

After installation, you can run the script from anywhere using:

```bash
copslogin
```

The script will:

1. Read your credentials from the `.env` file
2. Generate a current 2FA code
3. Log in to AWS using cloudopscli
4. Automatically open the AWS Console URL in your default browser

## Requirements

The following Python packages are required and will be automatically installed:

- pyotp
- python-dotenv
