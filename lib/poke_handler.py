import lib.utils as utils
import discord

# Scrape information from dex info command
def scrape_dex_info(e):
    deets = e.title.split()
    
    if len(deets) == 5:
        name = deets[3]
    elif len(deets) == 6:
        if deets[3] == 'Alolan':
            name = f'Alolan {deets[4]}'
        elif deets[3] == 'Detective':
            name = f'Detective {deets[4]}'
        else:
            name = f'Shiny {deets[4]}'
    elif len(deets) == 7:
        name = f'Shiny {deets[4]} {deets[5]}'

    return deets[-1][:-1], name, utils.get_img_hash(e.image.url)

# Scrape information from personal info commands
def scrape_owned_info(e):
    deets = e.title.split()
    
    if len(deets) == 3:
        name = deets[2]
    elif len(deets) == 4:
        if deets[1] == 'Alolan':
            name = f'Alolan {deets[3]}'
        elif deets[1] == 'Detective':
            name = f'Detective {deets[3]}'
        else:
            name = f'Shiny {deets[3]}'
    elif len(deets) == 5:
        name = f'Shiny {deets[3]} {deets[4]}'

    return name, utils.get_img_hash(e.image.url)

# Handle all incoming messages pertaining to pokecord
async def handle_pokecord(message):
    for e in message.embeds:
        print(f'title: {e.title}')
        print(f'image url: {e.image.url}')
        if 'Base stats for' in e.title:
            num, name, img_hash = scrape_dex_info(e)
            print(img_hash)
            await message.channel.send(f'The displayed Pokémon is a {name} with National Dex entry: {num}.\nHash: {img_hash}')
        elif 'Level' in e.title:
            name, img_hash = scrape_owned_info(e)
            print(img_hash)
            await message.channel.send(f'Nice {name}! Quack!\nHash: {img_hash}')
        elif 'A wild pokémon has аppeаred!' in e.title:
            img_hash = utils.get_img_hash(e.image.url)
            print(img_hash)
            await message.channel.send(f'A wild Pokémon... Quack.\nHash: {img_hash}')
