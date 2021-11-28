import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from dislash import InteractionClient, Option

client = commands.Bot(command_prefix="r!")
guild_ids=[892792256002682920]
inter_client = InteractionClient(client)
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
  client.load_extension("cogs.slashcommands")
  client.load_extension("cogs.listeners")
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

@inter_client.slash_command(name="reload", description="Reloads an extension", options=[Option("cog", "The cog you want to load")], guild_ids=guild_ids)
async def reload(inter, cog):
  if inter.author.id == 761159873194491915 or inter.author.id == 473125594410909696:
    try:
      client.unload_extension(f"cogs.{cog}")
      client.load_extension(f"cogs.{cog}")
      await inter.reply(f"Reloaded extension {cog}", ephemeral=True)
    except commands.ExtensionNotLoaded:
      client.load_extension(f"cogs.{cog}")
      await inter.reply(f"Loaded extension {cog}", ephemeral=True)
    except commands.ExtensionNotFound:
      await inter.reply(f"No cog with name {cog}", ephemeral=True)
    except commands.ExtensionFailed:
      await inter.reply(f"```diff\n- {commands.ExtensionFailed.original}\n```", ephemeral=True)      
  else:
    await inter.reply("You do not have permissions to do that.", ephemeral=True) 

@client.event
async def on_command(ctx):
  if ctx.author.id != 761159873194491915 or ctx.author.id != 473125594410909696:
    if maintainence == True:
      return await ctx.reply("Bot in maintainence! You cannot run any commands.")
keep_alive()
client.run(os.getenv("TOKEN"))