from requests import request
import base64, urllib.parse
from flask import current_app


class Mpesa:
    """
    """
    def __init__(self):
        """
        """
        pass

    def get_requests(self, path, payload={}, headers={}):
        """"""
        base_url = current_app.get('MPESA_SANDBOX_URL') if current_app.debug else current_app.get('MPESA_PRODUCTION_URL')
        payloads = {
            'grant_type' : 'client_credentials'
        }.update(payload)
        return request(
            "GET", 
            f'{base_url}/{path}?{urllib.parse.urlencode(payloads)}', 
            headers = { 
                'Authorization': f'Bearer {self.authorization}' 
            }
        )

    def authorization(self, consumer_key, consumer_secret):
        """
        """
        bearer_token = base64.b64encode(f'{consumer_key}:{consumer_secret}')
        base_url = current_app.get('MPESA_SANDBOX_URL') if current_app.debug else current_app.get('MPESA_PRODUCTION_URL')
        payload = {
            'grant_type' : 'client_credentials'
        }
        return request(
            "GET", 
            f'{base_url}/generate?{urllib.parse.urlencode(payload)}', 
            headers = { 
                'Authorization': f'Bearer {bearer_token}' 
            }
        ).text.encode('utf8')

