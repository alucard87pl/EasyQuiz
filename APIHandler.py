from pprint import pprint

import requests

url = 'https://opentdb.com/'


def get_categories():
    """
    Returns a list of all categories
    """
    response = requests.get(url + 'api_category.php')
    return response.json()['trivia_categories']


def get_questions(a, c=None, d=None, t=None):
    """
    Returns a list of questions for a given category
    """
    response = requests.get(url + 'api.php', params={'amount': a, 'category': c, 'difficulty': d, 'type': t})
    return response.json()['results']

