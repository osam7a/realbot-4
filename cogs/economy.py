import discord as discord
from discord.ext import commands
import json
import os
import asyncio

import random
from assests.assests import *

class Economy(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
    self.emojis = {e.name:str(e) for e in self.bot.emojis}
    self.emoji = self.emojis['money']
    with open("./dicts/economyshop.json", "r") as f:
      loadshop=json.load(f)
    self.shop = loadshop

    
  @commands.command(aliases=['register', 'reg'])
  async def start(self, ctx):
    with open("./dicts/economy.json", "r") as f:
      load = json.load(f)
      if f"{ctx.author.id}" not in load:
        load[f"{ctx.author.id}"] = {"balance":0, "username":f"{ctx.author}", "bank":{"max":False, "amount":0, "maxamount":5000}, "inventory":{}}
        await ctx.reply(f"You have been registered into the database!")
        with open("./dicts/economy.json", "w") as f:
          json.dump(load, f)
      else:
        return await ctx.reply("You are already registered!") 

  @commands.command(aliases=['bal', 'money', 'cash'])
  async def balance(self, ctx, user:discord.Member=None):
    if user == None:
      user = ctx.author
    with open("./dicts/economy.json", "r") as f:
      load = json.load(f)  
      if f"{user.id}" not in load:
        return await ctx.reply(f"{user.mention} Have not been registered! Do r!start") 
      bal = load[f'{user.id}']['balance']
      ban = load[f'{user.id}']['bank']['amount']
      maxban=load[f'{user.id}']['bank']['maxamount']
      await ctx.reply(embed=discord.Embed(title=f"{user.name}\'s balance", description=f":dollar: **Wallet**: {self.emoji}{bal}\n:bank: **Bank**: {self.emoji}{ban}/{self.emoji}{maxban}", color=Assests.color))  

  @commands.command()
  @commands.cooldown(1, 60*30, commands.BucketType.user)
  async def work(self, ctx):
    with open("./dicts/economy.json", "r") as f:
        load=json.load(f)
    if f"{ctx.author.id}" not in load:
        return await ctx.reply("You have not registered yet! Do r!start to get into our database.") 
    a= random.randint(0, 1500)  
    f=random.randint(0, 500)  
    statments= [[f"You impressed your boss by making a giant machine, here's {self.emoji}{a}", f"The boss decided to give you {self.emoji}{a}", f"You got {self.emoji}{a} for creating a big car", f"You got {self.emoji}{a} for cleaning a vent", f"You earned {self.emoji}{a} from streaming minecraft on twitch", f"You almost got stung by a bee but still earned {self.emoji}{a}", f"You work as a proffessional cuddler and earn {self.emoji}{a}", f"You work {random.randint(5, 15)} minutes at pizzahut and earn {self.emoji}{a}"], [f"You did terrible at work, you were fined {self.emoji}{f}", f"You light up a fire at the whole office building, you were fined {self.emoji}{f}", f"You broke the boss favorite mug, he fined you {self.emoji}{f}", f"You crash your car and got fined {self.emoji}{a}", f"You killed your boss fish by accident, you pay him {self.emoji}{f} as an apology", f"You accidently deleted the whole company database, the boss fined you {self.emoji}{f}"]]
    statement = random.choice(statments)
    embed=discord.Embed(title="", color=Assests.color)
    if statement == statments[0]:
      embed.title="You got payed!"
      embed.description=random.choice(statement)
      load[f'{ctx.author.id}']['balance'] += a
    else:
      if load[f'{ctx.author.id}']['balance'] - f < 0:
        embed.title = f"You have a less amount of money in your account, so you have not been fined!"
      else:  
          embed.title="You were fined!"
          embed.color=discord.Colour.red()
          embed.description=random.choice(statement) 
          load[f'{ctx.author.id}']['balance'] -= f
    
    with open("./dicts/economy.json", "w") as f:
        json.dump(load, f)
    await ctx.reply(embed=embed)  

  @commands.command()
  @commands.cooldown(1, 60*10, commands.BucketType.user)
  async def crime(self, ctx):
    with open("./dicts/economy.json", "r") as f:
        load=json.load(f)
    if f"{ctx.author.id}" not in load:
        return await ctx.reply("You have not registered yet! Do r!start to get into our database.")    
    if f"{ctx.author.id}" not in load:
        return await ctx.reply("You have not registered yet! Do r!start to get into our database.") 
    a= random.randint(0, 1500)  
    f=random.randint(0, 1000)
    statements=[[f"You sneaked out and took your dad's wallet, you earned {self.emoji}{a}", f"You break in to a supermarket and aggresivly ask for money, the cashier gives you {self.emoji}{a}", f"You robbed a bank and gained {self.emoji}{a}", f"You made a pyramid scheme gaining {self.emoji}{a} in the proccess", f"You successfully decrypted files you stole from FBI, you gained {self.emoji}{a}"], [f"You robbed secret files from the FBI, but ended up getting caught and got fined by {self.emoji}{f}", f"You tried to insult a kid, but he roasted you instead, he took from you {self.emoji}{f}", f"You tried running away after a bank heist, but ended up getting caught and fined {self.emoji}{f}"]]
    statement=random.choice(statements)
    embed=discord.Embed(title="", color=Assests.color)
    if statement == statements[0]:
      embed.title="You ran away!"
      embed.description=random.choice(statement)
      load[f'{ctx.author.id}']['balance'] += a
    else:
      if load[f'{ctx.author.id}']['balance'] - f < 0:
        embed.title = f"You have a less amount of money in your account, so you have not been fined!"
      else:  
          embed.title="You were fined!"
          embed.color=discord.Colour.red()
          embed.description=random.choice(statement) 
          load[f'{ctx.author.id}']['balance'] -= f
    
    with open("./dicts/economy.json", "w") as f:
        json.dump(load, f)
    await ctx.reply(embed=embed)  

  @commands.command(aliases=['deposit'])
  async def dep(self, ctx, amount:int):
      with open("./dicts/economy.json", "r") as f:
        load=json.load(f)
      if f"{ctx.author.id}" not in load:
        return await ctx.reply("You have not registered yet! Do r!start to get into our database.")  
      user = load[f'{ctx.author.id}']
      if user['bank']['max'] == True:
        return await ctx.reply(embed=discord.Embed(title="Oops! Your bank is full!", description=f"Your bank is currently full! {user['bank']['amount']}/{user['bank']['maxamount']}\n**How to get more space?**\nYou need to get banknotes for that!", color=discord.Colour.red()))
      if amount > load[f'{ctx.author.id}']['bank']['maxamount']:
        return await ctx.reply(embed=discord.Embed(title="Not enough capacity!", description=f"Your bank can hold only {user['bank']['maxamount']}!", color=discord.Colour.red())) 
      load[f'{ctx.author.id}']['bank']['amount'] += amount
      load[f'{ctx.author.id}']['balance'] -= amount
      if load[f'{ctx.author.id}']['bank']['amount'] == load[f'{ctx.author.id}']['bank']['maxamount']:
        load[f'{ctx.author.id}']['bank']['max'] = True
      with open("./dicts/economy.json", "w") as f:
        json.dump(load,f)  
      await ctx.reply(embed=discord.Embed(title="Deposited!", description=f"{self.emoji}{amount} Was deposited into your bank account!", color=Assests.color))  
  @commands.command(aliases=['with'])
  async def withdraw(self, ctx, amount:int):
    with open("./dicts/economy.json", "r") as f:
      load=json.load(f)
    if f"{ctx.author.id}" not in load:
        return await ctx.reply("You have not registered yet! Do r!start to get into our database.")  
    if load[f'{ctx.author.id}']['bank']['amount'] == 0:
      return await ctx.reply(embed=discord.Embed(title=f"Your bank is empty!", description=f"You were trying to withdraw your money while your bank is empty! Deposit money to it using r!dep <amount>"))
    if load[f'{ctx.author.id}']['bank']['amount'] - amount < 0:
      return await ctx.reply(embed=discord.Embed(title="Insefficunt funds!", description=f"You wanted to withdraw {self.emoji}{amount} from your bank, but you only have {load[f'{ctx.author.id}']['bank']['amount']}{self.emoji} in your bank!", color=discord.Colour.red())) 
    load[f'{ctx.author.id}']['balance'] += amount
    load[f'{ctx.author.id}']['bank']['amount'] -= amount
    load[f'{ctx.author.id}']['bank']['max'] = False
    with open("./dicts/economy.json", "w") as f:
      json.dump(load, f)
    await ctx.reply(embed=discord.Embed(title="Withdrawn!", description=f"{self.emoji}{amount} Was withdrawn from your bank, you now have {load[f'{ctx.author.id}']['bank']['amount']}{self.emoji} in your bank", color=Assests.color))

  @commands.command()
  @commands.cooldown(1, 60)
  async def beg(self, ctx):
    with open("./dicts/economy.json", "r") as f:
      load = json.load(f)
    if f"{ctx.author.id}" not in load:
        return await ctx.reply("You have not registered yet! Do r!start to get into our database.")  
    statements=["Get out of here you beggar!", "Oh you poor beggar, here's "]
    statement=random.choice(statements)
    embed=discord.Embed(title="")
    if statement == statements[0]:
      embed.title = "Your not lucky today"
      embed.color=discord.Colour.red()
      embed.description = f"\"{statement}\" You didnt gain any money :confused:"
    else:
      a=random.randint(0, 500)
      embed.title= "It is your day!"
      embed.color=Assests.color
      embed.description=f"\"{statement}{self.emoji}{a}\""  
      load[f'{ctx.author.id}']['balance'] += a
    await ctx.reply(embed=embed)

  @commands.command(aliases=['steal'])
  async def rob(self, ctx, *, user:discord.Member):
    with open("./dicts/economy.json", "r") as f:
      load = json.load(f)
    if f"{user.id}" not in load:
        return await ctx.reply(f"{user.mention} Have not been registered! Do r!start")
    if f"{ctx.author.id}" not in load:
      return await ctx.reply(f"You are not in our database! Do r!start")     
    if "padlock" in load[f'{user.id}']['inventory']:
      await ctx.reply(embed=discord.Embed(title=f"You were caught!", description=f"You tried to rob {user.mention}, but you notice that {user.name} has a huge padlock on his wallet, you pay him {self.emoji}250", color=discord.Colour.red()))
      if load[f'{ctx.author.id}']['balance'] > 250:
        load[f'{ctx.author.id}']['balance'] -= 250
      else:
        load[f'{ctx.author.id}']['balance'] -= load[f'{ctx.author.id}']['balance']  
      load[f'{user.id}']['balance'] += 250
      if load[f'{user.id}']['inventory']['padlock']['amount'] == 1:
        load[f'{user.id}']['inventory'].pop("padlock")
      else:
        load[f'{user.id}']['inventory']['padlock']['amount'] -= 1  
      file = open("./dicts/economy.json", "w")
      json.dump(load, file)
      return   
    if load[f'{user.id}']['balance'] < 500:
      return await ctx.reply(f"{user.mention} doesnt have atleast {self.emoji}500, not worth it man")  
    chances= [0, 1]
    f=random.randint(0, 750)
    foo = random.randint(0, load[f'{user.id}']['balance']-100)
    if random.randint(0, 1500) < 10 or load[f'{user.id}']['balance']-foo < 0:
      foo = load[f'{user.id}']['balance']
    fstatements= [f"{user.mention} Caught you while trying to eat his chips, you gave him {self.emoji}{f}", f"The police saw {user.mention} running after you, they fined you {self.emoji}{f}", f"{user.mention} Secretly knew you wanted to rob him/her, so he jumpscared you and stole {self.emoji}{f} from you", f"You stub your toe while running away from {user.mention}, you pay him/her {self.emoji}{f}"]
    res = random.choice(chances)
    embed=discord.Embed(title="")
    if res == 0:
      embed.title= f"You were caught!"
      embed.description=random.choice(fstatements)
      embed.color=discord.Colour.red()
      load[f'{ctx.author.id}']['balance'] -= f
      load[f'{user.id}']['balance'] += f
    else:
        size = ""
        if foo <= 500:
          size = "**Tiny**"
        elif foo in range(501, 1000):
          size = "**Small**"
        elif foo in range(1001, 1500):
          size = "**Decent**"
        elif foo in range(1501, 2000):
          size = "**Big**"
        else:
          size = "**Huge**"      
        if foo == load[f'{user.id}']['balance']:
          embed.title= f"You stole everything you can!"    
        else:
          embed.title=f"You stole a {size} portion!"
        embed.description=f"You stole {self.emoji}{foo} from {user.mention}"
        load[f'{user.id}']['balance'] -= foo
        load[f'{ctx.author.id}']['balance'] += foo
        embed.color=Assests.color
    with open("./dicts/economy.json", "w") as f:
      json.dump(load, f)    
    await ctx.reply(embed=embed)  

  @commands.group(aliases=['store'])
  async def shop(self, ctx):
    if ctx.invoked_subcommand == None:
       embed=discord.Embed(title="Shop",color=Assests.color)
       for i in self.shop:
         embed.add_field(name=self.shop.get(i).get('emoji') + i, value=f"**Price**: {self.shop.get(i).get('price')}\n**{self.shop.get(i).get('description')}**")
       await ctx.reply(embed=embed) 
  @shop.command(aliases=['purchase'])
  async def buy(self, ctx, item, amount:int=1):
    with open("./dicts/economy.json", "r") as f:
      load = json.load(f)
    if f"{ctx.author.id}" not in load:
        return await ctx.reply("You have not registered yet! Do r!start to get into our database.")  
    if item not in self.shop:
      return await ctx.reply(embed=discord.Embed(title="That item doesnt exist!", description=f"The item id `{item}` isnt any valid item in the shop!", color=discord.Colour.red()))
    else:
      if load[f'{ctx.author.id}']['balance']-self.shop.get(item)['price']*amount < 0:
        await emb(ctx, "Insefficunt funds!", f"You currently have {load[f'{ctx.author.id}']['balance']} in your wallet, but this item costs {self.emoji}{self.shop.get(item)['price']}", discord.Colour.red())
      else:
        load[f'{ctx.author.id}']['balance'] -= self.shop.get(item)['price']*amount
        if item in load[f'{ctx.author.id}']['inventory']:
          load[f'{ctx.author.id}']['inventory'][item]['amount'] += amount 
        else:
          load[f'{ctx.author.id}']['inventory'][item] = {"amount":amount, "id":item, "name":f"{self.shop.get(item).get('emoji')} {item}"}  
        await emb(ctx, "Purchased!", f"You paid {self.emoji}{self.shop.get(item)['price']*amount} to purchase {amount} {item}{'s' if amount >1 else ''}", Assests.color)
    with open("./dicts/economy.json", "w") as f:
      json.dump(load, f)    
  
  @commands.command(aliases=['inventory'])
  async def inv(self, ctx):
    with open("./dicts/economy.json", "r") as f:
      load = json.load(f)
    if f"{ctx.author.id}" not in load:
        return await ctx.reply("You have not registered yet! Do r!start to get into our database.")  
    else:
      embed=discord.Embed(title=f"{ctx.author}\'s inventory", color=Assests.color)
      for i in load[f'{ctx.author.id}']['inventory']:
        embed.add_field(name=load[f'{ctx.author.id}']['inventory'].get(i).get('name'), value=f"**Amount**: {load[f'{ctx.author.id}']['inventory'].get(i).get('amount')}\n**ID**: `{load[f'{ctx.author.id}']['inventory'].get(i).get('id')}`\n**Description**: {self.shop.get(i).get('description')}")   
      await ctx.reply(embed=embed) 

  @shop.command()
  async def add(self, ctx, id, emoji, price:int, *, description):
    if ctx.author.id == 761159873194491915 or ctx.author.id==473125594410909696:
      if id in self.shop:
        return await ctx.reply("That item is already in the shop!")
      with open("./dicts/economyshop.json", "r") as f:
        load=json.load(f)  
      load[id] = {"price":price, "description":description, "emoji":emoji}
      with open("./dicts/economyshop.json", "w") as f:
        json.dump(load, f)
      await ctx.reply(f"**Added `{id}` to the shop**\n> **ID**: {id}\n> **Description**: {description}\n> **Emoji**: {emoji}")
    else:
      await ctx.reply("No permissions.")
      
  @shop.command()
  async def remove(self, ctx, id):
    if ctx.author.id == 761159873194491915 or ctx.author.id==473125594410909696:
      if id not in self.shop:
        return await ctx.reply("That item != in the shop!")
      with open("./dicts/economyshop.json", "r") as f:
        load1=json.load(f)  
      load1.pop(id)
      with open("./dicts/economyshop.json", "w") as f:
        json.dump(load1, f)
      await ctx.reply(f"Removed `{id}` from the shop.") 
    else:
      await ctx.reply("No permissions")
      
  @shop.command()
  async def edit(self, ctx, id1, id, emoji, price:int, *, description):  
    if ctx.author.id == 761159873194491915 or ctx.author.id==473125594410909696:
      with open("./dicts/economyshop.json", "r") as f:
        load=json.load(f)
      if id1 not in load:
        return await ctx.reply("That item doesnt exist!")  
      await ctx.reply(f"**Edited**\n**__Before__**\n> **ID**: {id1}\n> **Description**: {load[id1].get('description')}\n> **Price**: {load[id1].get('price')}\n**__After__**\n> **ID**: {id1}\n> **Price**: {price}\n> **Description**: {description}")
      load.pop(id1)
      load[id] = {"price":price, "description":description, "emoji":emoji}
      with open("./dicts/economyshop.json", "w") as f:
        json.dump(load, f)
    else:  
      await ctx.reply("No permissions")
      

  @shop.command()
  async def info(self, ctx, id):
    if id in self.shop:
      await emb(ctx, f"Info about {id}", f"**ID**: {id}\n**Description**: {self.shop.get(id).get('description')}\n**Price**: {self.shop.get(id).get('price')}", Assests.color)    
    else:
      await ctx.reply("That item isnt in the shop!") 

  @commands.command(aliases=['rich', 'top', 'lb'])
  async def leaderboard(self, ctx):
    with open("./dicts/economy.json", "r") as f:
      load=json.load(f)
    a = []  
    for i in load:
      a.append(load.get(i))  
    a.sort(key=lambda g: g['balance'], reverse=True)
    embed=discord.Embed(title=f"Leaderboard", description="", color=Assests.color)
    for i in a[0:10]:
      embed.description += f"{i.get('username')} **>> {self.emoji}{i.get(('balance'))}**\n" 
    await ctx.reply(embed=embed)  
  
  @shop.command()
  async def sell(self, ctx, item, amount=1):
    with open("./dicts/economy.json", "r") as f:
      load = json.load(f)
    if f"{ctx.author.id}" not in load:
        return await ctx.reply("You have not registered yet! Do r!start to get into our database.")  
    if item not in load[f'{ctx.author.id}']['inventory']:
      return await emb(ctx, "You do not have that item!", f"You tried to sell {item}, but it isnt even in your inventory.", discord.Colour.red())
    load[f'{ctx.author.id}']['balance'] += self.shop.get(item).get('price')*amount
    if load[f'{ctx.author.id}']['inventory'][item]['amount']-amount < 0:
      return await emb(ctx, "Insefficunt items", "You do not have that much items!", discord.Colour.red())
    if load[f'{ctx.author.id}']['inventory'][item]['amount'] == 1:
        load[f'{ctx.author.id}']['inventory'].pop(item)
    else:  
        load[f'{ctx.author.id}']['inventory'][item]['amount'] -= amount
    file=open("./dicts/economy.json", "w")
    json.dump(load, file)
    await emb(ctx, "Sold!", f"You have sold the item {item} for {self.emoji}{self.shop.get(item).get('price')*amount}, you now have {self.emoji}{load[f'{ctx.author.id}']['balance']}", Assests.color)    



  @commands.command(aliases=['cf'])
  async def coinflip(self, ctx, bet=None):
    with open("./dicts/economy.json", "r") as f:
      load = json.load(f)
    if bet == None:
      bet = 500
    if bet == "max":
      if load[str(ctx.author.id)]['balance'] < 50000:
        bet = load[str(ctx.author.id)]['balance']
      else:  
        bet = 50000
    if load[str(ctx.author.id)]['balance']-int(bet) < 0:
      return await emb(ctx, "Insiffecunt funds!", f"You tried betting {bet} for a coinflip match, but you only have {load[str(ctx.author.id)]['balance']}!", discord.Colour.red())    
    if int(bet) < 500:
      return await emb(ctx, "Too low bet!", "The bet you input is too low! The minimum is 500", discord.Colour.red())
    if int(bet) > 50000:
      return await emb(ctx, "Too high bet!", "The bet you input is too high! The minimum is 50k", discord.Colour.red())  
    
    if f"{ctx.author.id}" not in load:
        return await ctx.reply("You have not registered yet! Do r!start to get into our database.")  
    a=random.choice(['heads', "tails"])    
    msg=await ctx.send(embed=discord.Embed(title=f"You are {a}", description=f"Choosing a random choice...."))  
    await asyncio.sleep(2)  
    b=random.randint(0, 100)
    if b < 50:
      load[f'{ctx.author.id}']['balance'] += int(bet)*2  
      embed=discord.Embed(title=f"{a}!", description=f"You were lucky and won the bet! You gained {self.emoji}{int(bet)*2}.", color=Assests.color)
      await msg.edit(embed=embed)
    elif b > 50:
      if load[f'{ctx.author.id}']['balance']-int(bet) < 0:
        load[f'{ctx.author.id}']['balance']-load[f'{ctx.author.id}']['balance']
      else: 
        load[f'{ctx.author.id}']['balance'] -= int(bet)
      embed=discord.Embed(title=f"{'heads' if a == 'tails' else 'tails'}..", description=f"You got unlucky and you lost the bet :/ You lost {self.emoji}{bet}", color=discord.Colour.purple())
      await msg.edit(embed=embed)  
    with open("./dicts/economy.json", "w") as f:
      json.dump(load, f)  

 

  @commands.command()
  async def use(self, ctx, item, amount:int):
    with open("./dicts/economy.json", "r") as f:
      load = json.load(f)
    if f"{ctx.author.id}" not in load:
        return await ctx.reply("You have not registered yet! Do r!start to get into our database.") 
    if item not in load[f'{ctx.author.id}']['inventory']:
      return await emb(ctx, "You do not have that item!", f"You tried to use {item}, but it isnt even in your inventory.", discord.Colour.red())      
    if item == "banknote":
      load[f'{ctx.author.id}']['bank']['max'] = False
      p = random.randint(5000, 10000)
      load[f'{ctx.author.id}']['bank']['maxamount'] += p*amount
      if load[f'{ctx.author.id}']['inventory']['banknote']['amount'] == 1:
        load[f'{ctx.author.id}']['inventory'].pop(item)
      else:  
        load[f'{ctx.author.id}']['inventory']['banknote']['amount'] -= 1*amount
      with open("./dicts/economy.json", "w") as f:
        json.dump(load, f)  
      await emb(ctx, f"Used banknote", f"Used {item} and got extra bank space, current bank: {load[f'{ctx.author.id}']['bank']['amount']}/{load[f'{ctx.author.id}']['bank']['maxamount']}", Assests.color)

  @commands.command(aliases=['give'])
  async def pay(self, ctx, user:discord.Member, amount:int):
    with open("./dicts/economy.json", "r") as f:
      load = json.load(f)
    if f"{user.id}" not in load or f"{ctx.author.id}" not in load:
      return await ctx.reply(f"Either you or {user.mention} is not in our database! Do r!start")
    if load[str(ctx.author.id)]['balance'] - amount <0:
      return await emb(ctx, "Insefficunt funds!", f"You tried paying {user.mention} {self.emoji}{amount}, But you dont have that amount!", discord.Colour.red())
    load[str(ctx.author.id)]['balance'] -= amount
    load[str(user.id)]['balance'] += amount
    await emb(ctx, "Paid!", f"You payed {user.mention} {self.emoji}{amount}! You now have {self.emoji}{load[str(ctx.author.id)]['balance']}", Assests.color )  
    file=open("./dicts/economy.json", "w")
    json.dump(load, file)


          

      


      




        

        











       
        





      

         







def setup(bot):
  bot.add_cog(Economy(bot))  