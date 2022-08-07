import discord
from discord.ext import commands

TOKEN = '---'
bot = commands.Bot(command_prefix='!!')

reactions = [":white_check_mark:", ":stop_sign:", ":no_entry_sign:"]


@bot.event
async def on_ready():
    print('Bot is ready.')


@bot.command()
async def bug(ctx, desc=None, rep=None):
    yas = '✔️'
    nay = '❌'

    valid_reactions = ['✔️', '❌']

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in valid_reactions

    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)

    if str(reaction.emoji) == yas:
        embed = ctx.channel.send # code to create the embed
        return await ctx.send(embed=embed)

    # there's only two reactions, so if the above function didn't return, it means the second reaction (nay) was used instead
    await ctx.send("Cancelled")

bot.run('MTAwNDg3ODgxNTUyMjIwMTcwMQ.GkP4jc.J8zp1GPFS2ck4rXPuUSkPjtCnUialigDFpJF4A')