import errno, os, requests, sys
from bs4 import BeautifulSoup
from constants import MANGA_DIR, BASE_URL
import threading
# Manga web scraper.
s = requests.session()

def get(url):
    print('GET:   '+url)
    r = s.get(url)
    if r.status_code != 200:
        return r.status_code
    return BeautifulSoup(r.content, 'html5lib')

def is_end(url):
    r = s.get(url)
    if r.status_code != 200:
        return True
    return False

def make_fname(page, chapt):
    return '0'*(4-len(str(chapt)))+str(chapt)+'_'+(2-len(str(page)))*'0'+str(page)+'.jpg'

def chapter_done(chapt):
    page = str(1)
    filename = make_fname(page, chapt)
    path = os.path.join(thispath, filename)
    if os.path.isfile(path):
        return True
    return False

def save_page(url, chapt, page):
    filename = make_fname(page, chapt)
    path = os.path.join(thispath, filename)
    if os.path.isfile(path):
        print("%s already exists, skipping" % path)
        return 200

    soup = get(url)
    if type(soup) == type(1) or soup is None:
        return soup
    try:
        url = soup.find(id='img')['src']
    except:
        return 404
    with open(path, 'wb') as fh:
        print('GET:  '+url)
        image = s.get(url).content
        print('CREATE: '+path)
        fh.write(image)
    return 200

class myThread(threading.Thread):
    def __init__(self, url, chapter, page):
        threading.Thread.__init__(self)
        self.chapter = chapter
        self.page = page
        self.url = url

    def run(self):
        res = save_page(self.url, self.chapter, self.page)
        return res


def new_manga(name):
    # Makes a new directory for a new manga
    os.makedirs(MANGA_DIR+'/'+name)

def get_chapter(base_url, chapt):
    if(chapter_done(chapt+1)):
        print "Chapter "+str(chapt)+" assumed done, skipping\n"
        return
    k = 1
    threads = []
    while True:
        urls = [base_url+'/'+str(chapt)+'/'+str(i) for i in range(k, k+5)]
        if(is_end(urls[0])):
            break
        for i in range(k, k+5):
            threads.append(myThread(urls[i%5-1], chapt, i))        
        for i in range(k-1, k+4):
            threads[i].start()
        k += 5

    for thread in threads:
        thread.join()

def get_range(base_url, start, end):
    for i in range(start, end+1):
        get_chapter(base_url, i)

if __name__ =='__main__':
    if len(sys.argv) < 5:
        print('Usage: python ' + sys.argv[0] + ' folder_name manga_url_name start end')
        print('Start and end are start/end chapters, manga_url_name is the name in the url for ur manga')
        print('Minus the chapter and page numbers')
        sys.exit(1)
    name = sys.argv[1]
    thispath = MANGA_DIR+'/'+name
    if not os.path.isdir(thispath):
        new_manga(name)
    base_url = BASE_URL + '/' + sys.argv[2]
    start = int(sys.argv[3]) # represents start chapter
    end = int(sys.argv[4]) # represents end chapter
    get_range(base_url, start, end)