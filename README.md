# Booktoki Novel Scraper And Translator
## Overview
Ever wanted to read a Korean Web Novel, but you don't want to translate and nagivate on the site known as Booktoki?
Well, now you can simply find the booktoki link, Copy + Paste it and you are now scraping data from the website and automatically translating it to English!!!

Note: I have not figured out a way to bypass the Booktoki CAPTCHA, Cloudfare was easy, but Booktoki's is a letter/number recognition system. If the CAPTCHA appears it will break your script, so you must scroll up in the terminal and find the last chapter it was scraping and restart at that chapter and do the CAPTCHA yourself

## Features
TODO: insert screenshots

## How to use
1. Run command in terminal:
```console
python booktoki_scraper.py
```
1. OR double click booktoki_scraper.py file
2. Paste a booktoki link
3. Enter a starting chapter (Default is 0)
4. Enter an ending chapter (Default is latest release)
5. Enter your .txt document name
6. Watch out for any Booktoki CAPTCHAs
7. Check the 'output/' directory for your novel

## Dependencies
Must have a Webdriver installed, such as chromedriver.exe
SeleniumBase and it's dependencies
Googletrans and it's dependencies