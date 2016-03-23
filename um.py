# coding: utf-8
import sys
import os
import re
import json
import click
import requests
from github import Github
from executor import execute
from jenkinsapi.jenkins import Jenkins
import configuration

BUILD_AUTOMATION = '{}/projects/build_automation'.format(os.environ.get('HOME'))
AWS_MANAGER = '{}/projects/aws_manager'.format(os.environ.get('HOME'))
sys.path.append(BUILD_AUTOMATION)
sys.path.append(AWS_MANAGER)
from config import users, projects

JENKINS = configuration.jenkins()

AWS_DEFINITIONS = None
with open('{}/aws_manager/definitions.json'.format(AWS_MANAGER), 'r') as f:
    AWS_DEFINITIONS = json.load(f)

SSH_LIMITATIONS = 'no-agent-forwarding,no-port-forwarding,no-X11-forwarding'
SSH_COMMAND = 'command="tmux new-session -t host-session -s pair-session"'
AUTHORIZED_KEYS = '{}/.ssh/authorized_keys'.format(os.environ.get('HOME'))


@click.group()
def cli():
    """Utility application that covers many things; thus umbrella; and um seemed um, short"""
    pass


@cli.group()
def github():
    """Commands that interact with GitHub"""
    pass


@github.group()
def pair():
    """Control authorized_keys for pairing"""
    pass


@pair.command()
@click.option('--replace/--no-replace', default=False, help='Replace user(s) key')
@click.option('--keys', required=True, type=click.Path(exists=True), default=AUTHORIZED_KEYS, help='Path and file name of your authorized_keys')
@click.option('--default-users/--no-default-users', help='Authorize all users in build_automation.users')
@click.argument('usernames', nargs=-1)
@click.pass_context
def add(ctx, replace, keys, default_users, usernames):
    """Add a github user to your authorized_keys"""
    if replace:
        ctx.invoke(remove, usernames=usernames)

    if default_users:
        usernames = users.USERS

    with open(keys, 'a') as f:
        for username in usernames:
            github_keys = get_keys(username)
            for key in github_keys:
                new_key = '{},{} {} #{}\n'.format(SSH_LIMITATIONS, SSH_COMMAND, key.key, username)
                f.write(new_key)
                # print(f.read())
            click.echo('Added {} to your authorized_keys'.format(username))
        f.closed


@pair.command()
@click.option('--keys', required=True, type=click.Path(exists=True), default=AUTHORIZED_KEYS, help='Path and file name of your authorized_keys')
@click.argument('usernames', nargs=-1)
def remove(keys, usernames):
    """Remove a github user from your authorized_keys"""
    for username in usernames:
        with open(keys, 'r+') as f:
            key_file = f.read()
            pattern = '^.* #{}\n'.format(username)
            match = re.sub(pattern, '', key_file, re.I)
            f.seek(0)
            f.write(match)
            f.truncate()
        f.closed
        click.echo('Removed {} from your authorized_keys'.format(username))


def get_keys(username):
    try:
        keys = Github().get_user(username).get_keys()
        return keys
    except Exception as e:
        click.echo('There was an error getting {}\'s key'.format(username))
        click.echo(e)
        raise e


@cli.group()
def local():
    """Local commands"""


@local.command()
def pair_setup():
    """ Sets up OS X for pairing

    1) Disables passwords and enables public-key authentication only

    2) Adds Pair and pair user aliases for the current user
    """
    sshd_config = execute("sed -E -i.bak {} {}".format(r"'s/^#?(PasswordAuthentication|ChallengeResponseAuthentication).*$/\1 no/'", "/etc/sshd_config"), capture=True, sudo=True)
    if sshd_config:
        click.echo('Disabled clear text passwords in sshd')

    user = os.getenv('USER')
    pair_alias = execute("dscl . -append /Users/{} RecordName Pair pair".format(user), capture=True, sudo=True)
    if pair_alias:
        click.echo('Added pair alias for current user')


@local.command()
@click.option('--adapter', default="Wi-Fi", help="Adapter name")
@click.argument('networks', nargs=-1)
def dns(adapter, networks):
    """Set dns entries for an adapter"""

    if networks:
        networks = " ".join(networks)

    dns_output = execute('networksetup -setdnsservers {} {}'.format(adapter, networks), capture=True, sudo=True)
    if dns_output:
        click.echo('Added dns servers {} to {}'.format(networks, adapter))


@local.command()
@click.argument('key', nargs=1)
@click.option('--value', help="Value of environmental variable")
def env(key, value):
    """Sets environmental variables"""
    lookup_set = get_lookup_set(key)
    keys = key.split('.')
    if not value:
        values = lookup_set
        for key in keys:
            values = values[key]
        value = values

    last_key = keys.pop()
    click.echo('export {}={}'.format(last_key.upper(), value))


# @local.command()
# @click.option('--hosts', default="/etc/hosts", help="Hosts file")
# @click.argument('key', nargs=1)
# @click.argument('value', nargs=1)
# def add(hosts, key, value):


@cli.group()
def jenkins():
    """Commands that interact with Jenkins"""
    pass


@jenkins.command()
@click.option('--watch-build/--no-watch-build', help='Watch the build')
@click.option('--number', help='Build number to rebuild')
@click.argument('project', nargs=1)
@click.pass_context
def rebuild(ctx, watch_build, number, project):
    """Rebuild the last build"""
    J = connect_to_jenkins()
    build = J['{}'.format(project)].get_last_build()
    lastBuildNumber = number if number else build.get_number()
    if not build.is_good():
        retry = "{}/job/{}/{}/retry".format(JENKINS.url, project, lastBuildNumber)
        response = requests.get(retry, auth=requests.auth.HTTPBasicAuth(JENKINS.username, JENKINS.password))
        if response.status_code == requests.codes.ok:
            click.echo('{} build restarted'.format(project))
    else:
        click.echo('Build {} was successful'.format(lastBuildNumber))

    if watch_build:
        ctx.invoke(watch, project=project)


@jenkins.command()
@click.argument('project', nargs=1)
@click.option('--number', help='Build number to rebuild')
def watch(project, number):
    """Watch console output from a build"""
    J = connect_to_jenkins()
    job = J['{}'.format(project)]
    build_number = int(number) if number else job.get_last_buildnumber()
    build = job.get_build(build_number)
    lastLength = 0
    while build.is_running():
        output = build.get_console()
        outputLength = len(output)
        click.echo(output[lastLength:], nl=False)
        lastLength = outputLength
    if not build.is_running():
        click.echo(build.get_console()[lastLength:], nl=False)
        click.echo('End of output for build {}'.format(build_number))


# Utility functions
def get_lookup_set(value):
    # replace with call to something to get set
    return AWS_DEFINITIONS


def connect_to_jenkins():
    return Jenkins(JENKINS.url, username=JENKINS.username, password=JENKINS.password)
