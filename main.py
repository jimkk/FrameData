import discord
from discord.ext import commands
import wikis.supercombo as sc

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def fdata(ctx, *args):
    if len(args) != 3:
        await ctx.send('Invalid command.\nFormat should be: `>fdata <game> <character> <move>`')
        return
    game, character, move = args
    game = game.lower()
    character = character.capitalize()
    move = move.upper()
    mv_data = sc.get_move_data(game, character, move)
    embed_message = discord.Embed(description=f'{character} - {move}', url=mv_data['url'])
    embed_message.set_thumbnail(url=mv_data['image'])
    del mv_data['image']
    for key, value in mv_data.items():
        embed_message.add_field(name=key, value=value, inline=True)
    await ctx.send(embed=embed_message)

with open('token', 'r') as f:
    token = f.read()

bot.run(token)
bot.change_presence(activity=discord.Game('Currently working for SF6'))