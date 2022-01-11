import discord
from discord.ext import commands
import json
from assests.assests import Assests
from discord import Webhook, RequestsWebhookAdapter
import re

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
      if msg.author.bot: return
      if msg.channel.id == 899258763121405974:
        if len(msg.content.split()) > 1:
          await msg.delete()
          return await msg.author.send("You have to send a 1 word message!")            
      elif msg.channel.id != 917474658889105468: return
      else:
        try:
          f=open("./dicts/currcount.json", "r")
          load=json.load(f)
          msgnum=int(msg.content)
          
          if load['currentcount'] + 1 == msgnum:
            if load['lastauthor'] == str(msg.author.id):
             print(msg.author)
             await msg.delete()
             return
            load['currentcount'] += 1
            f2=open("./dicts/currcount.json", "w")
            load['lastauthor'] = str(msg.author.id)
            json.dump(load, f2)
            return
            
          else:
            if load['lastauthor'] == str(msg.author.id):
             print(msg.author)
             await msg.delete()
             return
            load['currentcount'] += 1
            load['lastauthor'] = str
            (msg.author.id) 
            f2=open("./dicts/currcount.json", "w")
            json.dump(load, f2) 
            await msg.delete()  
            webhook = Webhook.from_url('https://discord.com/api/webhooks/917478130254479460/GwUNZesTyt5UVArRNRaCLMf2EY5v86TizZDvwoJ6Xbqxtb3bQ8R7o49gPY9xNQxNGA0u', adapter=RequestsWebhookAdapter())
            await webhook.send(username=msg.author.name, avatar_url=msg.author.avatar_url, content=load['currentcount']+1)
            
            return
        except:
          await msg.delete()
          
        

def setup(bot):
    bot.add_cog(Listeners(bot))
