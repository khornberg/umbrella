import os
import json
from collections import namedtuple


def jenkins():
    """Loads Jenkins Credentials

    Place JSON file at ~/.jenkins

    {"username": "blah", "password": "secret", "url", "https://..."}
    """
    with open('{}/.jenkins'.format(os.environ.get('HOME')), 'r') as f:
        creds = json.load(f)
        JenkinsCredentials = namedtuple('JenkinsCredentials', 'username password url')
        return JenkinsCredentials(creds['username'], creds['password'], creds['url'])
