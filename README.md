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
git clone <repository-url>
cd <repository-name>
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your credentials:

```plaintext
USERNAME=your_username
PASSWORD=your_password
SECRET_KEY=your_2fa_secret_key
```

## Usage

Simply run the script:

```bash
python main.py
```

This README provides:

- A clear description of what the project does
- Installation instructions
- Usage guide
- Security considerations
- Requirements information
- A placeholder for license information

Feel free to customize it further based on your specific needs!

The script will:

1. Read your credentials from the `.env` file
2. Generate a current 2FA code
3. Log in to AWS using cloudopscli
4. Automatically open the AWS Console URL in your default browser

## Security Notes

- Never commit your `.env` file to version control
- Keep your 2FA secret key secure
- Regularly rotate your credentials

## Requirements

See `requirements.txt` for Python package dependencies.

## License

[Choose an appropriate license]
