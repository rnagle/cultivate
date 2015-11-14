class Config(object):
    DEBUG = True
    TWEET_LIMIT = 100

class ProdConfig(object):
    DEBUG = False
    TWEET_LIMIT = 500
