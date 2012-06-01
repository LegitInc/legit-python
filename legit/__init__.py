__version_info__ = ('0', '1')
__version__ = '.'.join(__version_info__)

import os
import oauth2
import urllib
try:
    import json
except ImportError:
    import simplejson as json

BASE_URL = "https://legitapi.appspot.com"

class LegitBadRequestError(Exception):
    "Exception thrown when a request is bad"
    pass

class LegitPermissionError(Exception):
    "Exception thrown when a permission error is encountered"
    pass

class LegitUser(object):
    """
    Container class for all the identity aspects that the Legit API takes into
    account when specifying a user.
    """
    def __init__(self, user_id=None, name=None, address=None, ssn=None, 
                 phone=None, email=None, facebook_id=None, twitter_id=None, 
                 linkedin_id=None, drivers_lic=None):
        self.user_id=user_id
        self.name=name
        self.address=address
        self.ssn=ssn
        self.phone=phone
        self.email=email
        self.facebook_id=facebook_id
        self.twitter_id=twitter_id
        self.linkedin_id=linkedin_id
        self.drivers_lic=drivers_lic
        
    def to_dict(self):
        rv = {}
        for prop in ("user_id", "name", "address", "ssn", "phone", "email", 
                     "facebook_id", "twitter_id", "linkedin_id", "drivers_lic"):
            attr = getattr(self, prop, None)
            if attr != None:
                rv[prop] = attr
        return rv

class LegitClient(object):
    """
    The primary class for interacting with the Legit API. You have the option
    of creating it with your authentication key/secret. If you do not specify
    these, the client will attempt to read them out of the environment variables
    LEGIT_KEY and LEGIT_SECRET respectively. 
    
    The LegitClient's has a method for each resource of the Legit API. The 
    parameters of the client methods are the same as that of the API method.
    However, the identity elements of a call (user_id, name, email, etc) are 
    passed in via a LegitUser object. 
    """
    def __init__(self, consumer_key=None, consumer_secret=None):
        self.consumer_key = consumer_key or os.environ.get("LEGIT_KEY")
        self.consumer_secret = consumer_secret or os.environ.get("LEGIT_SECRET")
        
        consumer = oauth2.Consumer(key=self.consumer_key, secret=self.consumer_secret)
        self.client = oauth2.Client(consumer)
    
    def make_request(self, data, resource, category, method, sandbox):
        api = "sandbox" if sandbox else "api"        
        url = "%s/%s/%s/%s" % (BASE_URL, api, category, resource)

        resp, content = self.client.request(url, method, urllib.urlencode(data))

        if resp.status == 400:
            raise LegitBadRequestError("%d: %s" % (resp.status,content))
        elif resp.status == 403:
            raise LegitPermissionError("%d: %s" % (resp.status,content))
        elif resp.status != 200:
            raise Exception("%d: %s" % (resp.status,content))

        return json.loads(content)
    
    def submit(self, legit_user, transaction_count, review_count, 
               positive_review_percentage, date_joined, date_banned=None,
               reason_banned=None, sandbox=False):
        """
        Invokes the submit method of the Legit API. 
        
        Args:
            legit_user: A LegitUser object containing all the information needed
                to identity this user.
            
            transaction_count: Number of transaction the user has successfully completed
            review_count: Number of reviews for the user
            positive_revew_percentage: Percentage of review for the user whihch
                are positive
            date_joined: Date the user joined as a string in the format "YYYY-MM-DD"
            date_banned (optional): Date the user was banned in the format "YYYY-MM-DD"
            reason_banned (optional): Reason the user was banned
            
            sandbox: Boolean that dictates whether the request should be made
                against the sandbox API or the production API.

        Returns: 
            A dictionary of response data. See the Legit API docs for the
            precise structure of the response.
        """
        data = legit_user.to_dict()
        data["transaction_count"] = transaction_count
        data["review_count"] = review_count
        data["positive_review_percentage"] = positive_review_percentage
        data["date_joined"] = date_joined
        if date_banned != None:
            data["date_banned"] = date_banned
        if reason_banned != None:
            data["reason_banned"] = reason_banned
        
        return self.make_request(data, "user", "submit", "POST", sandbox)    
               
    def report(self, components, legit_user, sandbox=False):
        """
        Invokes the report method of the Legit API.
        
        Args:
            components: List of components you wish to include in the report.
            legit_user: A LegitUser object containing all the data needed to
                identity this user.
            
            sandbox: Boolean that dictates whether the request should be made
                against the sandbox API or the production API.        
        """
        # Validate the components/identity data
        
        data = legit_user.to_dict()
        data["components"] = ",".join(components)
        
        return self.make_request(data, "report", "query", "GET", sandbox)
        
        
        
        
        
        
        
        
        
        
        
        
        
        