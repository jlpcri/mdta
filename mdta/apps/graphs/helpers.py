from django.db import transaction
import pandas as pd

from mdta.apps.projects.models import Project, Module, VUID
from mdta.apps.graphs.models import Node

PAGE_NAME = "page name"
PROMPT_NAME = "prompt name"
PROMPT_TEXT = "prompt text"
# LANGUAGE = "language"
STATE_NAME = "state name"
DATE_CHANGED = "date changed"


@transaction.atomic
def parse_out_module_names(vuid, project_id):
    df = pd.read_excel(vuid.file.path)
    df.columns = map(str.lower, df.columns)
    project = Project.objects.get(pk=project_id)

    pgnames = (df[PAGE_NAME].unique())
    for p in pgnames:
        Module.objects.create(name=p, project=project)

    return {"valid": True, "message": 'Module \'{0}\' is added to \'{1}\''.format(p, project)}


@transaction.atomic
def parse_out_node_names(vuid):
    df = pd.read_excel(vuid.file.path)
    df.columns = map(str.lower, df.columns)
    pnames = (df[PROMPT_NAME])
    pnames = pnames.str.replace('_', ' ')
    pnames = pnames.str.rstrip('123456789').unique()

    for p in pnames:
        print(p)

    return {"valid": True, "message": 'Handled'}


def upload_vuid(uploaded_file, user, project_id):
    vuid = VUID(filename=uploaded_file.name, file=uploaded_file, project_id=project_id, upload_by=user)
    vuid.save()

    result = parse_out_module_names(vuid, project_id)
    if not result['valid']:
        vuid.delete()
        return result

    result = parse_out_node_names(vuid)
    if not result['valid']:
        vuid.delete()
        return result

    return dict(valid=True,
                message="File uploaded and parsed successfully.")



