from ruamel.yaml import YAML
import sys

def groups_config_create():
    # Initialize the YAML parser/dumper.
    yaml = YAML()
    yaml.default_flow_style = False
    total_groups = int(input('How many total groups? \n'))
    # Initialize a new dictionary to hold the groups.
    groups = {}
    for i in range(1, total_groups + 1):
        group = {}
        print(f'Data for group #{i}')
        for field in ['name', 'description', 'location', 'code']:
            fields = input(f'\tEnter {field}: ')
            group[field] = fields
        groups[f'group{i}'] = group
    data = {'morpheusComponent': 'groups', 'groups': groups}
    print('\n')
    print('# Start of Config File\n')
    yaml.dump(data, sys.stdout)
    print('\n# End of Config File')

def inputs_config_create():
    yaml = YAML()
    yaml.default_flow_style = False
    total_inputs = int(input('How many total input? \n'))
    # Initialize a new dictionary to hold the groups.
    inputs = {}
    for i in range(1, total_inputs + 1):
        inputv = {}
        print(f'Data for input #{i}')
        for field in ['name', 'type', 'description', 'fieldName', 'fieldLabel']:
            fields = input(f'\tEnter {field}: ')
            inputv[field] = fields
        inputs[f'input{i}'] = inputv
    data = {'morpheusComponent': 'inputs', 'inputs': inputs}
    print('\n')
    print('# Start of Config File\n')
    yaml.dump(data, sys.stdout)
    print('\n# End of Config File')

def templates_config_create():
    yaml = YAML()
    yaml.default_flow_style = False
    total_fileTemplates = int(input('How many total file templates? \n'))
    # Initialize a new dictionary to hold the groups.
    fileTemplates = {}
    for i in range(1, total_fileTemplates + 1):
        fileTemp = {}
        print(f'Data for template #{i}')
        for field in ['name', 'templatePhase', 'fileName', 'filePath', 'fileOwner', 'settingName', 'settingCategory', 'localFileName']:
            fields = input(f'\tEnter {field}: ')
            fileTemp[field] = fields
        fileTemplates[f'template{i}'] = fileTemp
    data = {'morpheusComponent': 'templates', 'fileTemplate': fileTemplates}
    print('\n')
    print('# Start of Config File\n')
    yaml.dump(data, sys.stdout)
    print('\n# End of Config File')

if __name__ == '__main__':

    conGenSelect = input('Select the type of config: ') 
    if conGenSelect == 'groups':
        groups_config_create()
    elif conGenSelect == 'inputs':
        inputs_config_create()
    elif conGenSelect == 'templates':
        templates_config_create()