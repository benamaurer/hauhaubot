debug_mode = False
from datetime import datetime


def new_command(message):

    try:
        # Parsing incoming message to get new bot command
        new_command = message.content[4:].split(',')[0]
        for character in new_command:
            if new_command[0] == ' ':
                new_command = new_command[1:]

        # Parsing incoming message to get bot response
        new_response = message.content[4:].split(',')[1]
        for character in new_response:
            if new_response[0] == ' ':
                new_response = new_response[1:]

    except:
        return f'Unable to parse message: {message.content}, ensure it is formatted correctly.'

    # Debug point
    if debug_mode:
        print(f'new command:{new_command}\nnew response: {new_response}')

    with open('commands.csv', encoding='utf8') as csv_file:
        command_check = [str(row.split(',')[0]) for row in csv_file]

    # Printing command list
    if debug_mode:
        for command in command_check:
            print(command)

    # Checking if command already exists and responding in discord then exiting on_message
    if new_command in command_check:
        print('Command already exists.')
        return f'{new_command} already exists or error with request format.'

    # If command found to not exist above, creating new command in csv and responding with new command
    else:
        with open('commands.csv', 'a') as csv_file:
            csv_file.write(
                f'\n{new_command},{new_response},{message.author},{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}')
        return f'**Creating new command with:**\n    command = _{new_command}\n    response = {new_response}\n    creator = {message.author}\n\n    *created at {datetime.now().strftime("%m/%d/%Y-%H:%M:%S")}'

    # # Searching for command in commands.csv
    # try:
    #     with open('commands.csv', encoding='utf8') as csv_file:
    #         command_check = [str(row.split(',')[0]) for row in csv_file]
    #
    #     # Printing command list
    #     if debug_mode:
    #         for command in command_check:
    #             print(command)
    #
    #     # Checking if command already exists and responding in discord then exiting on_message
    #     if new_command in command_check:
    #         print('Command already exists.')
    #         return message.channel.send(f'{new_command} already exists or error with request format.')
    #
    #     # If command found to not exist above, creating new command in csv and responding with new command
    #     else:
    #         with open('commands.csv', 'a') as csv_file:
    #             csv_file.write(
    #                 f'\n{new_command},{new_response},{message.author},{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}')
    #         return message.channel.send(
    #             f'**Creating new command with:**\n    command = _{new_command}\n    response = {new_response}\n    creator = {message.author}\n\n    *created at {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}')
    #
    # # Exception if issue with command lookup or creating command
    # except:
    #     print(f'Exception while creating {new_command}!')
    #     return f'Unable to find old or create the command [{new_command}], please check formatting of your request, it should be _add <prefix>, <bot response>.'


if __name__ == '__main__':
    pass