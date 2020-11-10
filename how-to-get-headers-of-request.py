from urllib.request import urlopen

url = input("Enter the URL:")
http_response = urlopen(url)
if http_response.code == 200:
    print(http_response.headers)
    for key, value in http_response.getheaders():
        print(key, value)