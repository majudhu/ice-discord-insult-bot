#bot.py

#V.2
#python C:\Users\Lola\Documents\Pythonex\Bot-testing\bot.py
#Now Supports !kaey for insults
#Words now stored in seperate file
#Now includes !attack - insults on attacks
#Logging now supported
#Now Supports !timecheck iPM to display time zones with deafult time to Male'

import os
import random
from discord.ext import commands
import discord
from dotenv import load_dotenv
from datetime import datetime,timedelta
import logging
import re

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - (message)s')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

       
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print (f'{bot.user.name} has connected to Discord!')

@bot.command(name='kaey', help = 'Type in !kaey for dhiv insults!')
async def insulter(ctx, *arg):
   
    f = open('insults.txt','r')
    
    WORDS = []
    for word in f.readlines():
        WORDS.append(word.strip())
    newinsult = []
    for i in range(random.randint(2,5)):
        if random.choice(WORDS) not in newinsult:
            newinsult.append(random.choice(WORDS))

    finalinsult = ' '.join(newinsult)
    
    allfalhuverin = []
    
    Aurthor = (ctx.message.author)
    #sender = Smember.split(' ', 1)[0]
    
    #for members in ctx.author.text.channel.members
    for member in ctx.guild.members:
        for role in member.roles:
            if role.name == "Falhuverin":
                if member != Aurthor:
                    allfalhuverin.append(member.id)

    RandomFalhuveriya = random.choice(allfalhuverin)
    
    def respond():
        if len(arg) < 2:
            return f'{finalinsult}'

        elif '-t' in arg:
            if arg[1] == 'random':
                return f'<@!{RandomFalhuveriya}> kaey thee {finalinsult}'
    
            elif arg[1] != 'random':
                logging.info('target given')
                target = arg[1]
                return f'{target} kaey thee {finalinsult}'
            else:
                pass
        else:
            return f'{finalinsult}.'
            print(arg)

    respond = respond()
    
    await ctx.send(respond)
    
    
@bot.command(name='timecheck', help='Look up times')
async def time(ctx, time_str, *arg):
    
    maletime = datetime.strptime(time_str, '%I%p')

    if arg == 'mle' or len(arg) == 0:
        maletime = maletime

    elif arg == 'mly' or arg == 'malay':
        malaydelta = timedelta(hours = +4)
        maletime = maletime - malaydelta
        
    elif arg == 'uk':
        UKdelta = timedelta(hours = -4)
        maletime = maletime - UKdelta

    malaydelta = timedelta(hours = +4)
    malaytime = maletime + malaydelta

    UKdelta = timedelta(hours = -4)
    UKtime = maletime + UKdelta

    MLE = maletime.strftime("%I%p")
    MLY = malaytime.strftime("%I%p")
    UK = UKtime.strftime("%I%p")
    
    #print(maletime.time())
    response = (f'''
```json
"{UK}  UK"
"{MLE} MLE"
"{MLY} MLY"
```
''')
    await ctx.send(response)

@bot.command(name='attack')
async def insulter(ctx):
    
    member = str(ctx.message.author)
    sender = member.split(' ', 1)[0]
    

    insult = ['ee enme attack kurevey o! loool',
              'thidhen attack ehtha?',
              'goru hendiyas maa rangalhu vanae!',
              'maithiri vebala',
              'gui laabala kaley, gui',
              "didn't you know, like Einstein said every action and reaction egual and opposite ok"
              "kaley saeedhaa ah dhekkenytha",
              'bidi olhaabala, bidi',
              'kaey mammayah attack kohbala'
        ]
    finalinsult = random.choice(insult)
    
    if (random.randint(1,3)) == 1:
        await ctx.send(f'@{sender} {finalinsult}')
    
bot.run(TOKEN)

