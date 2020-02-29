import hashlib
import os
import requests
from enum import Enum

class PokeAssist(Enum):
    none = 1
    assist = 2
    catch = 3

# print out how to run this bot
def print_usage():
    message = """
    Usage: python3 bot.py <is-bot> <token> <admin-user-id (optional)>

    <is-bot> Whether the token is a bot user: 'true' or 'false'  
    <token> Discord token of the user.
    <admin-user-id> user-id of the admin where some commands can only be run by.
        If not provided, all commands can be run by all users.
    """
    print(message)

# return whether the passed in param is a bool or should be one
def get_bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# Given a url, retrieve an image and return the md5 hash
def get_img_hash(url):
    response = requests.get(url)
    # Check to make sure we got an HTTP 2XX response
    if response.status_code // 100 != 2:
        raise RuntimeError(f'failed to fetch image {url}')
    return hashlib.sha256(response.content).hexdigest()