import errno, os, requests, sys
from constants import *
# Manga web scraper.
s = requests.session()
def get(url):
    print('GET:   '+url)
    r = s.get(url)
    if r.status_code != 200:
        return r.status_code
    return r.content

def new_manga(name):
    # Makes a new directory for a new manga
    os.makedirs(MANGA_DIR+'/'+name)

def save_page(url, chapt, page, ext):
    filename = '0'*(4-len(str(chapt)))+str(chapt)+'_'+(2-len(str(page)))*'0'+str(page)+ext
    path = os.path.join(thispath, filename)
    if os.path.isfile(path):
        print("%s already exists, skipping" % path)
        return 200

    image = get(url)
    if type(image) == type(1) or image is None:
        return image
    
    with open(path, 'wb') as fh:
        print('CREATE: '+path)
        fh.write(image)
    return 200

def get_chapter(base_url, chapt):
    i = 1
    switch = False
    init = base_url + str(chapt) + '/'
    if chapt >= 200:
        ext = '.png'
    else:
        ext = '.jpg'
    while True:
        url = init + str(i) + ext
        resp = save_page(url, chapt, i, ext)
        if resp != 200:
            if switch:
                break
            ext = '.jpg' if ext == '.png' else '.png'
            switch = True
            i = i-1
        else:
            switch = False
        i = i+1

def get_range(base_url, start, end):
    for i in range(start, end+1):
        get_chapter(base_url, i)

# if __name__ =='__main__':
#     print("For this need to change settings inside file to change manga")
#     print("Change the base stuff in constants basically, this just does")
#     print("manga_folder_name and Start/end chapters")

name = "one_piece_color"
thispath = MANGA_DIR+'/'+ name
if not os.path.isdir(thispath):
    new_manga(name)
#     base_url = BASE_URL_KISS + BASE_ONE_PIECE
base_url = "https://cdn.mangahub.io/file/imghub/one-piece-colored/"
start = int(sys.argv[1]) # represents start chapter
end = int(sys.argv[2]) # represents end chapter
get_range(base_url, start, end)



