from datetime import datetime
# from itertools import izip, takewhile
# from django.conf import settings
# from django.utils import timezone
from django.contrib import messages
from django.db import transaction
import pandas as pd

from mdta.apps.projects.models import Project, Module, VUID


PAGE_NAME = "page name"
PROMPT_NAME = "prompt name"
PROMPT_TEXT = "prompt text"
# LANGUAGE = "language"
STATE_NAME = "state name"
DATE_CHANGED = "date changed"

VUID_HEADER_NAME_SET = {
    PROMPT_NAME,
    PROMPT_TEXT,
    DATE_CHANGED
}


@transaction.atomic
def parse_out_module_names(vuid, project_id):
    df = pd.read_excel(vuid.file.path)
    project = Project.objects.get(pk=project_id)
    df.columns = map(str.lower, df.columns)

    pnames = list(set(df[PAGE_NAME].unique()))

    for p in pnames:
        Module.objects.create(name=p, project=project)

    return {"valid": True, "message": 'Module \'{0}\' is added to \'{1}\''.format(p, project)}


def upload_vuid(uploaded_file, user, project_id):
    vuid = VUID(filename=uploaded_file.name, file=uploaded_file, project_id=project_id, upload_by=user)
    vuid.save()

    result = parse_out_module_names(vuid, project_id)
    if not result['valid']:
        vuid.delete()
        return result

    return dict(valid=True,
                message="File uploaded and parsed successfully.")



