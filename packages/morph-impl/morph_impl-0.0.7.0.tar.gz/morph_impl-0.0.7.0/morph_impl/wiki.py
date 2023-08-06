import requests
import json
import glob
from . import morph_log
import urllib
from .classes import MorphConfig
import os


def checkWikiEntry(title):
    # need to check to ensure the wiki article doesn't exist or does it. 
    logger = morph_log.get_logger('getwiki')
    morphApi = MorphConfig()
    urlSearch = morphApi.searchWiki()
    new_string = title[1:]
    new_string = new_string.rstrip()
    print(new_string)
    wikiTitle = urllib.parse.quote(new_string)
    logger.info('Wiki Title '+wikiTitle)
    url = urlSearch+new_string
    header = morphApi.header_appJson()
    verifySSL = morphApi.verify()
    result = requests.request('GET', url, verify=verifySSL, headers=header)
    print(result.text)
    return result
   # print('test')

def addWikiEntry(file):
    logger = morph_log.get_logger('wiki')
    files = glob.glob(file)
    morphApi = MorphConfig()
    url = morphApi.addWiki()
    header = morphApi.authBearer_noContent()
    verifySSL = morphApi.verify()
    for file in files: 
        wiki = file
        with open(wiki, "r") as file:
            first_line = file.readline()
            title = first_line.translate({ord(i): None for i in '#'})
            checkTitle = checkWikiEntry(title)
            checkTitle = json.loads(checkTitle.text)
        if len(checkTitle['pages']) == 0:
            logger.info('Page not found')
            logger.info('Wiki will be created')
            payload = json.dumps({
                'page': {
                    'name': title,
                    'content': open(wiki, "r").read()
                }
            })
            requests.request('POST', url, verify=verifySSL, headers=header, data=payload)
        else:
            logger.info('Wiki Found - Skipping...')