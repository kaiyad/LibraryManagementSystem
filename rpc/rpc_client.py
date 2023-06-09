from typing import Any
from jsonrpcclient import request 
import requests

DEFAULT_URL = "http://localhost/jsonrpc:5001"

class ProxyMethod():
    def __init__(self, name, owner):
        self.name=name
        self.owner=owner

    def __call__(self, *args, **kwargs):
        if args and kwargs:
            raise Exception("Json RPC can not do positional and keyword argument in same call")
        return self.owner.call_json_rpc(self.name)

class RPC_Client():
    """"""
    URL = "http://localhost:5001"
    def __init__(self, URL: str=DEFAULT_URL, request=None):
        pass
    
    def __getattr__(self, __name: str) -> Any:
        proxy = ProxyMethod(__name, self)
        setattr(self, __name, proxy)
        return proxy

    def call_json_rpc(self, method):
        response = requests.post(url=self.URL, json=request("handle_request", [method]))
        return response.json()['result']


if __name__ == '__main__':
    client = RPC_Client()
    print(client.list_books())
