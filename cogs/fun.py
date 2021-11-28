import discord
import art 
import requests
import json
import random
import aiohttp
from assests.assests import Assests
from discord.ext import commands

class Fun(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
  @commands.command()
  async def textart(self, ctx, *, text):
    if len(text) > 14:
      return await ctx.reply("Message too long! Message should be less than 14 characters")
    result = art.text2art(text)
    await ctx.reply(f"```\n{result}\n```")

  @commands.command()
  async def meme(self, ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            post=random.choice(res['data']['children'])
            embed=discord.Embed(title=post['data']['title'], url=f"https://www.reddit.com/{post['data']['permalink']}", color=Assests.color).set_image(url=post['data']['url'])
            await ctx.reply(embed=embed)

  @commands.command()
  async def reddit(self, ctx, subreddit, sort=None):
    if sort == None:
      sort = "hot"
    async with aiohttp.ClientSession() as cs:
      async with cs.get(f"https://www.reddit.com/r/{subreddit}/new.json?sort={sort}&nsfw=false") as r:
        res = await r.json()
        post=random.choice(res['data']['children'])   
        embed=discord.Embed(title=post['data']['title'], url=f"https://www.reddit.com/{post['data']['permalink']}", color=Assests.color)
        if post['data']['url'].endswith(".png") or post['data']['url'].endswith(".gif") or post['data']['url'].endswith(".jpg"):
          embed.set_image(url=post['data']['url'])
        else:
          embed.description=post['data']['selftext'][0:3000]  

        await ctx.reply(embed=embed) 

  @commands.command()
  async def emojify(self, ctx, *, text):
      result = ""
      for i in text.lower():
        if i == " ":
          result += "  "
        else:
          result += f":regional_indicator_{i}:"   

      await ctx.reply(result) 

  @commands.command()
  async def snipe(self, ctx):
    with open("./dicts/deleted.json", "r") as f:
      load = json.load(f)
    last_msg = load[-1]
    embed=discord.Embed(title="", color=Assests.color).add_field(name="Author", value=last_msg['author'], inline=False).add_field(name="Content", value=last_msg['content'])
    await ctx.reply(embed=embed)

  @commands.command()
  async def edited(self, ctx):
    with open("./dicts/edited.json", "r") as f:
      load=json.load(f)
      last_msg=load[-1]
      embed=discord.Embed(title="", color=Assests.color).add_field(name="Author", value=last_msg['author'], inline=False).add_field(name="Before", value=last_msg['before']['content'], inline=False).add_field(name="After", value=last_msg['after']['content'], inline=False)  
      await ctx.reply(embed=embed) 

   
    

def setup(bot):
  bot.add_cog(Fun(bot))    