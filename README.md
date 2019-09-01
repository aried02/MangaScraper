# MangaScraper
I have a flight soon, and thought being able to read manga on it would be nice. So I built this somewhat simple scraper to grab the images from how its formatted on mangareader.net and store them for me, now with concurrent option :). Very easy to use. Just put your base url (https://www.mangareader.net for mangareader) in constants.py, and the directory you want to put everything in (be absolute about it).

Call with command line as so:
```shell
python <program_to_run> <folder name to put manga in> <url_manga_name (e.g. one-piece, hunter-x-hunter)> <start chapter> <end chapter>
```
