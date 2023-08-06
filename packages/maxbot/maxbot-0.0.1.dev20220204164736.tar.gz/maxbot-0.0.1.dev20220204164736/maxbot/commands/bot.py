import typer
import yaml
from pathlib import Path

from maxbot import studio
from maxbot.cli import add_typer, msg, table

app = typer.Typer()

add_typer(app, name="bot", help="Bot operations.")


@app.command()
def create(
    f: typer.FileText = typer.Option(..., '--filename', '-f',
                                  help='Filename to use to create the bot.',
                                  exists=True, dir_okay=False, readable=True)
):
    studio.post_cli_bots(yaml.safe_load(f))
    msg.good(f"Created bot from file: {f.name}")


@app.command()
def update(
    f: typer.FileText = typer.Option(..., '--filename', '-f',
                                  help='Filename to use to update the bot.',
                                  exists=True, dir_okay=False, readable=True)
):
    data = yaml.safe_load(f)
    studio.put_cli_bots(data['name'], data)
    msg.good(f"Updated bot from file: {f.name}")


@app.command()
def delete(
    name: str = typer.Argument(..., help='Bot name to delete.'),
    yes: bool = typer.Option(..., prompt='Are you sure?')
):
    if not yes:
        return
    studio.delete_cli_bots(name)
    msg.good(f"Deleted bot: {name}")


@app.command()
def list():
    rows = []
    for bot in studio.get_cli_bots():
        m = bot.get('messengers', {})
        row = [
            bot['name'],
            m.get('telegram', {}).get('customers_count', '-'),
            m.get('vkontakte', {}).get('customers_count', '-'),
            m.get('viber', {}).get('customers_count', '-'),
            m.get('facebook', {}).get('customers_count', '-'),
            m.get('instagram', {}).get('customers_count', '-'),
        ]
        rows.append(row)

    table(
        rows,
        header=['Name', 'tg', 'vk', 'vb', 'fb', 'ig'],
        aligns = ('l', 'r', 'r', 'r', 'r', 'r'),
        divider=True,
    )
