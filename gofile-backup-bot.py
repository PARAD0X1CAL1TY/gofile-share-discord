import discord
import asyncio
from threading import Thread
from discord import app_commands
from datetime import datetime
with open('token.txt', 'r') as file:
    TOKEN = file.read().replace('\n', '')
    if(TOKEN != ""):
        print("TOKEN loaded.")

with open('guild.txt', 'r') as file:
    GUILD = int(file.read().replace('\n', ''))
    print("GUILD: " + str(GUILD))

with open('channel.txt', 'r') as file:
    UPDATES = int(file.read().replace('\n', ''))
    print("Updates channel: " + str(UPDATES))


class backupInfo():
    password: str
    link: str
    hash: str
    fileSize: str

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
now = datetime.now()
sd_updates = client.get_channel(UPDATES)
isBackupRunning = False

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await tree.sync(guild=discord.Object(id=GUILD))
    print("Ready!")
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
###### END OF SETUP GARBAGE


# Backup the server
@tree.command(name = "backup", description = "Create a snapshot in time of the world", guild=discord.Object(GUILD)) 
async def backup(interaction: discord.Interaction):
    await backupHandler(interaction)

async def backupHandler(interaction: discord.Interaction):
    print(interaction.user)
    await interaction.response.send_message(interaction.user.mention + " started a backup job for the world.")
    thread = Thread(target = multiThreadHandler, args = ())
    thread.start()

def multiThreadHandler():
    backupInfo = completeBackup()
    asyncio.run_coroutine_threadsafe(sendUpdateMessageToChannel(backupInfo),client.loop)

def completeBackup():
    backupOutput = backupInfo()
    #do the backup stuff here
    from subprocess import Popen
    p = Popen(['./encryptandsend.sh'], shell=True)
    p.wait()

    file = open('./encryptandsendinfo.txt', 'r').readlines()
    backupOutput.password = file[0]
    backupOutput.link = file[1]
    backupOutput.hash = file[2]
    backupOutput.fileSize = file[3]
    return backupOutput

async def sendUpdateMessageToChannel(backupInfo):
    channel = client.get_channel(UPDATES)  
    await channel.typing()  
    embedLink = discord.Embed()
    embedLink.description = "[Download Server](" + backupInfo.link + ")\n [SHA256 Tool](https://emn178.github.io/online-tools/sha256_checksum.html)"
    await channel.send(embed=embedLink, content="Backup complete!\n\n Archive link: ``" + backupInfo.link + "``\n" + "Archive size: ``" + backupInfo.fileSize + "``\n" + "Password: ``" + backupInfo.password + "``\n" + "SHA256: ``" + backupInfo.hash + "``")

async def sendImages(user, sdImage):
    await discord.User(user).send("Image gen done.")
        
client.run(TOKEN)


