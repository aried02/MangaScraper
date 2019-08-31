from bs4 import BeautifulSoup
import errno, os, requests, sys
s = requests.session()
def get(url):
    print('GET:   '+url)
    r = s.get(url)
    # if r.status_code != 200:
    #     return r.status_code
    return BeautifulSoup(r.content, 'html5lib')

print(get('https://ww4.readonepiece.com/chapter/one-piece-digital-colored-comics-chapter-001/'))