from twitcasting import webhook, exceptions, user
from twitcasting.movie import Movie
from twitcasting.user import User, App

from . import config

def test_get_user_info():
    """
    Test the get_user_info function.
    """
    user_id = 'nekoya_cocona'
    authorization_mode = 'basic'
    user_obj: User
    supporter_count: int
    supported_count: int
    user_obj, supporter_count, supported_count = user.get_user_info(user_id=user_id, authorization_mode=authorization_mode, client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET)
    print(f"User: {user_obj}")
    print(f"Supporter Count: {supporter_count}")
    print(f"Supported Count: {supported_count}")
    assert isinstance(user_obj, User)
    assert isinstance(supporter_count, int)
    assert isinstance(supported_count, int)

def _test_verify_credential():
    """
    Test the verify_credentials function.
    """
    app_obj: App
    user_obj: User
    supporter_count: int
    supported_count: int
    app_obj, user_obj, supporter_count, supported_count = user.verify_credential(authorization_mode='basic', access_token=config.CLIENT_ID, client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET)
    print(f"App: {app_obj}")
    print(f"User: {user_obj}")
    print(f"Supporter Count: {supporter_count}")
    print(f"Supported Count: {supported_count}")
    assert isinstance(app_obj, App)
    assert isinstance(user_obj, User)
    assert isinstance(supporter_count, int)
    assert isinstance(supported_count, int)