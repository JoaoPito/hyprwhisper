def escape_characters(text: str):
    escaped_string = text.replace("\\", "\\\\")
    escaped_string = escaped_string.replace('"', '\\"')
    escaped_string = escaped_string.replace('$', '\\$')
    escaped_string = escaped_string.replace('`', '\\`')
    return escaped_string