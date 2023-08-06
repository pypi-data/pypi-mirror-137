{
    'morpheusComponent': {
        'type': 'string',
        'required': True
    },
    'inputs': {
        'valuesrules': {
        'required': True,
        'type': 'dict',
        'schema':{
            'name':{
                'required': True,
                'type': 'string'
            },
            'type':{
                'required': True,
                'type': 'string'
            },
            'description':{
                'required': True,
                'type': 'string'
            },
            'fieldName': {
                'required': True,
                'type': 'string'
            },
            'fieldLabel':{
                'required': True,
                'type': 'string'
            }
        }
        }
    }        
}