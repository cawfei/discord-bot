import hashlib
import os
import requests

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
    page = requests.get(url)

    f_ext = os.path.splitext(url)[-1]
    f_name = 'img{}'.format(f_ext)
    with open(f_name, 'wb') as f:
        f.write(page.content)
    
    return hashlib.md5(open(f_name,'rb').read()).hexdigest()
