from django.db import transaction
import pandas as pd

from mdta.apps.projects.models import Project, Module, VUID, Language
from mdta.apps.graphs.models import Node, NodeType
from mdta.apps.testcases.constant_names import LANGUAGE_DEFAULT_NAME

PAGE_NAME = "page name"
PROMPT_NAME = "prompt name"
PROMPT_TEXT = "prompt text"
STATE_NAME = "state name"


@transaction.atomic
def parse_out_promptmodulesandnodes(vuid, project_id):
    # Setup and create dataframe for parsing
    df = pd.read_excel(vuid.file.path, keep_default_na=False, na_values=' ', convert_float=True)
    df.columns = map(str.lower, df.columns)
    df.columns = df.columns.fillna("")
    df.drop_duplicates(subset=[PAGE_NAME, STATE_NAME], keep=False)

    project = Project.objects.get(pk=project_id)

    # check and grab all languages set in project
    lang = Language.objects.filter(project=project)
    if lang:
        available_languages = lang.values_list('name', flat=True)
    else:
        available_languages = [LANGUAGE_DEFAULT_NAME]

    for i in df.index:
        try:
            module_name = (df[PAGE_NAME][i])
            prompt_name = (df[PROMPT_NAME][i])
            english_text = (df[PROMPT_TEXT][i])
            node_name = (df[STATE_NAME][i])
        except KeyError:
            return {"valid": False, "message": "Parser error, invalid headers. Please check them again."}

        # if current row is Bravo Path
        if not node_name:
            continue

        # check if module exists if not create it
        try:
            module = Module.objects.get(name=module_name, project=project)
        except Module.DoesNotExist:
            module = Module(name=module_name, project=project)
            module.save()

        # parse, clean, and create nodes
        if node_name.startswith('prompt_'):
            type = NodeType.objects.get(name='Menu Prompt')
            node_name = node_name.replace('prompt_', ' ').strip(' ')
            keys = {
                'Outputs': "",
                'OnFailGoTo': "",
                'NonStandardFail': "",
                'Default': ""
            }
        elif node_name.startswith(('say_', 'play_')):
            type = NodeType.objects.get(name='Play Prompt')
            node_name = node_name.replace('say_', ' ').strip(' ')
            keys = {
            }
        else:
            type = NodeType.objects.get(name='Play Prompt')
            keys = {}

        try:
            node = Node.objects.get(module__project=project, name=node_name)

            if type.name == 'Menu Prompt' and node.type.name != 'Menu Prompt':
                node.verbiage = {LANGUAGE_DEFAULT_NAME: {
                    'InitialPrompt': "",
                    'NoInput1': "",
                    'NoInput2': "",
                    'NoMatch1': "",
                    'NoMatch2': ""
                }}
                node.type = type
                node.save()
        except Node.DoesNotExist:
            if type.name == 'Menu Prompt':
                verbiage_keys = {LANGUAGE_DEFAULT_NAME: {
                    'InitialPrompt': "",
                    'NoInput1': "",
                    'NoInput2': "",
                    'NoMatch1': "",
                    'NoMatch2': ""
                }}
            else:
                verbiage_keys = {LANGUAGE_DEFAULT_NAME: {
                    'InitialPrompt': "",
                }}
            node = Node(module=module, name=node_name, type=type, verbiage=verbiage_keys, properties=keys)

        # work with the current_language key to setup the node verbiage
        for current_language in available_languages:
            # Add exception if node exists and its verbiage field is null
            try:
                if current_language not in node.verbiage.keys():
                    node.verbiage[current_language] = {
                        'InitialPrompt': "",
                        'NoInput1': "",
                        'NoInput2': "",
                        'NoMatch1': "",
                        'NoMatch2': ""
                    }
            except AttributeError:
                node.verbiage = {
                    current_language: {
                        'InitialPrompt': "",
                        'NoInput1': "",
                        'NoInput2': "",
                        'NoMatch1': "",
                        'NoMatch2': ""
                    }
                }

            if current_language == 'English':
                verbiage = str(english_text)
            elif current_language != 'English':
                verbiage = str("")
                for d in df.columns:
                    if d.title().startswith(current_language):
                        language = d
                        verbiage = str((df[language][i]))

            if prompt_name.find('_') != -1:
                prompt_name = prompt_name.replace('_', ' ').rstrip('123456789').strip(' ')
            # Assign verbiage from this row into correct field
            if prompt_name.endswith('NI1'):
                node.verbiage[current_language]['NoInput1'] += verbiage
            elif prompt_name.endswith('NI2'):
                node.verbiage[current_language]['NoInput2'] += verbiage
            elif prompt_name.endswith('NM1'):
                node.verbiage[current_language]['NoMatch1'] += verbiage
            elif prompt_name.endswith('NM2'):
                node.verbiage[current_language]['NoMatch2'] += verbiage
            else:
                node.verbiage[current_language]['InitialPrompt'] += verbiage
        try:
            node.save()
        except Exception as e:
            print(node, e)
            pass

    return {"valid": True, "message": 'Handled'}


def verify_vuid(vuid):
    df = pd.read_excel(vuid.file.path)
    df.columns = map(str.lower, df.columns)
    valid = False
    message = "Invalid file structure, unable to upload"
    if not df.empty:
        if not verify_vuid_headers(vuid):
            message = "Parser error, invalid headers. Please check them again."
        else:
            valid = True
            message = "Uploaded file successfully"
    elif df.empty:
        message = "No records in file, unable to upload"
    return {"valid": valid, "message": message}


def verify_vuid_headers(vuid):
    df = pd.read_excel(vuid.file.path)
    df.columns = map(str.lower, df.columns)
    try:
        df.drop_duplicates(subset=[PAGE_NAME, STATE_NAME], keep=False)
    except KeyError:
        return False
    return True


def upload_vuid(uploaded_file, user, project_id):
    vuid = VUID(filename=uploaded_file.name, file=uploaded_file, project_id=project_id, upload_by=user)
    vuid.save()

    result = verify_vuid(vuid)
    if not result['valid']:
        vuid.delete()
        return result

    result = parse_out_promptmodulesandnodes(vuid, project_id)
    if not result['valid']:
        vuid.delete()
        return result

    return dict(valid=True,
                message="File uploaded and modules and nodes were parsed successfully.")



