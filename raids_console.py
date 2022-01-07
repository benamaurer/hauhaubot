#---------------------------------------------------------------------------------------------------------------
#Importing packages
import discord
import sys


#---------------------------------------------------------------------------------------------------------------
#Loading information from reference files

#Obtaining token/guild ID
def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


# #Reading bot-specific data file and returning data=[return value]
# def read_bcf(data):
#     with open("bcf_data.txt", "r") as f:
#         lines = f.readlines()
#         for line in lines:
#             if str(data) in str(line.strip()):
#                 return (str(line.split("=")[1].strip()))



#Prints information to the console including: sender, command run, and time
def log_sender(command, sender):
    print("---" + str(sender) + " ran (" + command + ") at " + str(time.strftime('%H:%M:%S_%m/%d/%y')) + "---")



#---------------------------------------------------------------------------------------------------------------
#Initial variable declaration


line_break = "-------------------------------------------------------------------------\n "
token = read_token()
client = discord.Client()
# guild_ID = int(read_bcf("guild_ID"))



#---------------------------------------------------------------------------------------------------------------
#Discord event handler


@client.event
async def on_ready():
    id = 717449642333306880
    print("Message event handler running, type \"_logout\" to exit.")
    while True:
        print(">:")
        cli_message = input()

        if cli_message == "_logout":
            print("script stopping...")
            sys.exit()

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