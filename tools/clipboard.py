import subprocess

from tools.cmd_utils import escape_characters
from tools.notification import notify

PASTE_CMD = 'wl-paste'
COPY_CMD = 'echo "{text}" | wl-copy'

def paste_from_clipboard():
    """Get the contents of the computer's clipboard.
    Use this whenever the user talks about something that he/she has copied or sent to you.

    Returns:
        The contents of the clipboard in text form.
    """
    process = subprocess.run([PASTE_CMD], stdout=subprocess.PIPE, shell=True)
    if process.stderr:
        return (f"Error using clipboard.\n({process.stderr})", [])
    text = process.stdout.decode('utf-8').strip('\n')
    
    notify("Got text from clipboard.")
    return (text, None)

def copy_to_clipboard(text: str):
    """Copy some text to the computer's clipboard.
    Use this whenever the user wants you to write or send something to her/him.

    Args:
      text: The content that will be sent to the user.

    Returns: The status of the command.
    """

    command = COPY_CMD.format(text=escape_characters(text))
    process = subprocess.run([command], stdout=subprocess.PIPE, shell=True)
    
    notify("Put text into clipboard.")
    if process.stderr:
        return (f"Error using clipboard.\n({process.stderr})", [])
    return ("Copied to clipboard.", None)

