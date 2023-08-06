import typer

from pathlib import Path

from maxbot.cli import add_typer, msg, table

app = typer.Typer()
add_typer(app, name="project", help="Template operations.")


def _validate_project_dir(project_dir):
    if project_dir.exists():
        msg.fail(f'Directory "{project_dir}" already exists', exits=1)
    return project_dir


@app.command()
def new(
    project_dir : Path = typer.Argument(...,
                                        help='Project directoy. Must not exists',
                                        callback=_validate_project_dir),
    bot_name : str = typer.Option(..., '--bot', '-b', prompt=True),
    telegram_token : str = typer.Option(..., prompt=True),
):
    """
        Create new project from template.
    """
    project_dir.mkdir()

    t = HELLO_WORLD.format(bot_name=bot_name, telegram_token=telegram_token)
    bot_file = project_dir / 'Bot.yaml'
    bot_file.write_text(t)
    msg.info(f'Generate file {bot_file}')
    msg.good('Project succseed')


HELLO_WORLD = """
version: 0.0.1
type: Bot
name: "{bot_name}"
messengers:
    telegram:
        token: "{telegram_token}"
definitions:
    intents:
      - name: greetings
        source: customer-nlu
        examples:
          - text: Здравствуйте
          - text: Привет
          - text: Салют
          - text: Добрый день
          - text: Рад видеть!
      - name: ending
        source: customer-nlu
        examples:
          - text: До свидания
          - text: Пока
          - text: До встречи
          - text: Прощай
          - text: Увидемся!
    dialog:
      - condition: intents.greetings
        response: |
            <text>Приветствую тебя!</text>
      - condition: intents.ending
        response: |
            <text>До скорой встречи</text>
""".strip()
