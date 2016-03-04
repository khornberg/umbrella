import os
import um as um
from click.testing import CliRunner


def test_github_pair_add_noop():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('authorized_keys', 'w') as f:
            f.write('')
        result = runner.invoke(um.cli, ['github', 'pair', 'add', '--keys', 'authorized_keys'])

        assert result.exit_code == 0
        assert not result.exception
        assert result.output == ''


def test_github_pair_add_user():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('authorized_keys', 'w') as f:
            f.write('')

        result = runner.invoke(um.cli, ['github', 'pair', 'add', '--keys', 'authorized_keys', 'khornberg'])
        with open('authorized_keys', 'r') as f:
            x = f.read()
            assert x == 'no-agent-forwarding,no-port-forwarding,no-X11-forwarding,command="tmux attach -t pair-session" ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDCZeMs4AnuGfPlYDS6ufGOPNjBRGMzja3bTvFsxY9t3AIFd7YBZ5vmpVIG/1WAKQKP/crDFb/C4IALkG2dbtqk5IkXuPcVQoYcodfa2jqpcjn+HFaQ2ZPcksiuDtT4axcth7LlNbt6bmrt1MZraUmZnmziBWdHoMPbf5XusIO6vm3OPoHSut4JJwL5sIS2vAA24HO4JTUT4fnpVseJsFod4JfS2dVjV/U3PLjdFGbSQAWxBrlvI4d2sCghI5J2P1xWIEt8ViJb6eK0Z8nCx79YrHOqJrMEBHZLk2HciN4QGH9Eh1dfzlRT0yXtrnoQPUE8nqL5JGRpTqiHvkXlrcKz #khornberg\n'

        assert result.exit_code == 0
        assert not result.exception
        assert result.output == 'Added khornberg to your authorized_keys\n'


def test_github_pair_remove_user():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('authorized_keys', 'w') as f:
            f.write('no-agent-forwarding,no-port-forwarding,no-X11-forwarding,command="tmux attach -t pair-session" ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDCZeMs4AnuGfPlYDS6ufGOPNjBRGMzja3bTvFsxY9t3AIFd7YBZ5vmpVIG/1WAKQKP/crDFb/C4IALkG2dbtqk5IkXuPcVQoYcodfa2jqpcjn+HFaQ2ZPcksiuDtT4axcth7LlNbt6bmrt1MZraUmZnmziBWdHoMPbf5XusIO6vm3OPoHSut4JJwL5sIS2vAA24HO4JTUT4fnpVseJsFod4JfS2dVjV/U3PLjdFGbSQAWxBrlvI4d2sCghI5J2P1xWIEt8ViJb6eK0Z8nCx79YrHOqJrMEBHZLk2HciN4QGH9Eh1dfzlRT0yXtrnoQPUE8nqL5JGRpTqiHvkXlrcKz #khornberg\n')

        result = runner.invoke(um.cli, ['github', 'pair', 'remove', '--keys', 'authorized_keys', 'khornberg'])
        with open('authorized_keys', 'r') as f:
            x = f.read()
            assert x == ''

        assert result.exit_code == 0
        assert not result.exception
        assert result.output == 'Removed khornberg from your authorized_keys\n'


def test_local_envvar_from_a_preset_list():
    runner = CliRunner()
    result = runner.invoke(um.cli, ['local', 'env', 'test'])
    assert os.environ.get('TEST') == 'https://um.so'
    assert result.output == 'Set TEST to https://um.so in your environment\n'


def test_local_envvar_from_a_provided_value():
    runner = CliRunner()
    result = runner.invoke(um.cli, ['local', 'env', 'test', '--value', 'https://khornberg.github.com'])
    assert os.environ.get('TEST') == 'https://khornberg.github.com'
    assert result.output == 'Set TEST to https://khornberg.github.com in your environment\n'
