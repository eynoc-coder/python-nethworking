from urllib.request import urlopen
import re


def download_page(url):
    USER_AGENT = 'Mozilla/5.0 (Windows NT 5.1; rv:20.0) Gecko/20100101 Firefox/20.0'
    headers = {'Accept-Language': 'nl', 'User-agent': USER_AGENT}
    return urlopen(url, headers=headers).read().decode('utf-8')


def extract_links(page):
    link_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return link_regex.findall(page)


if __name__ == '__main__':
    target_url = 'http://www.packtpub.com'
    packtpub = download_page(target_url)
    links = extract_links(packtpub)
    for link in links:
        print(link)
