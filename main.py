import sys
import os
from os import path
import discord
import dotenv
from discord.ext import commands
from data.db import Database
from wikis.base import Wiki
from wikis.exceptions import MoveNotFound
from wikis.supercombo import SuperCombo

sys.path.append('../FrameData')
dotenv.load_dotenv()



intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

if os.getenv('db_url') is None:
    print('Must supply a "db_url" variable')
    exit(-1)
db = Database(os.getenv('db_url'))

wikis : dict[str,Wiki] = {
    'sf6': SuperCombo
}

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def stats(ctx, *args):
    '''Get the stats for a given character'''
    if len(args) != 2:
        await ctx.send('Invalid command.\nFormat should be: `>stats <game> <character>`')
        return
    game, character = args
    game = game.lower()
    character = character.title()
    if game not in wikis.keys():
        await ctx.send('Invalid game')
        return
    wiki = wikis[game]
    info = wiki.get_info_box(game, character)
    embed = discord.Embed(description=f'{character}')
    for key, value in info.items():
        embed.add_field(name=key, value=value, inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def fdata(ctx, 
                game: str = commands.parameter(description="The game name (ex. 'sf6')"), 
                character: str = commands.parameter(default=None, description="The character's name (ex. 'Ryu')"), 
                move_id:str = commands.parameter(default=None, description="The name of the move (ex. 5MP, 236P, 236236P, 236P~P)")):
    '''
    Gets the frame data for a certain move.
    '''
    if character is None:
        user_pref = db.get_preference(ctx.author.id).character_pref
        if game is not None and user_pref is not None:
            move_id = game
            game = user_pref['game']
            character = user_pref['character']
        else:
            await ctx.send('Invalid command.\nFormat should be: `>fdata <game> <character> <move>`')
            return
    game = game.lower()
    character = character.title()
    move_id = move_id.upper()
    move_obj_list = db.get_character_data(game, character, move_id)
    if len(move_obj_list) == 0:
        if game not in wikis.keys():
            await ctx.send('Invalid game', reference=ctx.message)
            return
        wiki = wikis[game]
        try:
            move_obj_list = wiki.get_move_data(game, character, move_id)
        except MoveNotFound:
            await ctx.send('Move not found.', reference=ctx.message)
            return
        db.add_character_data(move_id, move_obj_list)
    embeds = []
    for move_obj in move_obj_list:
        embed_message = discord.Embed(description=f'{character} - {move_obj.move_id}')
        embed_message.set_thumbnail(url=move_obj.image)
        for key, value in move_obj.properties.items():
            embed_message.add_field(name=key, value=value, inline=True)
        embed_message.add_field(name='URL source', value=move_obj.url, inline=False)
        embeds.append(embed_message)
    await ctx.send(embeds=embeds)

@bot.command()
async def sourcecode(ctx):
    await ctx.send('Here is the source code link: ' + 'https://github.com/jimkk/FrameData')


@bot.command()
async def addpref(ctx, *args):
    if len(args) != 2:
        await ctx.send('Invalid command.\nFormat should be: `>addpref <game> <character>`')
        return
    game, character = args
    db.add_preference(ctx.author.id, {'game': game, 'character': character})
    await ctx.send(f'Added saved preference for <@{ctx.author.id}>: Game: `{game}`, Character: `{character}`')

if path.exists('token'):
    with open('token', 'r', encoding='utf-8') as f:
        token = f.read()
else:
    dotenv.load_dotenv()
    token = os.getenv('token')

bot.run(token)
