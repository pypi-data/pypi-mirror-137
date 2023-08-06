import typer

from maxbot import studio
from maxbot.cli import command, msg, write_login, STATE


@command()
def login(
    api_url : str = typer.Option('https://api-studio.midvix.ai'),
    phone_number : str = typer.Option(..., prompt=True),
    password : str = typer.Option(..., prompt=True, hide_input=True),
):
    """
        Login Studio API.
    """
    msg.info(f'Login {api_url}')
    studio_key = studio.post_cli_login(api_url, phone_number, password)
    write_login(api_url, phone_number, studio_key)
    msg.good('Login success')
