import urllib, base64, json
import urllib.request, urllib.error
from urllib.parse import urlencode
from typing import Never, Optional

from .exceptions import ERROR_CODES_DICT
from .user import User
from .movie import Movie

class Webhook:
    """
    Webhook class for TwitCasting API.
    """
    def _validate(self):
        """
        Validate the Webhook object.

        Raises:
            ValueError: If user_id or event is invalid.
        """
        if not self.user_id:
            raise ValueError("user_id cannot be empty")
        if not self.event:
            raise ValueError("event cannot be empty")
        if self.event not in ["livestart", "liveend"]:
            raise ValueError("event must be either 'livestart' or 'liveend'")
        self._validate()

    def __init__(self, user_id: str, event: str):
        """
        Initialize the Webhook object.

        Args:
            user_id (str): User ID.
            event (str): Event type.
        """
        self.user_id = user_id
        self.event = event
        self._validate()

    def __repr__(self):
        return f"Webhook(user_id={self.user_id}, event={self.event})"
    
    def __str__(self):
        return f"Webhook(user_id={self.user_id}, event={self.event})"
    
    def __eq__(self, other):
        if not isinstance(other, Webhook):
            return NotImplemented
        return self.user_id == other.user_id and self.event == other.event
    
    def __ne__(self, other):
        if not isinstance(other, Webhook):
            return NotImplemented
        return not self.__eq__(other)

def get_webhook_list(authorization_mode: str, access_token: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None, user_id: Optional[str] = None, limit: int = 50, offset: int = 0) -> tuple[int, list[Webhook]] | Never:
    """
    Get the list of webhooks.

    Args:
        authorization_mode (str): Authorization mode. 
            - "bearer" fro Access token
            - "basic" for Client ID and Client Secret
        access_token (Optional[str]): Access token.
        client_id (Optional[str]): Client ID.
        client_secret (Optional[str]): Client secret.
        user_id (Optional[str]): User ID. If None, all webhooks are retrieved.
        limit (int): Number of webhooks to retrieve. Default is 50.
        offset (int): Offset for pagination. Default is 0.

    Returns:
        int: 登録済みWebHook件数
        list[Webhook]: Webhook list.
        Never: Raises an exception if the request fails.
    """
    match authorization_mode:
        case "bearer":
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        case "basic":
            headers = {
                "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"
            }
        case _:
            raise ValueError("Invalid authorization mode. Use 'bearer' or 'basic'.")
    headers["Accept"] = "application/json"
    headers["X-Api-Version"] = "2.0"
    url = f"https://apiv2.twitcasting.tv/webhooks?limit={limit}&offset={offset}"
    if user_id:
        url += f"&user_id={user_id}"
    try:
        response = urllib.request.urlopen(urllib.request.Request(url, headers=headers))
        response_data = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_code = e.code
        error_message = ERROR_CODES_DICT.get(error_code, "Unknown error")
        raise Exception(f"Error {error_code}: {error_message}") from e
    except urllib.error.URLError as e:
        raise Exception(f"URL Error: {e.reason}") from e
    except json.JSONDecodeError as e:
        raise Exception(f"JSON Decode Error: {e.msg}") from e
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}") from e
    #{
    #    "all_count": 2,
    #    "webhooks": [
    #      {"user_id":"7134775954","event":"livestart"},
    #      {"user_id":"7134775954","event":"liveend"}
    #    ]
    #}
    webhooks:list[Webhook] = []
    error = response_data.get("error", None)
    if error:
        error_code = error.get("code", None)
        error_tuple:Optional[tuple] = ERROR_CODES_DICT.get(error_code, "Unknown error")
        exception = error_tuple[2]
        raise exception(f"Error {error_code}: {error_tuple[0]} - {error_tuple[1]}")
    all_count = response_data.get("all_count", 0)
    webhooks_data = response_data.get("webhooks", [])
    for webhook_data in webhooks_data:
        user_id = webhook_data.get("user_id", "")
        event = webhook_data.get("event", "")
        webhooks.append(Webhook(user_id, event))
    return all_count, webhooks

def register_webhook(authorization_mode: str, user_id: str, events: list[str], access_token: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None) -> tuple[str, list[str]] | Never:
    """
    Register a webhook.

    Args:
        authorization_mode (str): Authorization mode. 
            - "bearer" fro Access token
            - "basic" for Client ID and Client Secret
        access_token (Optional[str]): Access token.
        client_id (Optional[str]): Client ID.
        client_secret (Optional[str]): Client secret.
        user_id (str): User ID.
        events (list[str]): List of events to register.

    Returns:
        str: User ID.
        list[str]: List of added events.
        Never: Raises an exception if the request fails.
    """
    match authorization_mode:
        case "bearer":
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        case "basic":
            headers = {
                "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"
            }
        case _:
            raise ValueError("Invalid authorization mode. Use 'bearer' or 'basic'.")
    headers["Accept"] = "application/json"
    headers["X-Api-Version"] = "2.0"
    url = f"https://apiv2.twitcasting.tv/webhooks"
    data = {
        "user_id": user_id,
        "events": events
    }
    try:
        response = urllib.request.urlopen(urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers))
        response_data = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_code = e.code
        error_message = ERROR_CODES_DICT.get(error_code, "Unknown error")
        raise Exception(f"Error {error_code}: {error_message}") from e
    except urllib.error.URLError as e:
        raise Exception(f"URL Error: {e.reason}") from e
    except json.JSONDecodeError as e:
        raise Exception(f"JSON Decode Error: {e.msg}") from e
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}") from e
    #{
    #  "user_id":"7134775954",
    #  "events":["livestart","liveend"]
    #}
    error = response_data.get("error", None)
    if error:
        error_code = error.get("code", None)
        error_tuple:Optional[tuple] = ERROR_CODES_DICT.get(error_code, "Unknown error")
        exception = error_tuple[2]
        raise exception(f"Error {error_code}: {error_tuple[0]} - {error_tuple[1]}")
    user_id = response_data.get("user_id", "")
    events = response_data.get("events", [])
    return user_id, events

def delete_webhook(authorization_mode:str, user_id: str, access_token: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None) -> tuple[str, list[str]] | Never:
    """
    Delete a webhook.

    Args:
        authorization_mode (str): Authorization mode. 
            - "bearer" fro Access token
            - "basic" for Client ID and Client Secret
        access_token (Optional[str]): Access token.
        client_id (Optional[str]): Client ID.
        client_secret (Optional[str]): Client secret.
        user_id (str): User ID.

    Returns:
        str: User ID.
        list[str]: List of deleted events.
        Never: Raises an exception if the request fails.
    """
    match authorization_mode:
        case "bearer":
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        case "basic":
            headers = {
                "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"
            }
        case _:
            raise ValueError("Invalid authorization mode. Use 'bearer' or 'basic'.")
    headers["Accept"] = "application/json"
    headers["X-Api-Version"] = "2.0"
    url = f"https://apiv2.twitcasting.tv/webhooks?user_id={user_id}"
    try:
        response = urllib.request.urlopen(urllib.request.Request(url, method="DELETE", headers=headers))
        response_data = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_code = e.code
        error_message = ERROR_CODES_DICT.get(error_code, "Unknown error")
        raise Exception(f"Error {error_code}: {error_message}") from e
    except urllib.error.URLError as e:
        raise Exception(f"URL Error: {e.reason}") from e
    except json.JSONDecodeError as e:
        raise Exception(f"JSON Decode Error: {e.msg}") from e
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}") from e
    #{
    #  "user_id":"7134775954",
    #  "events":["livestart","liveend"]
    #}
    error = response_data.get("error", None)
    if error:
        error_code = error.get("code", None)
        error_tuple:Optional[tuple] = ERROR_CODES_DICT.get(error_code, "Unknown error")
        exception = error_tuple[2]
        raise exception(f"Error {error_code}: {error_tuple[0]} - {error_tuple[1]}")
    user_id = response_data.get("user_id", "")
    events = response_data.get("events", [])
    return user_id, events

def parse_webhook_data(data: str, signature: Optional[str]= None) -> tuple[Movie, User] | Never:
    """
    Parse the webhook data.

    Args:
        data (str): Webhook data.
        signature (Optional[str]): Signature for verification.

    Returns:
        bool: Whether the data is valid or not.
        Movie: Movie object.
        User: User object.
        Never: Raises an exception if the request fails.
    """
    data_obj = json.loads(data)
    if not data_obj:
        raise ValueError("Invalid data")
    if signature:
        if signature != data_obj.get("signature", ""):
            raise ValueError("Invalid signature")
    movie_data = data_obj.get("movie", {})
    movie: Movie = Movie(
        id=movie_data.get("id", ""),
        user_id=movie_data.get("user_id", ""),
        title=movie_data.get("title", ""),
        subtitle=movie_data.get("subtitle", None),
        last_owner_comment=movie_data.get("last_owner_comment", None),
        category=movie_data.get("category", None),
        link=movie_data.get("link", ""),
        is_live=movie_data.get("is_live", False),
        is_recorded=movie_data.get("is_recorded", False),
        comment_count=movie_data.get("comment_count", 0),
        large_thumbnail=movie_data.get("large_thumbnail", ""),
        small_thumbnail=movie_data.get("small_thumbnail", ""),
        country=movie_data.get("country", ""),
        duration=movie_data.get("duration", 0),
        created=movie_data.get("created", 0),
        is_collabo=movie_data.get("is_collabo", False),
        is_protected=movie_data.get("is_protected", False),
        max_view_count=movie_data.get("max_view_count", 0),
        current_view_count=movie_data.get("current_view_count", 0),
        total_view_count=movie_data.get("total_view_count", 0),
        hls_url=movie_data.get("hls_url", None)
    )
    user_data = data_obj.get("user", {})
    user: User = User(
        id=user_data.get("id", ""),
        screen_id=user_data.get("screen_id", ""),
        name=user_data.get("name", ""),
        image=user_data.get("image", ""),
        profile=user_data.get("profile", ""),
        level=user_data.get("level", 0),
        last_movie_id=user_data.get("last_movie_id", None),
        is_live=user_data.get("is_live", False)
    )
    return movie, user