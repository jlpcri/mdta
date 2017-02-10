from django.db import transaction
from orderedset import OrderedSet
import pandas as pd

from mdta.apps.projects.models import Project, Module, VUID
from mdta.apps.graphs.models import Node

PAGE_NAME = "page name"
PROMPT_NAME = "prompt name"
PROMPT_TEXT = "prompt text"
# LANGUAGE = "language"
STATE_NAME = "state name"


@transaction.atomic
def parse_out_modulesandnodes(vuid, project_id):
    df = pd.read_excel(vuid.file.path)
    df.columns = map(str.lower, df.columns)
    project = Project.objects.get(pk=project_id)

    # mylist = []
    mydict = {}

    pgnames = (df[PAGE_NAME]).unique()
    pnames = (df[PROMPT_NAME])
    ptext = (df[PROMPT_TEXT])
    stnames = (df[STATE_NAME]).unique()

    for p in pgnames:
        Module.objects.create(name=p, project=project)

    for x in range(len(df)):
        pname = df.iloc[x, 1]
        ptext = df.iloc[x, 2]
        if pname.find('_') != -1:
            pname = pname.replace('_', ' ').rstrip('123456789')
        print(pname)
        mydict.setdefault(pname, [])
        mydict[pname].append(ptext)
    print(project, pgnames, mydict)

    m = vuid.project.modules
    print(m)

    n = vuid.project.nodes
    print(n)

    return {"valid": True, "message": 'Handled'}


def upload_vuid(uploaded_file, user, project_id):
    vuid = VUID(filename=uploaded_file.name, file=uploaded_file, project_id=project_id, upload_by=user)
    vuid.save()

    result = parse_out_modulesandnodes(vuid, project_id)
    if not result['valid']:
        vuid.delete()
        return result

    return dict(valid=True,
                message="File uploaded and parsed successfully.")



