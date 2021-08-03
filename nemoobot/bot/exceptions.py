class WSCommandException(Exception):
    """
    Web socket commands exceptions
    """


class SettingsNotFound(WSCommandException):
    """
    Raises then settings for bot initialization not found
    """
