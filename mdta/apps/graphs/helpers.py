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
    languages = []
    verbiage = []

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
            values = lang.values_list('name', flat=True)
            if not values.exists():
                no_language = True
                values = ['English']
            for v in values:
                if d.title().startswith(v):
                    language = d
        if no_language:
            verbiage = ptext

        for v in values:
            plang = v
            languages.append(v)
            if plang == 'English':
                verbiage = ptext
            else:
                verbiage = (df[language][i])
            keys = {plang: {
                'Initialprompt': verbiage,
            }
            }
            print(keys)
        if stname.startswith('prompt_'):
            type = NodeType.objects.get(name='Menu Prompt')
            stname = stname.replace('prompt_', ' ').strip(' ')
        elif stname.startswith(('say_', 'play_')):
            type = NodeType.objects.get(name='Play Prompt')
            stname = stname.replace('say_', ' ').strip(' ')
        try:
            nn = Node.objects.get(module__project=project, name=stname)
        except Node.DoesNotExist:
            nn = Node(module=pg, name=stname, type=type, verbiage=keys)

        if pname.find('_') != -1:
            pname = pname.replace('_', ' ').rstrip('123456789').strip(' ')
        if pname.endswith('NI1'):
            nn.verbiage[plang]['NoInput_1'] = verbiage
        elif pname.endswith('NI2'):
            nn.verbiage[plang]['NoInput_2'] = verbiage
        elif pname.endswith('NM1'):
            nn.verbiage[plang]['NoMatch_1'] = verbiage
        elif pname.endswith('NM2'):
            nn.verbiage[plang]['NoMatch_2'] = verbiage

        nn.save()
        print(nn)
        # print(nn.verbiage)

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



