import sys
import discord
import random
from lib import poke_handler
from lib import utils
from lib import constants
from discord.ext import commands

if __name__ == '__main__':
    is_bot = True
    token = None
    admin_id = None
    if len(sys.argv) > 2:
        is_bot = utils.get_bool(sys.argv[1])
        token = sys.argv[2]
        if len(sys.argv) == 4:
            admin_id = int(sys.argv[3])
    else:
        print(utils.print_usage())
        sys.exit(1)
    
    print(f'Running a bot user: {is_bot}')
    print(f'Restricting some commands to admin: {admin_id != None}')

    client = commands.Bot(command_prefix = constants.PREFIXES)

    @client.event
    async def on_ready():
        print('Duck... Duck... Goose!')

    @client.event
    async def on_message(message):
        if message.author.id == client.user.id:
            return
        elif client.user.mentioned_in(message) and message.mention_everyone is False:
            print('quack')
            await message.channel.send('Quack')
        elif message.author.id == constants.POKECORD_ID:
            await poke_handler.handle_pokecord(message)
        
        await client.process_commands(message)

    @client.command()
    async def hi(ctx):
        print('hi')
        await ctx.send('Quack Quack...')

    @client.command(aliases=['cp'])
    async def copy(ctx, *, input):
        if admin_id and ctx.message.author.id == admin_id:
            print(input)
            await ctx.send(input)
        else:
            print(input)
            await ctx.send('Angry Quack!')
        
    @client.command(aliases=['gun'])
    async def shoot(ctx):
        await ctx.send(random.choice(constants.SANCTUARY_GUN_EMOTES))

    client.run(token, bot=is_bot)
