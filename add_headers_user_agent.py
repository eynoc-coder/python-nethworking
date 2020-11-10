from urllib.request import Request

USER_AGENT = 'Mozilla/5.0 (Windows NT 5.1; rv:20.0) Gecko/20100101 Firefox/20.0'
URL = 'http://www.debian.org'

def add_header_user_agent():
    headers = {'Accept-Language' : 'nl', 'User-agent' : USER_AGENT}
    requests = Request(URL, headers=headers)
    print("Request headers :")
    for key, values in requests.header_items():
        print("%s: %s" %(key, values))


if __name__ == "__main__":
    add_header_user_agent()