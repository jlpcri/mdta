from django.db import transaction
# from orderedset import OrderedSet
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
    for i, row in df.iterrows():

        try:
            pgname = (row[PAGE_NAME])
            pname = (row[PROMPT_NAME])
            ptext = (row[PROMPT_TEXT])
        except ValueError:
            return {"valid": False, "message": "Parser error, invalid headers"}

        for d in df.columns:
            lang = Language.objects.filter(project=project)
            values = lang.values_list('name')
            for v in values:
                plang = v
                if d.title().startswith(tuple(plang)):
                    language = d
                    lverbiage = (row[language])
                else:
                    no_language = ('English',)
                    print(no_language)

        stname = (row[STATE_NAME])

        try:
            pg = Module.objects.get(name=pgname, project=project)
        except Module.DoesNotExist:
            pg = Module(name=pgname, project=project)
            module_names.append(pg)
            pg.save()

        if pname.find('_') != -1:
            pname = pname.replace('_', ' ').rstrip('123456789').strip(' ')
        if stname.startswith('prompt_'):
            type = NodeType.objects.get(name='Menu Prompt')
            select = NodeType.objects.get(name='Language Select')
            stname = stname.replace('prompt_', ' ').strip(' ')
            verbiage_keys = [{'Language': plang,
                             'items': {
                                           'Verbiage': lverbiage,
                                           'TranslateVerbiage': ptext,
                                           'NoInput_1': "",
                                           'NoInput_2': "",
                                           'NoMatch_1': "",
                                           'NoMatch_2': "",
                             }
                             }]
        elif stname.startswith(('say_', 'play_')):
            type = NodeType.objects.get(name='Play Prompt')
            select = NodeType.objects.get(name='Language Select')
            stname = stname.replace('say_', ' ').strip(' ')
            verbiage_keys = [{'Language': plang,
                             'items': {
                                       'Verbiage': lverbiage,
                                       'TranslateVerbiage': ptext,
                             }
                             }]
        # print(stname)
        # print(pname)
        try:
            nn = Node.objects.get(module__project=project, name=stname)
        except Node.DoesNotExist:
            nn = Node(module=pg, name=stname, type=type, verbiage=verbiage_keys)

        print("{0} {1} == {2} {3}".format(type(nn.verbiage['Language']), nn.verbiage['Language'], type(
            no_language), no_language))

        if pname.endswith('NI1'):
            nn.verbiage['items']['NoInput_1'] = ptext
        elif pname.endswith('NI2'):
            nn.verbiage['NoInput_2'] = ptext
        elif pname.endswith('NM1'):
            nn.verbiage['NoMatch_1'] = ptext
        elif pname.endswith('NM2'):
            nn.verbiage['NoMatch_2'] = ptext

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



