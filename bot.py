#bot.py

#V.4
#Now Supports !kaey for insults
#Words now stored in seperate file
#Now includes !attack - insults on attacks
#Logging now supported
#Now Supports !timecheck iPM to display time zones with deafult time to Male'
#Now deletes insult aurthor
#Now supports plan making
#Now supports covid

import os
import random
from discord.ext import commands
import discord
from dotenv import load_dotenv
from datetime import datetime,timedelta
import logging
import re
import requests
from bs4 import BeautifulSoup

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
    await ctx.message.delete()
    
    
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
       
plan = []
planmembers = []

@bot.command(name='plan')
async def makelist(ctx, key, *arg):
    
    member = ctx.message.author
    sender = member.name

    def showmessage():
        message = plan[0]
        np = len(planmembers)
        membersPrint = (', '.join(planmembers))
       
        return f'''```
{message}

Players joined ({np}):
{membersPrint}
```'''
    if len(key)==0:
        await ctx.send('type in <!plan help> to get help')
        
    if key == 'make':
        plan.clear()
        planmembers.clear()
        await ctx.send(f'{sender} created a plan!')
        if sender not in planmembers:
            planmembers.append(sender)
        message = (''.join(*arg))
        plan.append(message)
        await ctx.send(showmessage())
        await ctx.message.delete()

    elif key == 'in':
        if len(plan) == 0:
            await ctx.send('There are no plans. :(')
            
        elif sender in planmembers:
            await ctx.send('You have already joined the plan')
            
        elif sender not in planmembers:
            planmembers.append(sender)
            await ctx.send(showmessage())
            await ctx.message.delete()

    elif key == 'out':
        if len(plan) == 0:
            await ctx.send('There are no plans. :(')
            
        elif sender in planmembers:
            planmembers.remove(sender)
            await ctx.send(f'{sender} pussied out')
            await ctx.message.delete()

    elif key == 'show':
        await ctx.send(showmessage())
                
    elif key == 'delete':
        await ctx.message.delete()
        plan.clear()
        planmembers.clear()

    elif key == 'help':
        await ctx.send('''You can <!plan make "faahana at 8"> (plan message must inside double quotaion) to make or,
<!plan in> to join current plan, or <!plan out> to pussy out''')
              
@bot.command(name='covid')
async def insulter(ctx, country):
    
    url = "https://www.worldometers.info/coronavirus/"
    res = requests.get(url).text
    soup = BeautifulSoup(res,features="html.parser")

    data = []

    table = soup.find('table')
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
              
    # print(type(data))

    searched = next(x for x in data if country in x)

    country = (searched[0])
    totalcase = (searched[1])
    newcase = (searched[2])
    
    await ctx.send(f'{country}\nTotal Cases: {totalcase}\nNew Cases: {newcase}')
    
bot.run(TOKEN)

