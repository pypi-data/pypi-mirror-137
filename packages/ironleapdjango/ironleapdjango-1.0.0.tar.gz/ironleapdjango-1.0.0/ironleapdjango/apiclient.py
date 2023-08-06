import requests
from .schemas import json_serialize


class ApiClient(object):
    def __init__(self, app_key, uri):
        self.uri = uri
        self.headers = {
            'content-type': 'application/json; charset=utf-8',
            'X-Ironleap-Application-ID': app_key,
        }

    def post_events_batch(self, batch):
        resp = requests.post(self.uri, headers=self.headers, data=json_serialize(batch))
        if (resp.status_code < 200) or (resp.status_code > 208):
            raise Exception("HTTP response suggests error")
