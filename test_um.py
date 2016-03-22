import os
import um as um
from click.testing import CliRunner


class TestGithub():

    def test_github_pair_add_noop(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('authorized_keys', 'w') as f:
                f.write('')
            result = runner.invoke(um.cli, ['github', 'pair', 'add', '--keys', 'authorized_keys'])

            assert result.exit_code == 0
            assert not result.exception
            assert result.output == ''

    def test_github_pair_add_user(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('authorized_keys', 'w') as f:
                f.write('')

            result = runner.invoke(um.cli, ['github', 'pair', 'add', '--keys', 'authorized_keys', 'khornberg'])
            with open('authorized_keys', 'r') as f:
                x = f.read()
                assert x == 'no-agent-forwarding,no-port-forwarding,no-X11-forwarding,command="tmux new-session -t host-session -s pair-session" ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDCZeMs4AnuGfPlYDS6ufGOPNjBRGMzja3bTvFsxY9t3AIFd7YBZ5vmpVIG/1WAKQKP/crDFb/C4IALkG2dbtqk5IkXuPcVQoYcodfa2jqpcjn+HFaQ2ZPcksiuDtT4axcth7LlNbt6bmrt1MZraUmZnmziBWdHoMPbf5XusIO6vm3OPoHSut4JJwL5sIS2vAA24HO4JTUT4fnpVseJsFod4JfS2dVjV/U3PLjdFGbSQAWxBrlvI4d2sCghI5J2P1xWIEt8ViJb6eK0Z8nCx79YrHOqJrMEBHZLk2HciN4QGH9Eh1dfzlRT0yXtrnoQPUE8nqL5JGRpTqiHvkXlrcKz #khornberg\n'

            assert result.exit_code == 0
            assert not result.exception
            assert result.output == 'Added khornberg to your authorized_keys\n'

    def test_github_pair_add_users(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('authorized_keys', 'w') as f:
                f.write('')

            result = runner.invoke(um.cli, ['github', 'pair', 'add', '--keys', 'authorized_keys', 'octocat', 'khornberg'])
            with open('authorized_keys', 'r') as f:
                x = f.read()
                assert x == 'no-agent-forwarding,no-port-forwarding,no-X11-forwarding,command="tmux new-session -t host-session -s pair-session" ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEApEhQ0WV/iZjAG6vgvOWlnluecdJL87p9ulO/PZSL2NethE1U1fbUlIYg59T+YOqk6F+msSkHTrFWuZ+DI5XbgCeYmdbupa5zmj+p4HBHd9NkwRMB0pfrRopj1zfVWur01DEemMqw/a06wdN/deB3SSbNQRrKQGtI73u4PFwRuBY54XXpAcgUxq8WVsheSBUK+dIvEdo0XGNcl3a01TAcnE2/4AwiawZIh15iy/6rux+2eNH6jaRT9VYCAlTlOa0Qb2vANLe9gCbs89TYgI+TS/SZqo/JvqcuIbz0JHkL9zcIWzKTCdlg/jD1N8uvC9+bhjUhfhVgpNdfTIfzzN2XJw== #octocat\nno-agent-forwarding,no-port-forwarding,no-X11-forwarding,command="tmux new-session -t host-session -s pair-session" ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDCZeMs4AnuGfPlYDS6ufGOPNjBRGMzja3bTvFsxY9t3AIFd7YBZ5vmpVIG/1WAKQKP/crDFb/C4IALkG2dbtqk5IkXuPcVQoYcodfa2jqpcjn+HFaQ2ZPcksiuDtT4axcth7LlNbt6bmrt1MZraUmZnmziBWdHoMPbf5XusIO6vm3OPoHSut4JJwL5sIS2vAA24HO4JTUT4fnpVseJsFod4JfS2dVjV/U3PLjdFGbSQAWxBrlvI4d2sCghI5J2P1xWIEt8ViJb6eK0Z8nCx79YrHOqJrMEBHZLk2HciN4QGH9Eh1dfzlRT0yXtrnoQPUE8nqL5JGRpTqiHvkXlrcKz #khornberg\n'

            assert result.exit_code == 0
            assert not result.exception
            assert result.output == 'Added octocat to your authorized_keys\nAdded khornberg to your authorized_keys\n'

    def test_github_pair_add_user_replace(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('authorized_keys', 'w') as f:
                f.write('')

            result = runner.invoke(um.cli, ['github', 'pair', 'add', '--keys', 'authorized_keys', '--replace', 'khornberg'])
            with open('authorized_keys', 'r') as f:
                x = f.read()
                assert x == 'no-agent-forwarding,no-port-forwarding,no-X11-forwarding,command="tmux new-session -t host-session -s pair-session" ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDCZeMs4AnuGfPlYDS6ufGOPNjBRGMzja3bTvFsxY9t3AIFd7YBZ5vmpVIG/1WAKQKP/crDFb/C4IALkG2dbtqk5IkXuPcVQoYcodfa2jqpcjn+HFaQ2ZPcksiuDtT4axcth7LlNbt6bmrt1MZraUmZnmziBWdHoMPbf5XusIO6vm3OPoHSut4JJwL5sIS2vAA24HO4JTUT4fnpVseJsFod4JfS2dVjV/U3PLjdFGbSQAWxBrlvI4d2sCghI5J2P1xWIEt8ViJb6eK0Z8nCx79YrHOqJrMEBHZLk2HciN4QGH9Eh1dfzlRT0yXtrnoQPUE8nqL5JGRpTqiHvkXlrcKz #khornberg\n'

            assert result.exit_code == 0
            assert not result.exception
            assert result.output == 'Removed khornberg from your authorized_keys\nAdded khornberg to your authorized_keys\n'

    # test default users
    # test no default users
    # test no replace

    def test_github_pair_remove_user(self):
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


class TestLocal():

    def test_local_envvar_from_a_preset_list(self):
        runner = CliRunner()
        result = runner.invoke(um.cli, ['local', 'env', 'Applications.Website.Environments.Production.DomainName'])
        assert result.output == 'export DOMAINNAME=www.imtapps.com\n'

    def test_local_envvar_from_a_provided_value(self):
        runner = CliRunner()
        result = runner.invoke(um.cli, ['local', 'env', 'test', '--value', 'https://khornberg.github.com'])
        assert result.output == 'export TEST=https://khornberg.github.com\n'
