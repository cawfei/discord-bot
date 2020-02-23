def print_usage():
    message = """
    Usage: python3 bot.py <is-bot> <token> <admin-user-id (optional)>

    <is-bot> Whether the token is a bot user: 'true' or 'false'  
    <token> Discord token of the user.
    <admin-user-id> user-id of the admin where some commands can only be run by.
        If not provided, all commands can be run by all users.
    """
    print(message)

def get_bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')