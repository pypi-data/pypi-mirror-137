import typer
import yaml
import wasabi

from pathlib import Path


app = typer.Typer()
# Just export useful methods
add_typer = app.add_typer
command = app.command

msg = wasabi.Printer()
table = msg.table

STATE = {
    'verbose': False,
    'config_dir': Path.home() / '.maxbot',
}

@app.callback()
def main(verbose: bool = False):
    """
        Lightweight access for Studio API
    """
    if verbose:
        msg.info("Will write verbose output")
        STATE['verbose'] = verbose


def write_login(api_url, phone_number, api_key):
    config = [{
        'phone_number': phone_number,
        'api_url': api_url,
        'api_key': api_key,
        'name': 'default'
    }]

    STATE['config_dir'].mkdir(exist_ok=True)
    config_file = STATE['config_dir'] / 'config.yaml'
    msg.text(f'Write {config_file}', show=STATE['verbose'])
    with config_file.open('w') as f:
        yaml.dump(config, f)


def read_api_config_or_fail():
    config_file = STATE['config_dir'] / 'config.yaml'
    if not config_file.exists():
        msg.fail('Not authorized. Please use "maxctl login".', exits=1)
    msg.text(f'Read {config_file}', show=STATE['verbose'])
    with config_file.open() as f:
        c = yaml.safe_load(f)
    for line in c:
        return line
    msg.fail('Not authorized. Please use "maxctl login".', exits=1)
