import discord
from discord.ext import commands
import json


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bad_words = ['shit', 'fuck', 'cum', 'whore', 'ass', 'pussy']

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        for i in self.bad_words:
            if i in message.content:
                return
        if message.author.bot:
            return
        with open("./dicts/deleted.json", "r") as f:
            load = json.load(f)
            load.append({
                "content": f"{message.content}",
                "author": f"{message.author}"
            })
            with open("./dicts/deleted.json", "w") as f:
                json.dump(load, f)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        for i in self.bad_words:
            if i in before.content.lower():
                return
        if before.author.bot:
            return
        with open("./dicts/edited.json", "r") as f:
            load = json.load(f)
            load.append({
                "author": f"{before.author}",
                "before": {
                    "content": f"{before.content}"
                },
                "after": {
                    "content": f"{after.content}"
                }
            })
            with open("./dicts/edited.json", "w") as f:
                json.dump(load, f)

    @commands.Cog.listener()
    async def on_message(self, msg):
      if msg.channel.id == 899258763121405974:
        if len(msg.content.split()) > 1:
          await msg.delete()
          return await msg.author.send("You have to send a 1 word message!")            


def setup(bot):
    bot.add_cog(Listeners(bot))
