from dataclasses import dataclass
from data_logging.discord.api_facade.types import DiscordUserID

@dataclass
class DiscordUser:
    """
    Represents discord user https://discord.com/developers/docs/resources/user#user-object
    """
    
    id: DiscordUserID
    username: str
    
    def __init__(self, user_object_response: dict) -> None:
        """Creates DiscordUser object from discord user object api response.

        Args:
            user_object_response (dict): https://discord.com/developers/docs/resources/user#user-object
        """
        
        self.id = DiscordUserID(user_object_response['id'])
        self.username = user_object_response['username']