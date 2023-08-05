from ..message import Message
import subprocess


def send_command_client(args):
    command = args['send'] 
    if args['result']:
        title = "result"
    else:
        title = None

    message = Message(title=title, content=command)
    return message


def send_command_server(mess):
    command = ' '.join(mess.get_content()) 
    result = subprocess.run(command, shell=True, 
            stdout=subprocess.PIPE)

    if mess.get_title() == "result": 
        return result.stdout.decode('utf-8')
    else:
        return ""

