import json
import urllib3
import urllib
import yaml
import requests
import glob
from .classes import MorphConfig
from . import morph_log

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def payloadHelper():

    """

    
    """
    print('test')


def pythonScript():
    """
    Create Python Task
    """
    print('test')

def fileTemplate_id_lookup(name):
    morphApi = MorphConfig()
    url = morphApi.templateLookup()
    header = morphApi.header_appJson()
    verifySSL = morphApi.verify()
    name = urllib.parse.quote(name)
    logger = morph_log.get_logger('fileTemp_lookup')
    url = url+name
    result = requests.request("GET", url, verify=verifySSL, headers=header)
    jsonData = result.json()
    print(json.dumps(jsonData))
    name = jsonData['groups'][0]['id']
    print(name)
    exit
    return name

def libraryTemplate(yaml_file):
    """
    Create file template task

    Currently a bug in the API.  Waiting until next version when the fix is in. 

    """
    logger = morph_log.get_logger('libraryTemplate')
    morphApi = MorphConfig()
    url = morphApi.tasks()
    header = morphApi.header_appJson()
    verifySSL = morphApi.verify()
    files = glob.glob(yaml_file)
    for file in files: 
        yaml_file = file
        logger.info('Current file: '+yaml_file)
        with open(yaml_file) as f:
            try:
                result=yaml.safe_load(f)
            except yaml.YAMLError as exc:
                logger.error(exc)
                logger.error('Was unable to load the file')
        for k, v in result['task'].items():
            
            name = result['task'][k]['name']
            code = result['task'][k]['code']
            type = result['task'][k]['type']
            executeTarget = result['task'][k]['executeTarget']
            templateId = fileTemplate_id_lookup(name)
            payload = json.dumps({
                'task': {
                    'name': name,
                    'taskType': {
                        'code': type
                    },
                    'taskOptions': {
                        'containerTemplate': templateId
                    },
                    'executeTarget': executeTarget 
                }
            })
    response = requests.request('POST', url, verify=verifySSL, headers=header, data=payload)


    print('test')

def shellScript(yaml_file, contentPackSelection):
    """
    Create Shell Script
    """
    logger = morph_log.get_logger('shellScript')
    morphApi = MorphConfig()
    url = morphApi.tasks()
    header = morphApi.authBearer_noContent()
    verifySSL = morphApi.verify()
    files = glob.glob(yaml_file)
    for file in files: 
        yaml_file = file 
        logger.info('Current file: '+yaml_file)
        with open(yaml_file) as f:
            try: 
                result=yaml.safe_load(f)
            except yaml.YAMLError as exc:
                logger.error(exc)
                logger.error('Was unable to load the file')
        for k, v in result['task'].items():
            name = result['task'][k]['name']
            code = result['task'][k]['code']
            taskType = result['task'][k]['taskType']
            resultType = result['task'][k]['resultType']
            scriptsourceType = result['task'][k]['scriptsourceType']
            sudo = result['task'][k]['sudo']
            executeTarget = result['task'][k]['executeTarget']
            retryable = result['task'][k]['retryable']
            allowCustomConfig = result['task'][k]['allowCustomConfig']
            filename = result['task'][k]['localFileName']
            logger.debug('Template file name: '+contentPackSelection+'/'+filename)
            localFileName = './'+contentPackSelection+'/'+filename
            payload = json.dumps({
                'task': {
                    'name': name,
                    'code': code,
                    'taskType': {
                        'code': taskType
                    },
                    'resultType': resultType,
                    'taskOptions':{
                        'shell.sudo': sudo
                    },
                    'file': {
                        'sourceType': scriptsourceType,
                        'content': open(localFileName, 'r').read()
                    },
                    'executeTarget': executeTarget,
                    'retryable': retryable,
                    'allowCustomConfig': allowCustomConfig
                }
            })
            response = requests.request('POST', url, verify=verifySSL, headers=header, data=payload)