import discord 
from discord.ext import commands

import aiohttp 
import asyncio 

import datetime 
import time 

import random 
import string

intents = discord.Intents.default()
intents.members = True 
intents.reactions = True

PREFIX = ">"
TOKEN = "Your bot token goes here"

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents
)

@bot.event 
async def on_ready():
    print('Bot Ready!')
    
@bot.command()
async def gw(ctx, time: int, *, prize):
    if ctx.author.guild_permissions.administrator:
        await ctx.message.delete()
        
        embed = discord.Embed(
            color = discord.Color.gold(),
            title = f"{prize}",
            description = f"New Giveaway hosted by {ctx.author.mention}"
        )
        embed.set_footer(text=f"Ends in {time}mins", icon_url=ctx.author.avatar_url)
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('🎉')
        
        await asyncio.sleep(time * 60)
        
        x = await ctx.channel.fetch_message(msg.id)
        reacts = await x.reactions[0].users().flatten()
        reacts.pop(reacts.index(bot.user))
        winner = random.choice(reacts)

        embed = discord.Embed(
            color = discord.Color.green(),
            title = f"You winned {prize}!",
            description = f"Check {ctx.channel.mention} to reedem your prize!"
        )
        try:
            await winner.send(embed=embed)
        except:
            pass 
        
        embed = discord.Embed(
            color = discord.Color.green(),
            title = "Giveaway Finished",
            description = f"Prize: {prize}\nWinner: {winner.mention}\nHost: {ctx.author.mention}"
        )
        
        await msg.edit(embed=embed)
        return
    
    embed = discord.Embed(
        color = discord.Color.red()
    )
    embed.add_field(name="Error", value="You don't have any permissions to create a Giveaway")
    await ctx.send(embed=embed)
    
    
if __name__ == '__main__':
    bot.run(TOKEN)