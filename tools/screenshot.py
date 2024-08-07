import os
from datetime import datetime
import subprocess
from PIL import Image

TEMPORARY_DIR_VAR = "TEMP_FOLDER"

command = 'grim "{filepath}" && notify-send "hyprwhisper" "Screenshot taken"'
image_size = (1920, 1080)

def get_screenshot():
    """Get a screenshot of the user's computer. The screenshot will be available to you after executing.
    Use this whenever the user mentions about something that is on their screen or when you need to see what he/she is talking about.

    Returns:
        The status of the command.
    """
    filepath = os.path.join(os.getenv(TEMPORARY_DIR_VAR), f"temp_{datetime.now().strftime("%d%m-%H%M%S")}.png")
    final_command = command.format(filepath=filepath)
    result = subprocess.run(final_command, shell=True, capture_output=True, text=True)
    
    if result.stderr:
        return (f"Error taking screenshot.\n({result.stderr})", [])
    
    img = Image.open(filepath)
    resized_img = img.resize(image_size)
    resized_img.save(filepath)
    
    return ("Screenshot taken.", [filepath])
