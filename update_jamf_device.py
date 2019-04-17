#!/usr/bin/env python3
# Jason Satti
import argparse

import requests

import api_creds


class JamfConnect(object):
    """Connect to Jamf Instance and update a user's device information."""

    def __init__(self, resource_url, api_user, api_pw):
        self.resource_url = resource_url
        self.api_user = api_user
        self.api_pw = api_pw

    def update_jamf_device(self, last_name, status):
        """Update device information on Jamf.

        :param status: Status of device to append end of name
        :param last_name: last name of target user
        """
        headers = {'Accept': "application/json",
                   'Content-Type': "application/xml"}
        r = requests.get(F'{self.resource_url}match/%2A{last_name}',
                         auth=(self.api_user, self.api_pw),
                         headers=headers)
        r.raise_for_status()
        devices = r.json()['computers']
        if devices:
            for device in devices:
                device_id = device.get('id')
                device_name = device.get('name')
                # <id>5</id> is the ID of extension attribute
                payload = F"""<computer>
                    <general>
                        <name>{device_name}-{status}</name>
                    </general>
                    <extension_attributes>
                        <extension_attribute>
                            <id>5</id>
                            <value>Yes</value>
                        </extension_attribute>
                    </extension_attributes>
                </computer>"""
                r = requests.put(F'{self.resource_url}id/{str(device_id)}',
                                 auth=(self.api_user, self.api_pw),
                                 headers=headers,
                                 data=payload)
                r.raise_for_status()


def main():
    """Update a user's device information in Jamf.

    :last_name: Required CLI Input
    :status: Required CLI Input
    """
    parser = argparse.ArgumentParser(description='Update user device '
                                                 'information on Jamf')
    parser.add_argument('-l', '--last_name', required=True, type=str,
                        help='Last name of user for device to update')
    parser.add_argument('-s', '--status', required=True, type=str,
                        help='Device status to append name with.')
    args = parser.parse_args()

    jss_connect = JamfConnect(api_creds.resource_url, api_creds.api_user,
                              api_creds.api_pw)
    jss_connect.update_jamf_device(args.last_name, args.status)


if __name__ == '__main__':
    main()
