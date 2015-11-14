class Config(object):
    DEBUG = True
    FAKE = True
    TWEET_LIMIT = 50

class ProdConfig(object):
    DEBUG = False
    FAKE = True
    TWEET_LIMIT = 500
