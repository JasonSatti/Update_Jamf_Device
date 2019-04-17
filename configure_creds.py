#!/usr/bin/env python3
# Jason Satti
import os


def create_and_configure():
    """Create a api_creds file and capture the API information."""
    user = input('Your API Username: ')
    password = input('Your API Password: ')
    name = input('Your JAMF Instance Name: ')
    api_creds_template = F"""api_user='{user}'\npassword ='{password}'\n\
url='https://{name}.jamfcloud.com/JSSResource/computers/'\n"""

    with os.fdopen(os.open('api_creds.py', os.O_WRONLY | os.O_CREAT, 0o600),
                   'w') as F:
        F.write(api_creds_template)
    F.close()


def main():
    if not os.path.exists('./api_creds.py'):
        create_and_configure()


if __name__ == '__main__':
    main()
