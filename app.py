import os

from flask import Flask, render_template, request
import tweepy
import urllib
import collections
import datetime
import json

app = Flask(__name__)

if os.environ.get('DEPLOYMENT_TARGET', False) == 'production':
    app.config.from_object('config.ProdConfig')
else:
    app.config.from_object('config.Config')

auth = tweepy.OAuthHandler(os.environ.get('TWITTER_CONSUMER_KEY'), os.environ.get('TWITTER_CONSUMER_SECRET'))
auth.set_access_token(os.environ.get('TWITTER_ACCESS_TOKEN_KEY'), os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))
api = tweepy.API(auth)

@app.route('/')
def home():
    return render_template('home.html', **{'content': 'Cultivate!'})


@app.route('/results')
def results():
    return render_template('results.html', **{'content': 'Results!'})


@app.route('/person/<identifier>')
def person(identifier):
    return render_template('home.html', **{'content': 'Person!'})


@app.route('/search', methods=['POST'])
def search():
    """
    TODO:
    - search for stuff on twitter
    - figure out who's included and rank them
    - return json to build results list
    """
    query = dict(request.form)
    querystring = get_querystring_from_params(query['term[]'])
    tweets = tweepy.Cursor(
        api.search,
        q=querystring,
        rpp=100,
        result_type="recent"
    ).items(1000)

    users = {}
    for tweet in tweets:
        user = users.get(tweet.author.screen_name)
        screen_name = tweet.author.screen_name

        if user is None:
            counts = {
                'statuses': tweet.author.statuses_count,
                'listed': tweet.author.listed_count,
                'friends': tweet.author.friends_count,
                'followers': tweet.author.followers_count,
                'total_tweets': 0,
                'total_favorited': 0,
                'total_retweeted': 0
            }
            users[screen_name] = tweet.author._json
            users[screen_name]['counts'] = counts

        users[screen_name]['counts']['total_tweets'] += 1
        users[screen_name]['counts']['total_favorited'] += tweet.favorite_count
        users[screen_name]['counts']['total_retweeted'] += tweet.retweet_count

    for screen_name in users.keys():
        users[screen_name]['score'] = get_score(users[screen_name])

    return json.dumps({'users': users})


def get_score(user):
    score = 0
    score += user['counts']['total_tweets']
    score += user['counts']['total_favorited']
    score += user['counts']['total_retweeted'] * 2
    score += user['counts']['followers'] / 50
    return score


def get_querystring_from_params(params):
    return urllib.quote_plus('+'.join(params))


port = int(os.environ.get('PORT', 5000))
if __name__ == '__main__':
    app.run(port=port, host='0.0.0.0')
