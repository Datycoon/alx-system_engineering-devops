#!/usr/bin/python3
"""
Function that queries the Reddit API and prints
the top ten hot posts of a subreddit
"""
from collections import defaultdict
import requests


def add_title(dictionary, hot_posts):
    """ Adds item into a list """
    if not hot_posts:
        return

    title = hot_posts[0]['data']['title'].split()
    for word in title:
        for key in dictionary:
            if word.lower() == key.lower():
                dictionary[key] += 1
    hot_posts.pop(0)
    add_title(dictionary, hot_posts)


def recurse(subreddit, dictionary, after=None):
    """ Queries to Reddit API """
    u_agent = 'Mozilla/5.0'
    headers = {'User-Agent': u_agent}
    params = {'after': after}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"

    res = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if res.status_code != 200:
        return None

    dic = res.json()
    hot_posts = dic['data']['children']
    add_title(dictionary, hot_posts)
    after = dic['data']['after']
    if after:
        recurse(subreddit, dictionary, after=after)


def count_words(subreddit, word_list):
    """ Init function """
    dictionary = defaultdict(int)

    recurse(subreddit, dictionary)

    l = sorted(dictionary.items(), key=lambda kv: kv[1], reverse=True)

    if l:
        for item in l:
            if item[1] != 0:
                print("{}: {}".format(item[0], item[1]))
    else:
        print("")

