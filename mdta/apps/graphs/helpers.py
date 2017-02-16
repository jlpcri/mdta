from django.db import transaction
from orderedset import OrderedSet
import pandas as pd

from mdta.apps.projects.models import Project, Module, VUID
from mdta.apps.graphs.models import Node, NodeType

PAGE_NAME = "page name"
PROMPT_NAME = "prompt name"
PROMPT_TEXT = "prompt text"
# LANGUAGE = "language"
STATE_NAME = "state name"

# pnames = (df[PROMPT_NAME])
# ptext = (df[PROMPT_TEXT])


@transaction.atomic
def parse_out_modules_names(vuid, project_id):
    df = pd.read_excel(vuid.file.path)
    df.columns = map(str.lower, df.columns)
    df.drop_duplicates(subset=[PAGE_NAME, STATE_NAME], keep=False)
    project = Project.objects.get(pk=project_id)

    # pgnames = (df[PAGE_NAME])

    #
    # for pg in pgnames:
    #     try:
    #         mn = Module.objects.get(name=pg, project=project)
    #     except Module.DoesNotExist:
    #         mn = Module(name=pg, project=project)
    #         module_names.append(mn)
    #         mn.save()
    #
    # print(module_names)

    module_names = []
    words = []
    text = {}

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
        elif stname.startswith('say_'):
            stname = NodeType.objects.get(name='Play Prompt')
            keys = {'Verbiage': verbiage,
                    'TranslateVerbiage': ""
                    }
        elif stname.startswith('play_'):
            stname = NodeType.objects.get(name='Play Prompt')
            keys = {'Verbiage': verbiage,
                    'TranslateVerbiage': ""
                    }
        # words.append(stname)
        stname.save()
        try:
            nn = Node.objects.get(module__project=project, name=pname)
        except Node.DoesNotExist:
            nn = Node(module=pg, name=pname, type=stname, properties=keys)
        nn.save()
        print(nn)

    return {"valid": True, "message": 'Handled'}


# @transaction.atomic
# def parse_out_node_names(vuid):
#     df = pd.read_excel(vuid.file.path)
#     df.columns = map(str.lower, df.columns)
#
#     mylist = []
#
#     pnames = (df[PROMPT_NAME])
#     if pnames.str.find('_').any() != -1:
#         pnames = pnames.str.replace('_', ' ')
#
#     for p in pnames:
#         if p.find(' ') != -1:
#             p = p.rstrip('123456789')
#         mylist.append(p.strip())
#         mylist = list(OrderedSet(mylist))
#
#     print(mylist)
#
#     for my in mylist:
#         print(my)
#
#     return {"valid": True, "message": 'Handled'}

# @transaction.atomic
# def parse_out_verbiage(vuid):
#     df = pd.read_excel(vuid.file.path)
#     df.columns = map(str.lower, df.columns)
#     ptext = (df[PROMPT_TEXT])
#
#     for pt in ptext:
#         print(pt)
#
#     return {"valid": True, "message": 'Handled'}


# @transaction.atomic
# def parse_out_node_types(vuid):
#     df = pd.read_excel(vuid.file.path)
#     df.columns = map(str.lower, df.columns)
#
#     stnames = (df[STATE_NAME]).unique()
#     node_types = []
#
#     for s in stnames:
#         if s.startswith('prompt_'):
#             s = 'Menu Prompt'
#         elif s.startswith('say_'):
#             s = 'Play Prompt'
#         elif s.startswith('play_'):
#             s = 'Play Prompt'
#         node_types.append(s)
#     print(node_types)
#
#     return {"valid": True, "message": 'Handled'}


def upload_vuid(uploaded_file, user, project_id):
    vuid = VUID(filename=uploaded_file.name, file=uploaded_file, project_id=project_id, upload_by=user)
    vuid.save()

    result = parse_out_modules_names(vuid, project_id)
    if not result['valid']:
        vuid.delete()
        return result

    # result = parse_out_node_names(vuid)
    # if not result['valid']:
    #     vuid.delete()
    #     return result

    # result = parse_out_verbiage(vuid)
    # if not result['valid']:
    #     vuid.delete()
    #     return result

    # result = parse_out_node_types(vuid)
    # if not result['valid']:
    #     vuid.delete()
    #     return result

    return dict(valid=True,
                message="File uploaded and parsed successfully.")



