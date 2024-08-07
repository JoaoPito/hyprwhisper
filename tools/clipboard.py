import subprocess

PASTE_CMD = 'wl-paste'
COPY_CMD = 'wl-copy'

def paste_from_clipboard():
    """Get the contents of the computer's clipboard.
    Use this whenever the user talks about something that he/she has copied or sent to you.

    Returns:
        The contents of the clipboard in text form.
    """
    process = subprocess.run([PASTE_CMD], stdout=subprocess.PIPE)
    if process.stderr:
        return (f"Error using clipboard.\n({process.stderr})", [])
    text = process.stdout.decode('utf-8').strip('\n')
    return (text, None)

def copy_to_clipboard(text: str):
    """Copy some text to the computer's clipboard.
    Use this whenever the user wants you to write or send something to her/him.

    Args:
      text: The content that will be sent to the user.

    Returns: The status of the command.
    """

    command = f'echo "{text}" | {COPY_CMD}'
    process = subprocess.run([command], stdout=subprocess.PIPE)
    if process.stderr:
        return (f"Error using clipboard.\n({process.stderr})", [])
    return ("Copied to clipboard.", None)