# NovelScrape
## Overview
Ever wanted to read an untranslated web novel? Well, with this tool, you can!
Just simply find the link to the novel's chapter list page and check the preset scraper settings and choose the correct website, then simply press


## Dependencies
### For Help with setting up these dependencies, go to the 'Setup' section
* Python 3.5 or later
* A chromium webdriver, such as 'chromedriver.exe'
* PySide6
* Selenium
* SeleniumBase
* deep-translator


## Notes
1. As with most python projects, creating a virtual environment is recommended
2. There are two versions, 'novel_scrape.py' which runs in a gui, and 'novel_scrape_console.py' which runs solely in the terminal
### TODO: Fix the captcha issue by restarting at the last attempted chapter
3. I have not figured out a way to bypass the Booktoki CAPTCHA, Cloudfare was easy, but Booktoki's is a letter/number recognition system. If the CAPTCHA appears it will break your script, so you must scroll up in the terminal and find the last chapter it was scraping and restart at that chapter and do the CAPTCHA yourself FOR NOW. Update coming soon!


## Setup
#### Installing a webdriver
### TODO: FINISH LATER

#### Installing packages
* Run 'setup.py' which checks and installs the required packages to run this program OR run:
```console
pip install PySide6
pip install selenium
pip install seleniumbase
pip install deep-translator
```


## How to use
### Option One -- Run Using File Explorer
1. Double click 'novel_scrape.py', 'novel_scrape_console.py',
### TODO: Explain how to use the gui application

### Option One -- Run Using Command Prompt
1. Run ONE of two commands:
```console
python novel_scrape.py
```
OR
```console
python novel_scrape_console.py
```
2. Paste a booktoki link
3. Enter a starting chapter (Default is 1)
4. Enter an ending chapter (Default is latest release)
5. Enter your translation directory
5. Enter 'y' to start OR 'n' to close
6. Wait until the script completes AND watch out for any Booktoki CAPTCHAs
7. Check the 'translations/' directory for your novel