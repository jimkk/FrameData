import sys
import discord
from discord.ext import commands
import wikis.supercombo as sc

sys.path.append('../FrameData')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def stats(ctx, *args):
    if len(args) != 2:
        await ctx.send('Invalid command.\nFormat should be: `>stats <game> <character>`')
        return
    game, character = args
    game = game.lower()
    character = character.title()
    info = sc.get_info_box(game, character)
    embed = discord.Embed(description=f'{character}')
    for key, value in info.items():
        embed.add_field(name=key, value=value, inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def fdata(ctx, *args):
    if len(args) != 3:
        await ctx.send('Invalid command.\nFormat should be: `>fdata <game> <character> <move>`')
        return
    game, character, move_id = args
    game = game.lower()
    character = character.title()
    move_id = move_id.upper()
    move_obj_list = sc.get_move_data(game, character, move_id)
    embeds = []
    for move_obj in move_obj_list:
        embed_message = discord.Embed(description=f'{character} - {move_obj.name}')
        embed_message.set_thumbnail(url=move_obj.image_link)
        for key, value in move_obj.properties.items():
            embed_message.add_field(name=key, value=value, inline=True)
        embed_message.add_field(name='URL source', value=move_obj.url, inline=False)
        embeds.append(embed_message)
    await ctx.send(embeds=embeds)

@bot.command()
async def sourcecode(ctx):
    await ctx.send('Here is the source code link: ' + 'https://github.com/jimkk/FrameData')

with open('token', 'r', encoding='utf-8') as f:
    token = f.read()

bot.run(token)
