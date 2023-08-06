import json
import yaml
import requests
from . import morph_log
import glob
from os import path
import os
from .classes import MorphConfig


def updateWhiteLabel (yaml_file):
    logger = morph_log.get_logger('uwhlabel')
    morphApi= MorphConfig()
    url = morphApi.whitelabel()
    header = morphApi.header_appJson()
    verifySSL = morphApi.verify()
    #headers = {'Content-Type': 'application/json','Authorization': 'Bearer ' +bearerToken}
    files = glob.glob(yaml_file)
    #url = baseURL+'/api/whitelabel-settings'
    for file in files:
        yaml_file = file
        logger.info('Current file: '+yaml_file)
        with open(yaml_file) as f:
            try:
                result = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                logger.error(exc)
                logger.error('Was unable to load the yaml file.')
        enabled = result['enabled']
        applianceName = result['applianceName']
        headerBgColor = result['headerBgColor']
        footerBgColor = result['footerBgColor']
        loginBgColor = result['loginBgColor']
        disableSupportMenu = result['disableSupportMenu']

        payload = json.dumps({"whitelabelSettings": {
                                "enabled": enabled,
                                "applianceName": applianceName,
                                "disableSupportMenu": disableSupportMenu,
                                "headerBgColor": headerBgColor,
                                "footerBgColor": footerBgColor,
                                "loginBgColor": loginBgColor}})
        whitelabelStatus = requests.request('PUT', url, verify=verifySSL, headers=header, data=payload)
        print(whitelabelStatus.text)

def updateLogoHeader(logoHeader):
    logger = morph_log.get_logger('ulogohead')
    morphApi= MorphConfig()
    url = morphApi.whitelabelimage()
    header = morphApi.imageWhiteLabel()
    verifySSL = morphApi.verify()
    #headers = {'Authorization': 'Bearer ' +bearerToken}
    #url = baseURL+'/api/whitelabel-settings/images'
    files = {'headerLogo.file' : open(logoHeader, 'rb')}
    payload = {}
    result = requests.request('POST', url, verify=verifySSL, headers=header, files=files, data=payload)
    logger.info(result.text)
def updateLogoFooter(logoFooter):
    logger = morph_log.get_logger('ulogofoot')
    morphApi= MorphConfig()
    url = morphApi.whitelabelimage()
    header = morphApi.imageWhiteLabel()
    verifySSL = morphApi.verify()
    #headers = {'Authorization': 'Bearer ' +bearerToken}
    #url = baseURL+'/api/whitelabel-settings/images'
    files = {'footerLogo.file' : open(logoFooter, 'rb')}
    payload = {}
    result = requests.request('POST', url, verify=verifySSL, headers=header, files=files, data=payload)
    logger.info(result.text)

def updateLogoLogin(logoLogin):
    logger = morph_log.get_logger('ulogolog')
    morphApi= MorphConfig()
    url = morphApi.whitelabelimage()
    header = morphApi.imageWhiteLabel()
    verifySSL = morphApi.verify()
    #headers = {'Authorization': 'Bearer ' +bearerToken}
    #url = baseURL+'/api/whitelabel-settings/images'
    files = {'loginLogo.file' : open(logoLogin, 'rb')}
    payload = {}
    result = requests.request('POST', url, verify=verifySSL, headers=header, files=files, data=payload)
    logger.info(result.text)




#    curl -XPOST "$serverUrl/api/whitelabel-settings/images" \
#  -H "Authorization: BEARER access_token" \
##  -F 'headerLogo.file=@filename.png;type=image/png' \
##  -F 'footerLogo.file=@filename.png;type=image/png' \
#  -F 'loginLogo.file=@filename.png;type=image/png' \
#  -F 'favicon.file=@filename.ico;type=image/ico'