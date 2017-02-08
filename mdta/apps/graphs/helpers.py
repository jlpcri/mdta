from django.db import transaction
from collections import OrderedDict
import pandas as pd

from mdta.apps.projects.models import Project, Module, VUID
from mdta.apps.graphs.models import Node

PAGE_NAME = "page name"
PROMPT_NAME = "prompt name"
PROMPT_TEXT = "prompt text"
# LANGUAGE = "language"
STATE_NAME = "state name"



# @transaction.atomic
# def parse_out_module_names(vuid, project_id):
#     df = pd.read_excel(vuid.file.path)
#     df.columns = map(str.lower, df.columns)
#     project = Project.objects.get(pk=project_id)
#
#     pgnames = (df[PAGE_NAME].unique())
#     for p in pgnames:
#         Module.objects.create(name=p, project=project)
#
#     return {"valid": True, "message": 'Module \'{0}\' is added to \'{1}\''.format(p, project)}


@transaction.atomic
def parse_out_node_names(vuid):
    df = pd.read_excel(vuid.file.path)
    df.columns = map(str.lower, df.columns)
    mylist = []

    pnames = (df[PROMPT_NAME])
    if pnames.str.find('_').any() != -1:
        pnames = pnames.str.replace('_', ' ')
        # if pnames.str.find(' ').any() != -1:
        #     pnames = pnames.str.rstrip('123456789').unique()

    for p in pnames:
        if p.find(' ') != -1:
            p = p.rstrip('123456789')
        mylist.append(p.strip())
        mylist = list(set(mylist))
        pnames.to_csv("media/file_unique_valuesALL.csv")
        print(mylist)

    return {"valid": True, "message": 'Handled'}


@transaction.atomic
def parse_out_node_types(vuid):
    df = pd.read_excel(vuid.file.path)
    df.columns = map(str.lower, df.columns)
    m = vuid.project.modules
    print(m)
    n = vuid.project.nodes
    print(n)

    stnames = (df[STATE_NAME]).unique()
    for st in stnames:

        print(st)

    return {"valid": True, "message": 'Handled'}


@transaction.atomic
def parse_out_verbiage(vuid):
    df = pd.read_excel(vuid.file.path)
    df.columns = map(str.lower, df.columns)
    ptext = (df[PROMPT_TEXT])

    for pt in ptext:
        print(pt)

    return {"valid": True, "message": 'Handled'}


def upload_vuid(uploaded_file, user, project_id):
    vuid = VUID(filename=uploaded_file.name, file=uploaded_file, project_id=project_id, upload_by=user)
    vuid.save()

    # result = parse_out_module_names(vuid, project_id)
    # if not result['valid']:
    #     vuid.delete()
    #     return result

    result = parse_out_node_names(vuid)
    if not result['valid']:
        vuid.delete()
        return result

    result = parse_out_verbiage(vuid)
    if not result['valid']:
        vuid.delete()
        return result

    result = parse_out_node_types(vuid)
    if not result['valid']:
        vuid.delete()
        return result

    return dict(valid=True,
                message="File uploaded and parsed successfully.")



