import sys
import discord
import random
from lib import poke_handler
from lib import utils
from lib import constants as const
from lib import dynamodb_handler as dynamo
from discord.ext import commands, tasks

if __name__ == '__main__':
    is_bot = True
    upload_to_dynamo = False
    poke_assist = utils.PokeAssist.assist
    token = None
    admin_id = None
    channels_to_spam = {}

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
    print(f'Upload pokemon to dynamo table: {upload_to_dynamo}')

    client = commands.Bot(command_prefix = const.PREFIXES)

    @client.event
    async def on_ready():
        print('Duck... Duck... Goose!')
        await client.change_presence(activity=discord.Game('Duck Duck Goose'))
        spam.start()

    @client.event
    async def on_message(message):
        if message.author.id == client.user.id:
            return

        if message.author.id == const.POKECORD_ID:
            s_time = 0
            if message.guild.id == const.SANCTUARY_GUILD_ID:
                s_time = 45
            await poke_handler.handle_pokecord(message, poke_assist, upload_to_dynamo, s_time)
        if client.user.mentioned_in(message) and message.mention_everyone is False:
            await message.channel.send('Quack')

        await client.process_commands(message)

    @client.command(hidden=True, aliases=['cp'])
    async def copy(ctx, *, input):
        if admin_id and ctx.message.author.id == admin_id:
            print(input)
            await ctx.send(input)
        else:
            print(input)
            await ctx.send('Angry Quack!')

    @client.command(hidden=True, aliases=['tu'])
    async def toggle_upload(ctx):
        global upload_to_dynamo
        if admin_id and ctx.message.author.id == admin_id:
            upload_to_dynamo = not upload_to_dynamo
            await ctx.send(f'Upload Pokémon: {upload_to_dynamo}... Quack!')
        else:
            await ctx.send('Angry Quack!')

    @client.command(hidden=True, aliases=['pal'])
    async def poke_assist_level(ctx, *, pal):
        global poke_assist
        if admin_id and ctx.message.author.id == admin_id:
            msg = None
            if pal == utils.PokeAssist.none.name:
                poke_assist = utils.PokeAssist.none
            elif pal == utils.PokeAssist.assist.name:
                poke_assist = utils.PokeAssist.assist
            elif pal == utils.PokeAssist.catch.name:
                if is_bot:
                    msg = 'Bot users cant catch Pokémon! Quack!'
                else:
                    poke_assist = utils.PokeAssist.catch
            else:
                msg = 'Invalid input Quack! Please enter \'none\', \'assist\' or \'catch\''

            if msg is None:
                msg = f'Poke Assist level changed to: {poke_assist.name}! Quack!'
            await ctx.send(msg)
        else:
            await ctx.send('Angry Quack!')

    @client.command(aliases=['get'])
    async def retrieve(ctx, *, img_url):
        msg = 'Sad Quack! Can\'t find the Pokémon...'
        img_hash = utils.get_img_hash(img_url)
        found, name = dynamo.try_retrieve_pokemon(img_hash)
        if found:
            msg = f'That is a {name}! Quack!'
        await ctx.send(msg)

    @client.command(hidden=True, aliases=['as'])
    async def add_spam(ctx):
        global channels_to_spam
        if not admin_id or not ctx.message.author.id == admin_id:
            await ctx.send('Angry Quack!')
        else:
            channels_to_spam[ctx.message.channel.id] = True
            await ctx.send(f'Spamming for {ctx.message.channel.name} in {ctx.message.channel.guild.name}. Quack!')

    @client.command(hidden=True,  aliases=['ss'])
    async def stop_spam(ctx):
        global channels_to_spams
        if not admin_id or not ctx.message.author.id == admin_id:
            await ctx.send('Angry Quack!')
        else:
            channels_to_spam[ctx.message.channel.id] = False
            await ctx.send(f'Stopping spam for {ctx.message.channel.name} in {ctx.message.channel.guild.name}. Quack!')

    @client.command(hidden=True, aliases=['lb'])
    async def load_bulk(ctx, *, indices):
        inds = indices.split()
        if not admin_id or not ctx.message.author.id == admin_id:
            await ctx.send('Angry Quack!')
        elif not upload_to_dynamo:
            await ctx.send(f'Must enable Pokémon upload... Quack')
        elif not len(inds) == 2:
            await ctx.send('Please provide pokedex start and end like this: \'d.lb 1 700\'. Quack.')
        elif is_bot:
            await ctx.send('Cannot be a bot user... Quack.')
        else:
            try:
                start = int(inds[0])
                end = int(inds[1])
                poke_handler.set_bulk_load_params(start, end)
                await ctx.send(f'.pokedex #{start}')
            except ValueError as verr:
                await ctx.send(f'Please give two numbers... Quack!')

    @client.command()
    async def hi(ctx):
        print('hi')
        await ctx.send('Quack Quack...')
        
    @client.command(aliases=['gun'])
    async def shoot(ctx):
        await ctx.send(random.choice(const.SANCTUARY_GUN_EMOTES))

    @tasks.loop(seconds=2)
    async def spam():
        for cid in list(channels_to_spam):
            if channels_to_spam[cid]:
                channel = await client.fetch_channel(cid)
                await channel.send(content="Quack")

    client.run(token, bot=is_bot)
