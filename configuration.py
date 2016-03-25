import os
import json
from collections import namedtuple


def jenkins():
    """Loads Jenkins Credentials

    Place JSON file at ~/.um

    {
      "jenkins": {
        "username": "blah",
        "password": "secret",
        "url": "https://..."
      },
      "github": {
        "token": "01234"
      },
    }
    """
    with open('{}/.um'.format(os.environ.get('HOME')), 'r') as f:
        configuration = json.load(f)
        jenkins = configuration["jenkins"]
        JenkinsCredentials = namedtuple('JenkinsCredentials', 'username password url')
        return JenkinsCredentials(jenkins['username'], jenkins['password'], jenkins['url'])


def github():
    with open('{}/.um'.format(os.environ.get('HOME')), 'r') as f:
        configuration = json.load(f)
        github = configuration["github"]
        GithubCredentials = namedtuple('GithubCredentials', 'name token')
        return GithubCredentials(github["name"], github["token"])
