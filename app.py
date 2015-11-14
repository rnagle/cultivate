import os
import tweepy
import urllib
import requests
import json

from flask import Flask, render_template, request, Response
from flask.ext.compress import Compress

from geopy.geocoders import Nominatim as Geocoder
from geopy.distance import vincenty

app = Flask(__name__)
Compress(app)

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
    if app.config['FAKE']:
        return fake_search()
    else:
        return real_search()


def fake_search():
    query = dict(request.form)
    city = query['city'][0]
    term = query['term[]'][0]

    if term == 'codepen' and city == 'New York, NY':
        with open('data/codepen_nyc.json') as users_json:
            resp = users_json.read()
            return Response(resp, mimetype='application/json')

    if term == 'buzzfeed.com/food' and city == 'Indianapolis, IN':
        with open('data/buzzfeed_indy.json') as users_json:
            resp = users_json.read()
            return Response(resp, mimetype='application/json')

    if term == 'theskimm' and city == 'Chicago, IL':
        with open('data/skimm_chicago.json') as users_json:
            resp = users_json.read()
            return Response(resp, mimetype='application/json')

    return Response(json.dumps({'users': []}), mimetype='application/json')


def real_search():
    query = dict(request.form)
    querystring = get_querystring_from_params(query['term[]'])

    geocoder = Geocoder()
    # loc = geocode(query['city'][0])
    loc = geocoder.geocode(query['city'][0], timeout=10)

    tweets = tweepy.Cursor(
        api.search,
        q=querystring,
        rpp=100,
        result_type="recent"
    ).items(app.config['TWEET_LIMIT'])

    users = {}
    skip = []
    for tweet in tweets:
        user = users.get(tweet.author.screen_name)
        screen_name = tweet.author.screen_name

        if screen_name in skip:
            continue

        if user is None:
            location = tweet.author.location.encode("utf-8")
            user_loc = geocoder.geocode(location, timeout=10)
            print "address: {}".format(location)
            if user_loc and loc:
                if distance(user_loc.longitude, user_loc.latitude, loc.longitude, loc.latitude) < 30:
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
                else:
                    skip.append(screen_name)
                    continue
            else:
                skip.append(screen_name)
                continue

        users[screen_name]['counts']['total_tweets'] += 1
        users[screen_name]['counts']['total_favorited'] += tweet.favorite_count
        users[screen_name]['counts']['total_retweeted'] += tweet.retweet_count

    for screen_name in users.keys():
        users[screen_name]['score'] = get_score(users[screen_name], query)

    return Response(json.dumps({'users': users}), mimetype='application/json')


def get_score(user, query):
    score = 0
    score += user['counts']['total_tweets']
    score += user['counts']['total_favorited']
    score += user['counts']['total_retweeted'] * 2
    score += user['counts']['followers'] / 75
    return score


def distance(lon1, lat1, lon2, lat2):
    return vincenty((lon1, lat1), (lon2, lat2)).miles


def geocode(address):
    request_url = 'http://maps.googleapis.com/maps/api/geocode/json?'
    try:
        request_url += urllib.urlencode({'address': address})
    except:
        print "NOPE NOT UNICODE: {}".format(address.encode("utf-8"))
        return False
    response = requests.get(request_url)
    data = json.loads(response.content)
    if data['results']:
        if data['results'][0]:
            lat = data['results'][0]['geometry']['location']['lat']
            lng = data['results'][0]['geometry']['location']['lng']
            return {
                'latitude': lat,
                'longitude': lng
            }
        else:
            print "NOPE NO RESULTS FOR: {}".format(address)
            return False
    else:
        print "NOPE COULDNT GEOLOCATE: {}".format(address)
        return False

def get_querystring_from_params(params):
    return urllib.quote_plus('+'.join(params))


port = int(os.environ.get('PORT', 5000))
if __name__ == '__main__':
    app.run(port=port, host='0.0.0.0')
