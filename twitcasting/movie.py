from typing import Optional

from .exceptions import ERROR_CODES_DICT

class Movie:
    """
    Movie class for TwitCasting API.
    """

    def __init__(self, id: str, user_id: str, title: str, subtitle: Optional[str], last_owner_comment: Optional[str], category: Optional[str], link: str, is_live: bool, is_recorded: bool, comment_count: int, large_thumbnail: str, small_thumbnail: str, country: str, duration: int, created: int, is_collabo: bool, is_protected: bool, max_view_count: int, current_view_count: int, total_view_count: int, hls_url: Optional[str]) -> None:
        """
        Initialize the Movie object.

        Args:
            id (str): Movie ID.
            user_id (str): User ID.
            title (str): Movie title.
            subtitle (Optional[str]): Movie subtitle. Default is None.
            last_owner_comment (Optional[str]): Last owner comment. Default is None.
            category (Optional[str]): Movie category. Default is None.
            link (str): Movie link.
            is_live (bool): Whether the movie is live or not.
            is_recorded (bool): Whether the movie is recorded or not.
            comment_count (int): Number of comments.
            large_thumbnail (str): Large thumbnail URL.
            small_thumbnail (str): Small thumbnail URL.
            country (str): Country code.
            duration (int): Movie duration in seconds.
            created (int): Created timestamp.
            is_collabo (bool): Whether the movie is a collaboration or not.
            is_protected (bool): Whether the movie is protected or not.
            max_view_count (int): Maximum view count.
            current_view_count (int): Current view count.
            total_view_count (int): Total view count.
            hls_url (Optional[str]): HLS URL. Default is None.
        """
        self.id = id
        self.user_id = user_id
        self.title = title
        self.subtitle = subtitle
        self.last_owner_comment = last_owner_comment
        self.category = category
        self.link = link
        self.is_live = is_live
        self.is_recorded = is_recorded
        self.comment_count = comment_count
        self.large_thumbnail = large_thumbnail
        self.small_thumbnail = small_thumbnail
        self.country = country
        self.duration = duration
        self.created = created
        self.is_collabo = is_collabo
        self.is_protected = is_protected
        self.max_view_count = max_view_count
        self.current_view_count = current_view_count
        self.total_view_count = total_view_count
        self.hls_url = hls_url