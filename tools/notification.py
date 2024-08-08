import subprocess

from tools.cmd_utils import escape_characters

command = 'notify-send "hyprwhisper" "{message}"'

def notify(text: str):
    """Send a notification to the user.
    Use this whenever you want to alert the user about something important.

    Args:
      text: The content that will be shown to the user.

    Returns: The status of the command.
    """
    escaped_text = escape_characters(text)
    result = subprocess.run(command.format(message=escaped_text), shell=True, capture_output=True, text=True)
    if result.stderr:
        print(f"Error issuing notification\n({result.stderr})")
        return (f"Error issuing notification\n({result.stderr})", [])
    return ("Notification sent",  [])