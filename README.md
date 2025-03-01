# Booktoki Novel Scraper And Translator
## Overview
Ever wanted to read a Korean Web Novel, but you don't want to translate and nagivate on the site known as Booktoki?
Well, now you can simply find the booktoki link, Copy + Paste it and you are now scraping data from the website and automatically translating it to English!!!

Note: I have not figured out a way to bypass the Booktoki CAPTCHA, Cloudfare was easy, but Booktoki's is a letter/number recognition system. If the CAPTCHA appears it will break your script, so you must scroll up in the terminal and find the last chapter it was scraping and restart at that chapter and do the CAPTCHA yourself

## How to use
1. Run command in terminal OR double click booktoki_scraper.py file:
```console
python booktoki_scraper.py
```
2. Paste a booktoki link
3. Enter a starting chapter (Default is 0)
4. Enter an ending chapter (Default is latest release)
5. Enter your .txt document name
6. Watch out for any Booktoki CAPTCHAs
7. Check the 'output/' directory for your novel

## Dependencies
* Must have a Webdriver installed, such as chromedriver.exe
* SeleniumBase and it's dependencies
* Googletrans and it's dependencies

## Notes
If this script doesn't work try these:
1. Inspect element on a booktoki novel chapter and look for the articleBody element and search for where the chapter data is stored and check to see if it is 'novel_content'. If it isn't, modify the 'html_id' string at the top of the main() function
2. Inspect element on a booktoki novel's page's chapter list and compare it's XPath to 'data-index='. If it isn't the same, modify the getInitialChapterUrl() function with the updated XPath
3. Inspect element on a booktoki novel chapter's next arrow and compare it's class to 'btn-resource.btn-next.at-tip'. If it isn't the same modify the "btn-resource.btn-next.at-tip" part of findNextChapterUrl() to the updated class name