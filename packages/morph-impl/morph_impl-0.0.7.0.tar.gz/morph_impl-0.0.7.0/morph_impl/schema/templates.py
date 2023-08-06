{
    'morpheusComponent': {
        'type': 'string',
        'required': True
    },
    'fileTemplate': {
        'valuesrules': {
        'required': True,
        'type': 'dict',
        'schema':{
            'name':{
                'required': True,
                'type': 'string'
            },
            'templatePhase':{
                'required': True,
                'type': 'string'
            },
            'fileName':{
                'required': True,
                'type': 'string'
            },
            'filePath':{
                'required': True,
                'type': 'string'
            },
            'fileOwner': {
                'required': True,
                'type': 'string'
            },
            'settingName':{
                'required': True,
                'type': 'string'
            },
            'settingCategory':{
                'required': True,
                'type': 'string'
            },
            'localFileName':{
                'required': True,
                'type': 'string'
            }
        }
        }
    }
}