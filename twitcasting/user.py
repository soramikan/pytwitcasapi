import urllib, base64, json
import urllib.request, urllib.error
from urllib.parse import urlencode
from typing import Optional, Never

from .exceptions import ERROR_CODES_DICT

class User:
    """
    User class for TwitCasting API.
    """

    def __init__(self, id: str, screen_id: str, name: str, image: str, profile: str, level: int, is_live: bool, last_movie_id: Optional[str] = None) -> None:
        """
        Initialize the User object.

        Args:
            id (str): User ID.
            screen_id (str): Screen ID.
            name (str): User name.
            image (str): User icon URL.
            profile (str): User profile.
            level (int): User level.
            last_movie_id (Optional[str]): Last movie ID. Default is None.
            is_live (bool): Whether the user is live or not.
        """
        self.id = id
        self.screen_id = screen_id
        self.name = name
        self.image = image
        self.profile = profile
        self.level = level
        self.last_movie_id = last_movie_id
        self.is_live = is_live

    def __repr__(self) -> str:
        """
        String representation of the User object.

        Returns:
            str: String representation of the User object.
        """
        return f"User(id={self.id}, screen_id={self.screen_id}, name={self.name}, image={self.image}, profile={self.profile}, level={self.level}, last_movie_id={self.last_movie_id}, is_live={self.is_live})"
    
    def __str__(self) -> str:
        """
        String representation of the User object.

        Returns:
            str: String representation of the User object.
        """
        return f"User: {self.name} (ID: {self.id})"

    def __eq__(self, other: object) -> bool:
        """
        Check equality of two User objects.

        Args:
            other (object): Other object to compare.

        Returns:
            bool: True if equal, False otherwise.
        """
        if not isinstance(other, User):
            return NotImplemented
        return self.id == other.id and self.screen_id == other.screen_id and self.name == other.name and self.image == other.image and self.profile == other.profile and self.level == other.level and self.last_movie_id == other.last_movie_id and self.is_live == other.is_live

class App:
    """
    App class for TwitCasting API.
    """

    def _validate(self) -> None:
        """
        Validate the App object.

        Raises:
            ValueError: If any of the required attributes are missing.
        """
        if not self.client_id or not self.name or not self.owner_user_id:
            raise ValueError("client_id, name, and owner_user_id are required.")

    def __init__(self, client_id: str, name: str, owner_user_id: str) -> None:
        """
        Initialize the App object.

        Args:
            client_id (str): Client ID.
            name (str): App name.
            owner_user_id (str): Owner user ID.
        """
        self.client_id = client_id
        self.name = name
        self.owner_user_id = owner_user_id
        self._validate()

    def __repr__(self) -> str:
        """
        String representation of the App object.

        Returns:
            str: String representation of the App object.
        """
        return f"App(client_id={self.client_id}, name={self.name}, owner_user_id={self.owner_user_id})"
    
    def __str__(self) -> str:
        """
        String representation of the App object.

        Returns:
            str: String representation of the App object.
        """
        return f"App: {self.name} (Client ID: {self.client_id})"

def get_user_info(user_id: str, authorization_mode: str, access_token: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None) -> tuple[User, int, int] | Never:
    """
    Get user information.

    Args:
        user_id (str): User ID.
        authorization_mode (str): Authorization mode.
        access_token (Optional[str]): Access token. Default is None.
        client_id (Optional[str]): Client ID. Default is None.
        client_secret (Optional[str]): Client secret. Default is None.
    Returns:
        User: User object.
        int: ユーザーのサポーターの数
        int: ユーザーがサポートしている数
    """
    match authorization_mode:
        case 'basic':
            if client_id is None or client_secret is None:
                raise ValueError("client_id and client_secret must be provided for basic authorization.")
            headers = {
                'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
            }
        case 'bearer':
            if access_token is None:
                raise ValueError("access_token must be provided for bearer authorization.")
            headers = {
                'Authorization': 'Bearer ' + access_token,
            }
        case _:
            raise ValueError("Invalid authorization mode. Use 'basic' or 'bearer'.")
    url = f"https://apiv2.twitcasting.tv/users/{user_id}"
    headers['Accept'] = 'application/json'
    headers['X-Api-Version'] = '2.0'
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_code = e.code
        error_message = ERROR_CODES_DICT.get(error_code, ("Unknown Error", "Unknown Error", Exception))[1]
        raise Exception(f"Error {error_code}: {error_message}")
    except urllib.error.URLError as e:
        raise Exception(f"URL Error: {e.reason}")
    except json.JSONDecodeError as e:
        raise Exception(f"JSON Decode Error: {e.msg}")
    error = data.get('error', None)
    if error:
        error_code = error.get("code", None)
        error_tuple:Optional[tuple] = ERROR_CODES_DICT.get(error_code, "Unknown error")
        exception = error_tuple[2]
        raise exception(f"Error {error_code}: {error_tuple[0]} - {error_tuple[1]}")
    user_data = data.get('user', {})
    user: User
    user = User(
        id=user_data.get('id', ''),
        screen_id=user_data.get('screen_id', ''),
        name=user_data.get('name', ''),
        image=user_data.get('image', ''),
        profile=user_data.get('profile', ''),
        level=user_data.get('level', 0),
        last_movie_id=user_data.get('last_movie_id', None),
        is_live=user_data.get('is_live', False)
    )
    supporter_count = user_data.get('supporter_count', 0)
    supporting_count = user_data.get('supporting_count', 0)
    return user, supporter_count, supporting_count

def _verify_credential(authorization_mode: str, access_token: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None) -> tuple[App, User, int, int] | Never:
    """
    Verify credentials.

    Args:
        authorization_mode (str): Authorization mode.
        access_token (Optional[str]): Access token. Default is None.
        client_id (Optional[str]): Client ID. Default is None.
        client_secret (Optional[str]): Client secret. Default is None.

    Returns:
        App: App object.
        User: User object.
        int: ユーザーのサポーターの数
        int: ユーザーがサポートしている数
    """
    match authorization_mode:
        case 'basic':
            if client_id is None or client_secret is None:
                raise ValueError("client_id and client_secret must be provided for basic authorization.")
            headers = {
                'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
            }
        case 'bearer':
            if access_token is None:
                raise ValueError("access_token must be provided for bearer authorization.")
            headers = {
                'Authorization': 'Bearer ' + access_token,
            }
        case _:
            raise ValueError("Invalid authorization mode. Use 'basic' or 'bearer'.")
    url = f"https://apiv2.twitcasting.tv/verify_credentials"
    headers['Accept'] = 'application/json'
    headers['X-Api-Version'] = '2.0'
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_code = e.code
        error_message = ERROR_CODES_DICT.get(error_code, ("Unknown Error", "Unknown Error", Exception))[1]
        raise Exception(f"Error {error_code}: {error_message}")
    except urllib.error.URLError as e:
        raise Exception(f"URL Error: {e.reason}")
    except json.JSONDecodeError as e:
        raise Exception(f"JSON Decode Error: {e.msg}")
    error = data.get('error', None)
    if error:
        error_code = error.get("code", None)
        error_tuple:Optional[tuple] = ERROR_CODES_DICT.get(error_code, "Unknown error")
        exception = error_tuple[2]
        raise exception(f"Error {error_code}: {error_tuple[0]} - {error_tuple[1]}")
    app_data = data.get('app', {})
    app: App
    app = App(
        client_id=app_data.get('client_id', ''),
        name=app_data.get('name', ''),
        owner_user_id=app_data.get('owner_user_id', '')
    )
    user_data = data.get('user', {})
    user: User
    user = User(
        id=user_data.get('id', ''),
        screen_id=user_data.get('screen_id', ''),
        name=user_data.get('name', ''),
        image=user_data.get('image', ''),
        profile=user_data.get('profile', ''),
        level=user_data.get('level', 0),
        last_movie_id=user_data.get('last_movie_id', None),
        is_live=user_data.get('is_live', False)
    )
    supporter_count = user_data.get('supporter_count', 0)
    supporting_count = user_data.get('supporting_count', 0)
    return app, user, supporter_count, supporting_count