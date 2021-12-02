import discord
from discord.ext import commands
import art 
import requests
import aiohttp
import json
import random
from assests.assests import Assests

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
        async with cs.get('https://www.reddit.com/r/MinecraftMemes/search.json?q=url:imgur.com&restrict_sr=on') as r:
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
  async def editsnipe(self, ctx):
    with open("./dicts/edited.json", "r") as f:
      load=json.load(f)
      last_msg=load[-1]
      embed=discord.Embed(title="", color=Assests.color).add_field(name="Author", value=last_msg['author'], inline=False).add_field(name="Before", value=last_msg['before']['content'], inline=False).add_field(name="After", value=last_msg['after']['content'], inline=False)  
      await ctx.reply(embed=embed)

  @commands.command()
  async def encrypt(self, ctx, shift:int, *, text):
        result = ''
        if shift > 25:
            return await ctx.reply("Shift too long!")
        for a in range(len(text)):
            i = text[a]
            if (i.isupper()):
                result += chr((ord(i) - shift - 65) + 65)
            else:
                result += chr((ord(i) - shift - 97) + 97)    
        await ctx.reply(f"Encrypted your message with shift: {shift}, result: **{result}**") 

  @commands.command()
  async def decrypt(self, ctx, shift, *, text):
        result = ''  
        if shift.isalpha() == False:
            for a in range(len(text)):
                i = text[a]
                if (i.isupper()):
                    result += chr((ord(i) + int(shift) + 65) - 65)
                else:
                    result += chr((ord(i) + int(shift) + 97) - 97)     
            return await ctx.reply(f"Decrypted your message, result: **{result}**") 
        else:
            LETTERS=''
            message = text #encrypted message
            if message.isupper():
                LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            elif message.islower():
                LETTERS = "abcdefghijklmnopqrstuvwxyz"
            else:
              LETTERS="abcdefghijklmnopqrstuvwxyz"  
                    
            test=[]
            for key in range(len(LETTERS)):
                translated = ''
                result = ''
                for symbol in message:
                    if symbol in LETTERS:
                        num = LETTERS.find(symbol)
                        num = num - key
                        if num < 0:
                            num = num + len(LETTERS)
                            translated = translated + LETTERS[num]
                        else:
                            translated = translated + symbol
                result += "`Key #%s: %s` " % (key, translated)
                test.append(result)
            await ctx.reply(f"Decryption ended with **{len(LETTERS)}** Possiblities:\n{''.join(test)}")             



    

def setup(bot):
  bot.add_cog(Fun(bot))    