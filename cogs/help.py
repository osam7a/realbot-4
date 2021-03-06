import discord
from assests.assests import Assests

from discord.ext import commands



class NewHelpName(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, color=Assests.color)
            await destination.send(embed=emby)