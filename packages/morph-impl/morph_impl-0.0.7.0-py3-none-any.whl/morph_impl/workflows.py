import json
import urllib3
import yaml
import requests
import glob
from .classes import MorphConfig
from . import morph_log


def lookUpTaskId():
    print('Test')


def createProvisioningWF():
    print('create provisioning')


# i need to create a way for the user to input the workflows with the task and iterate. 




"""
curl -XPOST "$serverUrl/api/task-sets" \
  -H "Authorization: BEARER $accessToken" \
  -H "Content-Type: application/json" \
  -d '{"taskSet": {
    "name": "my workflow",
    "tasks": [
      {
        "taskId": 3
      },
      {
        "taskId": 8
      },
      {
        "taskId": 9,
        "taskPhase": "postProvision"
      }
    ]
  }}'







"""