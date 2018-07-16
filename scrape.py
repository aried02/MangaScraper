import errno, os, requests, sys
from bs4 import BeautifulSoup
from constants import MANGA_DIR
# Manga web scraper.
s = requests.session()
def get(url):
    print('GET:   '+url)
    r = s.get(url)
    if r.status_code != 200:
        return r.status_code
    return BeautifulSoup(r.content, 'html5lib')

def new_manga(name):
    # Makes a new directory for a new manga
    os.makedirs(MANGA_DIR+'/'+name)

def save_page(url, chapt, page):
    filename = '0'*(4-len(str(chapt)))+str(chapt)+'_'+(2-len(str(page)))*'0'+str(page)+'.jpg'
    path = os.path.join(thispath, filename)
    if os.path.isfile(path):
        print("%s already exists, skipping" % path)
        return 200
    
    soup = get(url)
    if type(soup) == type(1):
        return soup
    url = soup.find(id='img')['src']
    with open(path, 'wb') as fh:
        print('GET:  '+url)
        image = s.get(url).content
        print('CREATE: '+path)
        fh.write(image)
    return 200

def get_chapter(base_url, chapt):
    i = 1
    while True:
        url = base_url+'/'+str(chapt)+'/'+str(i)
        resp = save_page(url, chapt, i)
        if resp != 200:
            break
        i = i+1

def get_range(base_url, start, end):
    for i in range(start, end+1):
        get_chapter(base_url, i)
    
if __name__ =='__main__':
    if len(sys.argv) < 5:
        print('Usage: python scrape.py n/e folder_name base_url start end')
        print('Start and end are start/end chapters, base_url is manga base')
        print('Minus the chapter and page numbers')
        sys.exit(1)
    opt = sys.argv[1] # pass 'n' for new manga, anything else for adding to existing
    name = sys.argv[2]
    thispath = MANGA_DIR+'/'+name
    if opt == 'n':
        new_manga(name)
    base_url = sys.argv[3]
    start = int(sys.argv[4]) # represents start chapter
    end = int(sys.argv[5]) # represents end chapter
    get_range(base_url, start, end)



