import discord
from discord.ext import commands
from dislash import Option, InteractionClient, OptionType
import requests
import dislash
from assests.assests import Assests

class Slashcommands(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
  @dislash.slash_command(name="wasted", description="Sends a picture of user\'s avatar url with wasted picture on it", guild_ids=Assests.guild_ids, options=[Option("user", "The user to get wasted on", OptionType.USER, required=False)]) 
  async def wasted(self, inter, user:discord.User=None):
    if user == None:
      user = inter.author
    request=requests.get("https://some-random-api.ml/canvas/wasted?avatar=%s" % (user.avatar_url_as(format='png'))) 
    file=open("./assests/wasted.png", "wb")
    file.write(request.content)
    file.close()
    await inter.reply(file=discord.File("./assests/wasted.png")) 


def setup(bot):
  bot.add_cog(Slashcommands(bot))     