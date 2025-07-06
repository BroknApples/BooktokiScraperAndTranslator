# NovelScrape
## Overview
Ever wanted to read an untranslated web novel? Well, with this tool, you can!
Just simply find the link to the novel's chapter list page and check the preset scraper settings and choose the correct website, then simply press

# TODO: Fix the captcha issue by restarting at the last attempted chapter
Note: I have not figured out a way to bypass the Booktoki CAPTCHA, Cloudfare was easy, but Booktoki's is a letter/number recognition system. If the CAPTCHA appears it will break your script, so you must scroll up in the terminal and find the last chapter it was scraping and restart at that chapter and do the CAPTCHA yourself FOR NOW. Update coming soon!

## How to use
1. Double click 'novel_scrape.py' OR run this command in terminal:
```console
python novel_scrape.py
```
# TODO: Review these points

2. Paste a booktoki link
3. Enter a starting chapter (Default is 0)
4. Enter an ending chapter (Default is latest release)
5. Enter your .txt document name
6. Watch out for any Booktoki CAPTCHAs
7. Check the 'translations/' directory for your novel

## Dependencies
* Python 3.5 or later
* Must have a Webdriver installed, such as 'chromedriver.exe'
* Selenium and it's dependencies
* SeleniumBase and it's dependencies
* Googletrans and it's dependencies
* PyAutoGUI (Automatically installed by selenium)

## Notes
# TODO: Fill in later