from dataclasses import dataclass
from enum import Enum

import requests

from chai_py.auth import get_auth
from chai_py import defaults, error


class BotStatus(Enum):
    """
    Active bots can be discovered by users on the app
    and inactive bots can only be accessed with a direct link.
    """
    ACTIVE = 1
    INACTIVE = 2


@dataclass
class DeployedBot:
    """
    A currently deployed chatbot.

    Args:
        bot_uid (str): The unique ID of the chatbot.
        name (str): The name of the chatbot.
        developer_uid (str): ID of the developer who created the chatbot.
        status (BotStatus): Whether the chatbot is visible to users.
    """
    bot_uid: str
    name: str
    developer_uid: str
    status: BotStatus


def get_bots():
    """
    Retrive a summary of all bots deployed by a developer.

    Returns:
        list[DeployedBot]: list of bots you have deployed.
    """
    url = '{}/chatbots'.format(defaults.API_HOST)
    js = {'developer_uid': _get_developer_uid()}
    resp = requests.get(url, params=js, auth=_credentials())
    _check_response_for_error(resp)
    return _parse_multiple_bots_response(resp)


def activate_bot(bot_uid: str):
    """
    Activate a bot so it can be discovered by users on the app.

    Args:
        bot_uid (str): the unique ID of the bot to make visibile
    """
    url = '{}/chatbots/{}'.format(defaults.API_HOST, bot_uid)
    js = {'status': 'active'}
    resp = requests.post(url, json=js, auth=_credentials())
    _check_response_for_error(resp)


def deactivate_bot(bot_uid: str):
    """
    Deactivate a bot so it cannot be discovered by users on the app.

    Args:
        bot_uid (str): the unique ID of the bot to remove from visibility.
    """
    url = '{}/chatbots/{}'.format(defaults.API_HOST, bot_uid)
    js = {'status': 'inactive'}
    resp = requests.post(url, json=js, auth=_credentials())
    _check_response_for_error(resp)


def _check_response_for_error(resp):
    if resp.status_code != 200:
        raise error.APIError('Bad response ({}): {}'.format(resp.status_code, resp.text))


def _get_developer_uid():
    return get_auth().uid


def _credentials():
    auth = get_auth()
    return requests.auth.HTTPBasicAuth(auth.uid, auth.key)


def _parse_multiple_bots_response(resp):
    bots = []
    for raw_bot_response in resp.json()['data']:
        bots.append(_parse_raw_bot_dict(raw_bot_response))
    return bots


def _parse_raw_bot_dict(data):
    status = BotStatus[data['status'].upper()]
    return DeployedBot(data['bot_uid'], data['name'], data['developer_uid'], status)
