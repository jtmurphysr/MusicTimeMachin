import os
from dotenv import load_dotenv

class EnvConfig:
    """
    A configuration class for managing environment variables.
    
    This class loads environment variables from a .env file and provides
    convenient access to them through properties and dictionary-like access.
    """
    def __init__(self):
        """
        Initialize the EnvConfig class and load environment variables from .env file.
        
        Raises:
            EnvironmentError: If the .env file is not found or cannot be read.
        """
        load_result = self._load_env()
        if not load_result:
            raise EnvironmentError(".env file not found or unreadable.")

    def get(self, key, default=None):
        """
        Get an environment variable by key.
        
        Args:
            key (str): The name of the environment variable.
            default (Any, optional): The default value to return if the variable is not found.
                                    Defaults to None.
        
        Returns:
            str: The value of the environment variable.
            
        Raises:
            KeyError: If the environment variable is not found and no default is provided.
        """
        value = os.getenv(key, default)
        if value is None:
            raise KeyError(f"Required environment variable '{key}' not found and no default provided.")
        return value

    def _load_env(self):
        """
        Load environment variables from .env file.
        
        Returns:
            bool: True if the .env file was loaded successfully, False otherwise.
        """
        return load_dotenv()

    @property
    def spotify_client_id(self):
        """Get the Spotify client ID from environment variables."""
        return self.get("SPOTIFY_CLIENT_ID")
    
    @property
    def spotify_client_secret(self):
        """Get the Spotify client secret from environment variables."""
        return self.get("SPOTIFY_CLIENT_SECRET")
    
    @property
    def spotify_redirect_uri(self):
        """Get the Spotify redirect URI from environment variables."""
        return self.get("SPOTIFY_REDIRECT_URI")
    
    def __getitem__(self, key):
        """
        Allow dictionary-like access to environment variables.
        
        Args:
            key (str): The name of the environment variable.
            
        Returns:
            str: The value of the environment variable.
        """
        return self.get(key)

    def __getattr__(self, key):
        """
        Allow attribute-like access to environment variables.
        
        This method is called when an attribute is not found through normal attribute lookup.
        It attempts to find an environment variable with the same name.
        
        Args:
            key (str): The name of the environment variable.
            
        Returns:
            str: The value of the environment variable.
            
        Raises:
            AttributeError: If the environment variable is not found.
        """
        try:
            return self.get(key)
        except KeyError as e:
            raise AttributeError(e)

# Usage example:
# from env_variables import EnvConfig
# config = EnvConfig()
# api_key = config.spotify_client_id