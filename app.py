import os
import tweepy
import urllib
import json

from flask import Flask, render_template, request, Response
from geopy.geocoders import Nominatim as Geocoder
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__)

if os.environ.get('DEPLOYMENT_TARGET', False) == 'production':
    app.config.from_object('config.ProdConfig')
else:
    app.config.from_object('config.Config')

auth = tweepy.OAuthHandler(
    os.environ.get('TWITTER_CONSUMER_KEY'),
    os.environ.get('TWITTER_CONSUMER_SECRET')
)
auth.set_access_token(
    os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
    os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
)
api = tweepy.API(auth)

@app.route('/')
def home():
    return render_template('home.html', **{'content': 'Cultivate!'})


@app.route('/search', methods=['POST'])
def search():
    with open('data/users.json') as users_json:
        resp = users_json.read()
        return Response(resp, mimetype='application/json')


def get_score(user, query):
    score = 0
    score += user['counts']['total_tweets']
    score += user['counts']['total_favorited']
    score += user['counts']['total_retweeted'] * 2
    score += user['counts']['followers'] / 75
    return score


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def get_querystring_from_params(params):
    return urllib.quote_plus('+'.join(params))


port = int(os.environ.get('PORT', 5000))
if __name__ == '__main__':
    app.run(port=port, host='0.0.0.0')
