import oauth2
import urllib
try:
    import json
except ImportError:
    import simplejson as json

BASE_URL = "https://legitapi.appspot.com/"

class RequestError(Exception):
    pass

class LegitClient(object):
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        
        consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
        self.client = oauth2.Client(consumer)
    
    def _make_request(self, data, method, resource, sandbox):
         api = "sandbox" if sandbox else "api"        
         url = "%s/%s/%s" % (BASE_URL, api, resource)

         resp, content = self.client.request(url, method, urllib.urlencode(data))

         if resp != 200:
             raise RequestError(content)

         return json.loads(content)
    
    def submit(self, parameters, sandbox=False):
        """
        Invokes the submit method of the Legit API. 
        
        Args:
            parameters: Dictionary of data that identitifies a user. See
            the API docs for information on the specific fields.
            
            sandbox: Boolean that dictates whether the request should be made
            against the sandbox API or the production API.

        Returns: A dictionary of request data.
        """
        return self._make_request(parameters, "submit", "POST", sandbox)
        
               
    def report(self, components, parameters, sandbox=False):
        """
        Invokes the report method of the Legit API
        
        """
        # Validate the components/identity data
        
        request_data = {}
        request_data.update(parameters)
        request_data["components"] = ",".join(components)
        
        return self._make_request(request_data, "report", "GET", sandbox)
        
        
        
        
        
        
        
        
        
        
        
        
        
        