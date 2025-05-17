from twitcasting import webhook, exceptions
from twitcasting.movie import Movie
from twitcasting.user import User
from twitcasting.webhook import Webhook
import os

from . import config

def test_parse_webhook_data():
    """
    Test the parse_webhook_data function.
    """
    test_data_path = os.path.join(os.path.dirname(__file__), 'webhook.json')
    with open(test_data_path, 'r') as f:
        data = f.read()
    movie: Movie
    user: User 
    movie, user = (webhook.parse_webhook_data(data))
    assert isinstance(movie, Movie)
    assert isinstance(user, User)

def test_get_webhook_list():
    """
    Test the get_webhook_list function.
    """
    webhook_count: int
    webhook_list: list[Webhook]
    webhook_count, webhook_list = webhook.get_webhook_list(authorization_mode='basic', client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET)
    print(f"Webhook Count: {webhook_count}")
    print(f"Webhook List: {webhook_list}")
    assert isinstance(webhook_count, int)
    assert isinstance(webhook_list, list)
    #assert all(isinstance(webhook, Webhook) for webhook in webhook_list)