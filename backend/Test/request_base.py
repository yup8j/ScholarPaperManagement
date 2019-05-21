import requests

base_url = "http://127.0.0.1"
port = 5000


def test(route, post_data):
    test_url = base_url + ":" + str(port) + route
    res = requests.post(url=test_url, data=post_data)
    print(res.text)
