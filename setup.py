from setuptools import setup, find_packages

setup(
    name="cloudopslogin",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "pyotp",
        "python-dotenv",
        "pexpect",
    ],
    entry_points={
        'console_scripts': [
            'copslogin=cloudopslogin.main:main',
        ],
    },
)
