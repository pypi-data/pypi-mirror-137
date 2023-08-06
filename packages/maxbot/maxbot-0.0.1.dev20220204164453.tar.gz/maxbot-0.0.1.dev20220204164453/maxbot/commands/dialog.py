import typer
import textwrap

from pathlib import Path

from maxbot.commands import bot
from maxbot import studio
from maxbot.cli import add_typer, msg, table

app = typer.Typer()

add_typer(app, name="dialog", help="Dialog operations.")


@app.command()
def list(
    bot_name: str = typer.Option(..., '--bot', '-b', help='Bot name.')
):
    """
        List latest dialogs.
    """
    rows = []
    for c in studio.get_cli_dialogs(bot_name):
        rows.append([c['customer_messenger_id'], c['messenger_type'], c['name']])
    table(
        rows,
        header=["ID","Messenger", "Name"],
        aligns = ("r", "l", "l"),
        divider=True,
    )


@app.command()
def messages(
    dialog_id: int = typer.Argument(..., help='Customer ID.')
):
    """
        Show messages in a dialog.

        Use "maxctl dialog list --bot <bot_name>" to get DIALOG_ID for this command.
    """
    turns = studio.get_history_turns(dialog_id)
    for t in turns:
        msg.text(f"🧑 {t['event']['text']}")
        for d in t['detections']:
            for j in d.get('journals', []):
                for e in j.get('events', []):
                    msg.text(f"🤖 {e['text']}")
            if 'broken_flow' in d:
                b = d['broken_flow']
                msg.text(f"❌ Broken flow by {b['reason']}")
                msg.text(textwrap.indent(b['message'], '\t'))
                msg.text(textwrap.indent(b['xml_document'], '\t'))
