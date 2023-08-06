import requests
from requests.auth import HTTPBasicAuth

class Auth:
    """
    Basic Email and Password authentication
    """
    def basicAuth(self, email, password, tokenEndpoint):
        self.email = email
        self.password = password
        self.tokenEndpoint=tokenEndpoint
        # get token
        res =  requests.post(tokenEndpoint,auth=HTTPBasicAuth(self.email,self.password))
        jsonres= res.json()
        if(jsonres['status']=='SUCCESS'):
            return jsonres['tokenInfo']
        else:
            return 'Error'
