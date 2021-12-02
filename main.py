import discord
from discord.ext import commands
import os
from cogs.help import HelpCommand
from keep_alive import keep_alive


client = commands.Bot(command_prefix="r!", allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True, replied_user=True), help_command=None)
maintainence=False

@client.command()
async def maintainence(ctx, boolean):
  maintainence=bool(boolean)
  await ctx.reply(f"Set maintainence to {boolean}")

@client.event
async def on_ready():
  print("[--Running Cogs--]")
  client.load_extension("cogs.fun")
  client.load_extension("cogs.misc")
  client.load_extension("cogs.help")
  client.load_extension("cogs.listeners")
  client.load_extension("cogs.error")
  client.load_extension("cogs.economy")
  for cog in client.cogs:
    print(cog)
  print(f"[--System Info--]\nBot Name: {client.user}\nBot ID: {client.user.id}") 

@client.command()
async def reload(ctx, cog):
  if ctx.author.id == 761159873194491915 or ctx.author.id == 473125594410909696:
    try:
      client.unload_extension(f"cogs.{cog}")
      client.load_extension(f"cogs.{cog}")
      await ctx.reply(f"Reloaded extension {cog}")
    except commands.ExtensionNotLoaded:
      client.load_extension(f"cogs.{cog}")
      await ctx.reply(f"Loaded extension {cog}")
    except commands.ExtensionNotFound:
      await ctx.reply(f"No cog with name {cog}")
    except commands.ExtensionFailed:
      await ctx.reply(f"```diff\n- {commands.ExtensionFailed.original}\n```")      
  else:
    await ctx.reply("You do not have permissions to do that.")  

 

@client.event
async def on_command(ctx):
  if ctx.author.id != 761159873194491915 or ctx.author.id != 473125594410909696:
    if maintainence == True:
      return await ctx.reply("Bot in maintainence! You cannot run any commands.")
keep_alive()
client.run(os.getenv("TOKEN"))