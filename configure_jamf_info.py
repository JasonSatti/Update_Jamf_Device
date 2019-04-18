#!/usr/bin/env python3
# Jason Satti
import os


def create_and_configure():
    """Create a jamf_info file and capture the API information."""
    user = input('Your API Username: ')
    password = input('Your API Password: ')
    name = input('Your JAMF Instance Name: ')
    jamf_info_template = F"""api_user='{user}'\napi_pw ='{password}'\n\
resource_url='https://{name}.jamfcloud.com/JSSResource/computers/'\n"""

    with os.fdopen(os.open('jamf_info.py', os.O_WRONLY | os.O_CREAT, 0o600),
                   'w') as F:
        F.write(jamf_info_template)
    F.close()


def main():
    if not os.path.exists('./jamf_info.py'):
        create_and_configure()


if __name__ == '__main__':
    main()
