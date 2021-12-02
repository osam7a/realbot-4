import discord
from discord.ext import commands
from assests.assests import Assests
from dislash import InteractionClient, Button, SelectMenu, SelectOption, ActionRow
class HelpCommand(commands.Cog):
    def __init__(self, bot):
      self.bot=bot
      self.inter_client=InteractionClient(self.bot)

    @commands.command()
    async def help(self, ctx, query=None):
      if query == None:
        home=discord.Embed(title="Hello %s!" % (ctx.author), color=Assests.color)
        menuoptions=[]
        for cog in self.bot.cogs:
          if cog == "ErrorHandler" or "Listeners":
            continue
          else:  
            menuoptions.append(SelectOption(cog, cog))
            home.add_field(name=f"**__{cog.capitalize()}__**", value=f"{cog.capitalize()} Commands")
        
        
        row = ActionRow(
          SelectMenu(
          placeholder="Select a category...",
          custom_id="HomeMenu",
          max_values=1,
          options=menuoptions
        )
        )
        await ctx.reply(embed=home, components=[row])   


def setup(bot):
  bot.add_cog(HelpCommand(bot))    