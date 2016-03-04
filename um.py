# coding: utf-8
import os
import re
import click
from github import Github
from executor import execute


SSH_LIMITATIONS = 'no-agent-forwarding,no-port-forwarding,no-X11-forwarding'
SSH_COMMAND = 'command="tmux attach -t pair-session"'


@click.group()
def cli():
    """Utility application that covers many things; thus umbrella; and um seemed um, short"""
    pass


@cli.command()
def colors():
    """Demonstrates ANSI color support."""
    for color in 'red', 'green', 'blue', 'white', 'black', 'yellow':
        click.echo(click.style('{} am colored {}'.format('you', color), fg=color))
        click.echo(click.style('{} am background colored {}'.format('kyle', color), bg=color))


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
@click.option('--keys', required=True, type=click.Path(exists=True), help='Path and file name of your authorized_keys')
@click.argument('usernames', nargs=-1)
def add(replace, keys, usernames):
    """Add a github user to your authorized_keys"""
    if replace:
        remove(usernames)

    for username in usernames:
        github_keys = get_keys(username)
        with open(keys, 'r+') as f:
            for key in github_keys:
                new_key = '{},{} {} #{}\n'.format(SSH_LIMITATIONS, SSH_COMMAND, key.key, username)
                f.write(new_key)
        f.closed
        click.echo('Added {} to your authorized_keys'.format(username))


@pair.command()
@click.option('--keys', required=True, type=click.Path(exists=True), help='Path and file name of your authorized_keys')
@click.argument('usernames', nargs=-1)
def remove(keys, usernames):
    """Remove a github user from your authorized_keys"""
    for username in usernames:
        with open(keys, 'r+') as f:
            key_file = f.read()
            pattern = '.* #{}\n'.format(username)
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
    lookup_set = {'test': 'https://um.so'}
    if not value:
        value = lookup_set[key]

    os.environ[key.upper()] = value
    click.echo('Set {} to {} in your environment'.format(key.upper(), value))
