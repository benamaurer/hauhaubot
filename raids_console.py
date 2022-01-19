import discord
import sys
from dotenv import load_dotenv
import os


# Loading .env
load_dotenv()


#Prints information to the console including: sender, command run, and time
def log_sender(command, sender):
    print("---" + str(sender) + " ran (" + command + ") at " + str(time.strftime('%H:%M:%S_%m/%d/%y')) + "---")


line_break = "-------------------------------------------------------------------------\n "
token = str(os.getenv('token'))
client = discord.Client()
guild_ID = str(os.getenv('guild_id'))


@client.event
async def on_ready():
    for channel in client.get_guild(guild_ID)
    print("Message event handler running, type \"_logout\" to exit.")
    while True:
        print(">:")
        cli_message = input()

        if cli_message == "_logout":
            print("script stopping...")
            sys.exit()

        if cli_message == "_channels"
            for channel in channels:
                print(channel)

        message_split = cli_message.split()[1:]
        message_out = " ".join(message_split)
        channel_select = cli_message.split()[0]
        print("Sending:    \"" + str(message_out) + "\"    to (" + str(channel_select) + ") channel, confirm?  (\"n\" to cancel)")
        confirm = input()
        if str(confirm) == "n":
            break
        tob = client.get_channel(758032791496687718)
        bot = client.get_channel(771131702453600277)
        test = client.get_channel(771057112867405886)

        try:
            if channel_select == "test":
                await test.send(str(message_out))
                print("sent")
                print(line_break)
            elif channel_select == "tob":
                await main.send(str(message_out))
                print("sent")
                print(line_break)
            elif channel_select == "bot":
                await bot.send(str(message_out))
                print("sent")
                print(line_break)
            else:
                print("invalid channel.")
                print(line_break)
                return
        except:
            print("Unknown exception, continuing...")
            return


client.run(token)