import os
from datetime import datetime
import subprocess
from PIL import Image

TEMPORARY_DIR_VAR = "TEMP_FOLDER"

command = 'grim "{filepath}" && notify-send "hyprwhisper" "Screenshot taken"'
image_size = (1280, 720)

def get_screenshot():
    """Get a recent screenshot of the user's computer.

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
