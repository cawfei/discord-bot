import sys
import discord
from discord.ext import commands


if __name__ == '__main__':
    token = None
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        print('Missing token. Exiting...')
        sys.exit(1)

    client = commands.Bot(command_prefix = 'd>')

    @client.event
    async def on_ready():
        print('Duck... Duck... Goose!')


    client.run(token)
