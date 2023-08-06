"""
Purpose of this script - 

Handle task creation of custom scripts.  
Handle file imports of custom templates. 

"""
import json
import yaml
import requests
import os
import glob
from . import morph_log
import urllib
from .classes import MorphConfig


def create_Template_fromCP(yaml_file, contentPackSelection):
    logger = morph_log.get_logger('crtmpFromcp')
    morphApi= MorphConfig()
    url = morphApi.fileTemplate()
    header = morphApi.authBearer_noContent()
    verifySSL = morphApi.verify()
    #print('test')
    #headers = {'Authorization': 'Bearer ' +bearerToken}  #'Content-Type': 'application/json',
    files = glob.glob(yaml_file)
    #url = baseURL+'/api/library/container-templates'
    for file in files:
        yaml_file = file
        logger.info('Current file: '+yaml_file)
        with open(yaml_file) as f:
            try:
                result=yaml.safe_load(f)
            except yaml.YAMLError as exc:
                logger.error(exc)
                logger.error('Was unable to load the yaml file')
        for k, v in result['fileTemplate'].items():
            name = result['fileTemplate'][k]['name']
            templatePhase = result['fileTemplate'][k]['templatePhase']
            fileName = result['fileTemplate'][k]['fileName']
            filePath = result['fileTemplate'][k]['filePath']
            fileOwner = result['fileTemplate'][k]['fileOwner']
            settingName = result['fileTemplate'][k]['settingName']
            settingCategory = result['fileTemplate'][k]['settingCategory']
            filename = result['fileTemplate'][k]['localFileName']
            logger.debug('Template file name: '+contentPackSelection+'/'+filename)
            localFileName = './'+contentPackSelection+'/'+filename
            payload = json.dumps({
                'containerTemplate':{
                    'templatePhase': templatePhase,
                    'name': name,
                    'fileName': fileName,
                    'filePath': filePath,
                    'fileOwner': fileOwner,
                    'settingName': settingName,
                    'settingCategory': settingCategory,
                    'template': open(localFileName, "r").read()
                }
            })
            response = requests.request('POST', url, verify=verifySSL, headers=header, data=payload)
            #print(response.text)
           # #print(payload)