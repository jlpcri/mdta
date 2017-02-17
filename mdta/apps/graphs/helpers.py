from django.db import transaction
# from orderedset import OrderedSet
import pandas as pd

from mdta.apps.projects.models import Project, Module, VUID
from mdta.apps.graphs.models import Node, NodeType

PAGE_NAME = "page name"
PROMPT_NAME = "prompt name"
PROMPT_TEXT = "prompt text"
# LANGUAGE = "language"
STATE_NAME = "state name"


@transaction.atomic
def parse_out_promptmodulesandnodes(vuid, project_id):
    df = pd.read_excel(vuid.file.path)
    df.columns = map(str.lower, df.columns)
    df.drop_duplicates(subset=[PAGE_NAME, STATE_NAME], keep=False)
    project = Project.objects.get(pk=project_id)

    module_names = []
    for x in range(len(df)):
        pgname = df.iloc[x, 0]
        stname = df.iloc[x, 3]
        pname = df.iloc[x, 1]
        verbiage = df.iloc[x, 2]
        try:
            pg = Module.objects.get(name=pgname, project=project)
        except Module.DoesNotExist:
            pg = Module(name=pgname, project=project)
            module_names.append(pg)
            pg.save()

        if pname.find('_') != -1:
            pname = pname.replace('_', ' ').rstrip('123456789')

        if stname.startswith('prompt_'):
            stname = NodeType.objects.get(name='Menu Prompt')
            keys = {'Verbiage': verbiage,
                    'TranslateVerbiage': "",
                    'Outputs': "",
                    'NoInput_1': "",
                    'NoInput_2': "",
                    'NoMatch_1': "",
                    'NoMatch_2': "",
                    'OnFailGoTo': "",
                    'NonStandardFail': "",
                    'Default': ""
                   }
        elif stname.startswith(('say_', 'play_')):
            stname = NodeType.objects.get(name='Play Prompt')
            keys = {'Verbiage': verbiage,
                    'TranslateVerbiage': ""
                    }
        stname.save()
        try:
            nn = Node.objects.get(module__project=project, name=pname)
        except Node.DoesNotExist:
            nn = Node(module=pg, name=pname, type=stname, properties=keys)
        nn.save()
        print(nn)

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



