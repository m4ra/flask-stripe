import os
import stripe

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
     #   'postgresql:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    # Stripe configuration:
    # https://stripe.com/docs/checkout/guides/flask
    # modified execution string:  
    #  PUBLISHABLE_KEY=<test publishable key from stripe API> SECRET_KEY=<test
    #  secret key from stripe API> python manage.py runserver

    STRIPE_KEYS = {
        # 'secret_key': os.environ['SECRET_KEY'],
        # 'publishable_key': os.environ['PUBLISHABLE_KEY']
        'secret_key':'sk_test_vv1QGRslGX4eXCSfZLc0KcoZ',
        'publishable_key':'pk_test_D1ol20dCt0FNQQxkIWI7Pc8U'
    }

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    stripe.api_key = STRIPE_KEYS['secret_key']


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    STRIPE_KEYS = {
        # 'secret_key': os.environ['SECRET_KEY'],
        # 'publishable_key': os.environ['PUBLISHABLE_KEY']
        'secret_key':'sk_live_aCZGf8EhD6V3e0VmdTo0SRa8',
        'publishable_key':'pk_live_OGP9ExBicjJqS5VTw6mAKHKj'
    }


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
