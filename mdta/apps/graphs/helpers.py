from django.db import transaction
import pandas as pd

from mdta.apps.projects.models import Project, Module, VUID, Language
from mdta.apps.graphs.models import Node, NodeType

PAGE_NAME = "page name"
PROMPT_NAME = "prompt name"
PROMPT_TEXT = "prompt text"
STATE_NAME = "state name"


@transaction.atomic
def parse_out_promptmodulesandnodes(vuid, project_id):
    df = pd.read_excel(vuid.file.path)
    df.columns = map(str.lower, df.columns)
    df.drop_duplicates(subset=[PAGE_NAME, STATE_NAME], keep=False)
    project = Project.objects.get(pk=project_id)

    module_names = []
    no_language = False

    for i in df.index:
        try:
            pgname = (df[PAGE_NAME][i])
            pname = (df[PROMPT_NAME][i])
            ptext = (df[PROMPT_TEXT][i])
            stname = (df[STATE_NAME][i])
        except ValueError:
            return {"valid": False, "message": "Parser error, invalid headers"}

        try:
            pg = Module.objects.get(name=pgname, project=project)
        except Module.DoesNotExist:
            pg = Module(name=pgname, project=project)
            module_names.append(pg)
            pg.save()

        for d in df.columns:
            lang = Language.objects.filter(project=project)
            available_languages = lang.values_list('name', flat=True)
            if not available_languages.exists():
                no_language = True
                available_languages = ['English']
            for current_language in available_languages:
                if d.title().startswith(current_language):
                    language = d
        if no_language:
            verbiage = ptext

        if stname.startswith('prompt_'):
            type = NodeType.objects.get(name='Menu Prompt')
            stname = stname.replace('prompt_', ' ').strip(' ')
        elif stname.startswith(('say_', 'play_')):
            type = NodeType.objects.get(name='Play Prompt')
            stname = stname.replace('say_', ' ').strip(' ')
        try:
            nn = Node.objects.get(module__project=project, name=stname)
        except Node.DoesNotExist:
            keys = {current_language: {}}
            nn = Node(module=pg, name=stname, type=type, verbiage=keys)

        for current_language in available_languages:
            if current_language not in nn.verbiage.keys():
                nn.verbiage[current_language] = {}
            if current_language == 'English':
                verbiage = ptext
            else:
                verbiage = (df[language][i])
            if pname.find('_') != -1:
                pname = pname.replace('_', ' ').rstrip('123456789').strip(' ')

            # Assign verbiage from this row into correct field
            if pname.endswith('NI1'):
                nn.verbiage[current_language]['NoInput_1'] = verbiage
            elif pname.endswith('NI2'):
                nn.verbiage[current_language]['NoInput_2'] = verbiage
            elif pname.endswith('NM1'):
                nn.verbiage[current_language]['NoMatch_1'] = verbiage
            elif pname.endswith('NM2'):
                nn.verbiage[current_language]['NoMatch_2'] = verbiage
            else:
                nn.verbiage[current_language]['Initialprompt'] = verbiage

        nn.save()
        print(nn)
        print(nn.verbiage)

    return {"valid": True, "message": 'Handled'}


def upload_vuid(uploaded_file, user, project_id):
    vuid = VUID(filename=uploaded_file.name, file=uploaded_file, project_id=project_id, upload_by=user)
    vuid.save()

    result = parse_out_promptmodulesandnodes(vuid, project_id)
    if not result['valid']:
        vuid.delete()
        return result

    return dict(valid=True,
                message="File uploaded and modules and nodes were parsed successfully.")



