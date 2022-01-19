import discord
from dotenv import load_dotenv
from datetime import datetime
import os
from command_request import new_command
from python_vlookup import python_vlookup
import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from timers import *
import random


# Toggles
debug_mode = True
accepting_responses = False
dev_override = True
dev = ['mauberries#0001','ohiotexas#9559']


# Loading .env
load_dotenv()

# Defining bot process
bot = discord.Client()

# Keeping this here in the case dotenv not being used
# token = str(os.getenv('token'))


# Event to add commands to bot from discord
@bot.event
async def on_message(message):

    timestamp = datetime.now().strftime("%m/%d/%Y-%H:%M:%S") + ' ... '
    author = message.author
    # Parsing message to set command as word in between first underscore and next space
    try:
        command = message.content.split("_")[1].split(" ")[0].replace('?','')
    except:
        command = message.content.split(' ')[0]


# Console messages
    if message.content.find('_') != -1:
        # Exiting if bot
        if message.author.bot:
            return
        else:
            print(f'{timestamp}{author} executed [{command}]. ')


# _add command
    if message.content.find('_add') != -1:
        # Exiting if author is a bot
        if message.author.bot:
            return

        # Checking if accept responses are on for new commands
        if accepting_responses and message.content[4:] == '_add' or str(message.author) in dev:
            response = new_command(message)
            if response != None:
                await message.channel.send(response)

        # Responding in discord if requests are turned off
        else:
            if message.content[4:] == '_add':
                await message.channel.send('New command requests turned off. rekt')
        return


# responding to all commands within commands.csv
    if message.content.find('_') != -1:
        # Exiting if author is a bot
        if message.author.bot:
            return

        # Retrieving and creating a list of commands from commands.csv
        with open('commands.csv', encoding='utf8') as csv_file:
            commands = [row.split(',')[0] for row in csv_file]

        # Checking if parsed command is in list of commands, responding with response on csv if so
        if command in commands:
            # BLANK ROWS IN CSV FILE WILL RESULT IN 'list index out of range' ERROR!
            await message.channel.send(python_vlookup.vlookup(command, 'commands.csv',2).replace('///n','\n'))


# 'nice' response if message contains '69' except if the message contains the below text
    if message.content.find("69") != -1:
        if message.content.find("cdn.discordapp.com") != -1:
            await message.channel.send("nice.")
            print('')
        else:
            pass


# _timer command
    if message.content.find("_timer") != -1:
        await message.channel.send(timer_parse(message.content, str(message.author.id)))


# _pid command
    if message.content == ("_pid"):
        await message.delete()
        await message.channel.send("ᵖᶦᵈ")
        await message.channel.send(read_data('dab'))


# _fact command
    if message.content == ("_fact"):
        content = urllib.request.urlopen("https://fungenerators.com/random/facts/animal/sheep")
        read_content = content.read()
        soup = BeautifulSoup(read_content, "html.parser")
        pALL = soup.find_all("h2")
        fact_raw = pALL[0]
        fact = fact_raw.text
        fact_peep = fact.replace("Sheep", "Peepy Sheepy")
        fact_final = fact_peep.replace("(Animal  > Peepy Sheepy  )", "")
        await message.channel.send(fact_final)


# responding with chips gif if chipsncrackr is mentioned
    if message.content.find(os.getenv('ID_chipsncrackr')) != -1:
        await message.channel.send("https://tenor.com/view/chips-and-dip-snacks-chips-dip-snack-gif-16658490")


# responding to reddit links with content only message so it will preview in discord
    if message.content.find("reddit.com") != -1:
        #print("reddit message received")
        content = Request(str(message.content)+".json", headers={"User-Agent": "Mozilla/5.0"})
        read_content = urlopen(content).read()
        print(read_content)
        soup = BeautifulSoup(read_content, "html.parser")
        #print(soup)
        if "fallback_url" in str(soup):
            partitions = str(soup).partition("{\"fallback_url\": \"")
            pre_trimmed = partitions[1] + partitions[2]
            pre_trimmed = pre_trimmed.replace("{\"fallback_url\": \"","")
            partitions = pre_trimmed.partition("\"")
            post_trim = partitions[0]
            await message.channel.send(post_trim)
        elif "url_overridden_by_dest" in str(soup):
            partitions = str(soup).partition("\"url_overridden_by_dest\": \"")
            pre_trimmed = partitions[1] + partitions[2]
            pre_trimmed = pre_trimmed.replace("\"url_overridden_by_dest\": \"","")
            partitions = pre_trimmed.partition("\"")
            post_trim = partitions[0]
            await message.channel.send(post_trim)
        else:
            return


# Responds with meme capitalized text
    if message.content[:2] == '_ ':
        meme_response = []
        for char in message.content[2:]:
            uppercase = random.randint(0,1)
            if char == ' ':
                continue
            elif uppercase == 0:
                try:
                    meme_response.append(char.lower())
                except:
                    meme_response.append(char)
            else:
                try:
                    meme_response.append(char.upper())
                except:
                    meme_response.append(char)
        await message.channel.send(''.join([str(elem) for elem in meme_response]))


# Sending message from the bot if sent in bot console channel
    if str(message.channel) == 'console':
        channel_send = bot.get_channel(771057112867405886)
        if message.content[:4] == '_del':
            await channel_send.send(message.content[4:])
            time.sleep(1)
            await channel_send.purge(limit=1)
        else:
            await channel_send.send(message.content)
        print(message.content[:4])



bot.run(str(os.getenv('token')))