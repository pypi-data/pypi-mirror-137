import requests

BASE_URL = "https://api.databaseci.com/v1/copy"


def get_response(request):
    r = requests.post(BASE_URL, json=request)

    r.raise_for_status()

    return r.json()
