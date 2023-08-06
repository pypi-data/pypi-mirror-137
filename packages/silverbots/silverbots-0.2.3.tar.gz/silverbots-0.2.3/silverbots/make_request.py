import requests


def make_request(url, json=None, headers=None, method="post"):
    if method.lower() == "post":
        return requests.post(url, json=json, headers=headers)
    elif method.lower() == "get":
        return requests.get(url, json=json, headers=headers)

