import requests
import typer
import textwrap

from wasabi import msg, table

from maxbot.cli import read_api_config_or_fail, STATE


def _fail_for_status(resp):
    if STATE['verbose']:
        req = resp.request
        msg.divider()
        msg.text(f'{req.method} {req.url}')
        if req.body:
            msg.text(req.body.decode())
        msg.text(f'HTTP {resp.status_code} {resp.reason}')
        msg.text(resp.text)
    if not resp.ok:
        try:
            detail = resp.json().get('detail')
            parts = detail.split('\n')
            title = parts[0] # workaround long and ugly swagger errors
            text = textwrap.shorten("\n".join(parts[1:]), width=1000)
            msg.fail(f'Error: {title}', text, exits=1)
        except requests.exceptions.JSONDecodeError:
            msg.fail(f'HTTP {resp.status_code} {resp.reason}', resp.text, exits=1)


def post(path, json):
    cfg = read_api_config_or_fail()
    resp = requests.post(f"{cfg['api_url']}{path}", json=json, headers={
        'Authorization': f"Bearer {cfg['api_key']}"
    })
    _fail_for_status(resp)
    return resp.json()


def put(path, json):
    cfg = read_api_config_or_fail()
    resp = requests.put(f"{cfg['api_url']}{path}", json=json, headers={
        'Authorization': f"Bearer {cfg['api_key']}"
    })
    _fail_for_status(resp)
    return resp.json()


def get(path, params=None):
    cfg = read_api_config_or_fail()
    resp = requests.get(f"{cfg['api_url']}{path}", params=params, headers={
        'Authorization': f"Bearer {cfg['api_key']}"
    })
    _fail_for_status(resp)
    return resp.json()


def delete(path):
    cfg = read_api_config_or_fail()
    resp = requests.delete(f"{cfg['api_url']}{path}", headers={
        'Authorization': f"Bearer {cfg['api_key']}"
    })
    _fail_for_status(resp)
    return resp.json()


def get_cli_bots():
    return get('/v1/cli/bots').get('bots')


def post_cli_bots(data):
    return post('/v1/cli/bots', json=data)


def put_cli_bots(name, data):
    return put(f'/v1/cli/bots/{name}', json=data)


def delete_cli_bots(name):
    delete(f"/v1/cli/bots/{name}")


def get_cli_dialogs(bot):
    return get(f'/v1/cli/dialogs?bot={bot}').get('dialogs')


def get_history_turns(customer_messenger_id):
    return get(f'/v1/history/{customer_messenger_id}/turns').get('turns')


def post_cli_login(api_url, phone_number, password):
    resp = requests.post(f"{api_url}/v1/cli/login", json={'phone_number': phone_number, 'password': password})
    _fail_for_status(resp)
    return resp.json().get('api_key')
