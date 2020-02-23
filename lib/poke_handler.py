import lib.utils as utils
import discord

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