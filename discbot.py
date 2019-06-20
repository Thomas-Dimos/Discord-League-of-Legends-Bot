import discord
from pymongo import MongoClient

champions = []

#---------MongoDB Vars---------#
client = MongoClient("enter mongodb client here")
db = client.get_database('champions')
records = db.champion_runes

#---------Discord Vars---------#
TOKEN ='enter your discord token  here'
client = discord.Client()


@client.event
async def on_message(message):
    channel = message.channel
    
    if message.author == client.user:# we do not want the bot to reply to itself
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await channel.send(msg)
        return
    elif message.content.startswith('!victory'):
        msg = '{0.author.mention} is doing the victory dance'.format(message)
        embed = discord.Embed(title = '', description = msg)
        embed.set_image(url = 'https://media1.tenor.com/images/26ff317c89f308d16cd5b9c14dd6b584/tenor.gif')
        await message.channel.send(content = None, embed = embed)
        return


    if message.content.startswith('!'):
        token = message.content.split()
        token = token[0].replace('!','').rstrip().lower()

        for champion in champions:
            if token == 'j4':
                token = 'jarvan'
            if token in champion:
                record = records.find_one({'name': champion})
                try:
                    msg = styleTheMessage(record)
                except:
                    msg= 'Currently not enough data in champion.gg!'
                await channel.send(msg)
                return

        await channel.send("command not found")
        return


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def styleTheMessage(record):
    combined_runes = ''
    runes = record['primary_build'].split(',')
    runes[0] = '\n**'+runes[0]+'**' #make the Sorcery, Inspiration etc. bold
    runes[4] = runes[4]+'\t' #split primary runes with secondary
    runes[5] = '\n**'+runes[5]+'**' #same as above ^
    runes[8] = '\n**Stat Runes**\n'+runes[8] #split secondary runes with stat runes
    for rune in runes:
        combined_runes = (combined_runes + rune + '\n')
    msg = ('\n**'+record['name'].upper()+'**'+'\n'+combined_runes)

    return msg

def getChampionsFromCsv():
    global champions

    with open ('champions.csv', 'r') as file:
        for line in file:
            champions.append(line.rstrip().lower())

getChampionsFromCsv()
client.run(TOKEN)

