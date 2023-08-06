{
    'morpheusComponent': {
        'type': 'string',
        'required': True
    },
    'cypher': {
        'valuesrules': {
        'required': True,
        'type': 'dict',
        'schema':{
            'name':{
                'required': True,
                'type': 'string'
            },
            'secret':{
                'required': True,
                'type': 'string'
            }
        }
        }
    }
}