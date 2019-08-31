# MangaScraper
I have a flight soon, and thought being able to read manga on it would be nice. So I built this super simple scraper to grab the images from how its formatted on mangareader.net and store them for me. Very easy to use. Just put your base url in constants.py, and the directory you want to put everything in (be absolute about it).

Call with command line as so:
```shell
python scrape.py <folder name to put manga in> <url_manga_name that the chapter and page numbers add to (e.g. one-piece)> <start chapter> <end chapter>
```
