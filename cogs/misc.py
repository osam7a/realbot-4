import discord
from discord.ext import commands
import requests
import os
import aiohttp
from assests.assests import Assests
import random

class Misc(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
  @commands.command()
  async def wasted(self, ctx, user:discord.User=None):
    if user == None:
      user = ctx.author
    request=requests.get("https://some-random-api.ml/canvas/wasted?avatar=%s" % (user.avatar_url_as(format='png'))) 
    file=open("./assests/wasted.png", "wb")
    file.write(request.content)
    file.close()
    await ctx.reply(file=discord.File("./assests/wasted.png")) 
  
  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def purge(self, ctx, limit:int):
    await ctx.channel.purge(limit=limit)
    await ctx.send("Purged %s messages" % limit, delete_after=3)


  @commands.command()
  async def screenshot(self, ctx, url):
   async with ctx.typing(): 
    async with aiohttp.ClientSession() as cs:
      async with cs.post(
    "https://api.deepai.org/api/nsfw-detector",
    data={
        'image': f'https://image.thum.io/get/{url}',
    },
    headers={'api-key': 'ca94ba74-a1fd-4cbd-87e5-286f843f1202'}) as r:
        a=await r.json()
        print(a)
   if a['output']['nsfw_score'] > 0.005:
          return await ctx.reply("That contains NSFW!")
   if url.startswith("https://"):
          
              await ctx.reply(embed=discord.Embed(title="Link", url=url, color=Assests.color).set_image(url=f"https://image.thum.io/get/{url}")) 
   else:
          await ctx.reply("Invalid url")      



  @commands.command()
  async def jail(self, ctx, user:discord.User=None):
    if user == None:
      user=ctx.author
    request=requests.get(f"https://some-random-api.ml/canvas/jail?avatar={user.avatar_url_as(format='png')}")
    file=open("./assests/jailed.png", "wb")
    file.write(request.content)
    file.close()
    await ctx.reply(file=discord.File("./assests/jailed.png")) 

  @commands.command()
  async def passed(self, ctx, user:discord.User=None):
    if user == None:
      user=ctx.author
    request=requests.get("https://some-random-api.ml/canvas/passed?avatar=%s" % (user.avatar_url_as(format='png')))
    file=open("./assests/passed.png", "wb")
    file.write(request.content)
    file.close()
    await ctx.reply(file=discord.File("./assests/passed.png")) 

  @commands.command()
  async def comrade(self, ctx, user:discord.User=None):
    if user == None:
      user = ctx.author
    request=requests.get("https://some-random-api.ml/canvas/comrade?avatar=%s" % (user.avatar_url_as(format='png')))
    file=open("./assests/comrade.png", "wb")
    file.write(request.content)
    file.close()
    await ctx.reply(file=discord.File("./assests/comrade.png"))

  @commands.command()
  async def triggered(self, ctx, user:discord.User=None):
    if user == None:
      user = ctx.author
    request=requests.get("https://some-random-api.ml/canvas/triggered?avatar=%s" % (user.avatar_url_as(format='png')))
    file=open("./assests/triggered.gif", "wb")
    file.write(request.content)
    file.close()
    await ctx.reply(file=discord.File("./assests/triggered.gif"))

  @commands.command()
  async def animal(self, ctx): 
     query = random.choice(["cat", "koala", "panda", "red_panda", "whale", "kangaroo"])    
     request=requests.get("https://some-random-api.ml/animal/%s" % (query))
     json = request.json()
     embed=discord.Embed(title=json['fact'], url=json['image'], color=Assests.color).set_image(url=json['image'])
     await ctx.reply(embed=embed)

  @commands.command(aliases=['image', 'pic']) 
  async def img(self, ctx, query):
    request=requests.get("https://source.unsplash.com/1600x900/?%s" % (query))
    file= open("./assests/img.png", "wb")
    file.write(request.content)
    file.close()
    await ctx.reply(file=discord.File("./assests/img.png"))        



def setup(bot):
  bot.add_cog(Misc(bot))    