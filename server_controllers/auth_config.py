from authomatic.providers import oauth2, oauth1
import authomatic
from authomatic import Authomatic

CONFIG = {
    'fb': {
        'class_': oauth2.Facebook,
        'consumer_key': '809734642398306',
        'consumer_secret': 'd65c89ac5e420d2030e5c14a7f011852',
        'id': authomatic.provider_id(),
        
        # We need the "publish_stream" scope to post to users timeline,
        # the "offline_access" scope to be able to refresh credentials,
        # and the other scopes to get user info.
        'scope': ['offline_access', 'email'],
    },
}

authomatic = Authomatic(config=CONFIG, secret='123ABChiImtotallyrandom')