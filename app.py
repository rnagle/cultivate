import os

from flask import Flask, render_template, request
import tweepy
import urllib
import collections
import datetime

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
    tweets = tweepy.Cursor(api.search, q=querystring, rpp=100, result_type="recent").items(1000)
    users = {}
    for tweet in tweets:
        user = users.get(tweet.author.screen_name)
        if user is None:
            users[tweet.author.screen_name] = {
                'user_info': {},
                'tweet_counts': {}
            }
            users[tweet.author.screen_name]['user_info'] = {
                'statuses_count': tweet.author.statuses_count,
                'lists_memberships': tweet.author.lists_memberships,
                'listed_count': tweet.author.listed_count,
                'friends_count': tweet.author.friends_count,
                'followers_count': tweet.author.followers_count,
                'description': tweet.author.description,
                'location': tweet.author.location
            }
            users[tweet.author.screen_name]['tweet_counts']['favorited_count'] = 0
            users[tweet.author.screen_name]['tweet_counts']['retweeted_count'] = 0
        users[tweet.author.screen_name]['tweet_counts']['favorited_count'] += tweet.favorite_count
        users[tweet.author.screen_name]['tweet_counts']['retweeted_count'] += tweet.retweet_count
    return '{"success": true}'

def get_tweets_from_query(query):
    querystring = get_querystring_from_params(query['term[]'])
    results = api.search(querystring)
    import ipdb; ipdb.set_trace()
    return results

def get_querystring_from_params(params):
    string = urllib.quote_plus('+'.join(params))

    last_month = datetime.datetime.now() - datetime.timedelta(days=30)
    string += 'since:{}'.format(last_month.strftime('%Y-%m-%d'))
    return string

port = int(os.environ.get('PORT', 5000))
if __name__ == '__main__':
    app.run(port=port, host='0.0.0.0')
