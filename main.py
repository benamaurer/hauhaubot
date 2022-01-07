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

# Toggles
debug_mode = True
accepting_responses = False
dev_override = True
dev = ['mauberries#0001','ohiotexas#9559']

# Loading .env
load_dotenv()

# Defining bot process
bot = discord.Client()

token = str(os.getenv('token'))


# Event to add commands to bot from discord
@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.content.find('_add') != -1:
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


    if message.content.find('_') != -1:
        if message.author.bot:
            return
        command = message.content[1:]
        with open('commands.csv', encoding='utf8') as csv_file:
            commands = [str(row.split(',')[0]) for row in csv_file]
        if command in commands:
            await message.channel.send(str(python_vlookup.vlookup(command, 'commands.csv',2)))
        return


    if message.content.find("69") != -1:
        if message.content.find("cdn.discordapp.com") != -1:
            await message.channel.send("nice.")
        else:
            pass


    if message.content.find("_timer") != -1:
        await message.channel.send(timer_parse(message.content, str(message.author.id)))


    if message.content == ("_pid"):
        await message.delete()
        await message.channel.send("ᵖᶦᵈ")
        await message.channel.send(read_data('dab'))


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


    if message.content.find(os.getenv('ID_chipsncrackr')) != -1:
        await message.channel.send("https://tenor.com/view/chips-and-dip-snacks-chips-dip-snack-gif-16658490")


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

# @bot.event

bot.run(str(os.getenv('token')))