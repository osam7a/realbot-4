import nextcord as discord
from nextcord.ext import commands

async def emb(ctx, title, description, color, **kwargs):
    embed=discord.Embed(title=title, description=description, color=color)
    await ctx.reply(embed=embed)

class Assests:
  color=0x2ecc71
  guild_ids=[892792256002682920]
  