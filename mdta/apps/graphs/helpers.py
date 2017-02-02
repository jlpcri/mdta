from datetime import datetime
# from itertools import izip, takewhile
# from django.conf import settings
# from django.utils import timezone
from django.contrib import messages
from django.db import transaction
import pandas as pd

from mdta.apps.projects.models import Project, Module, VUID


PAGE_NAME = "Page Name"
PROMPT_NAME = "Prompt Name"
PROMPT_TEXT = "Prompt Text"
# LANGUAGE = "language"
STATE_NAME = "State Name"
DATE_CHANGED = "Date Changed"

VUID_HEADER_NAME_SET = {
    PROMPT_NAME,
    PROMPT_TEXT,
    DATE_CHANGED
}


@transaction.atomic
def parse_out_module_names(vuid):
    df = pd.read_excel(vuid.file.path)
    mods = []

    pnames = list(set(df[PAGE_NAME].unique()))
    for p in pnames:
        print(p)
        # im = Project.create(project=module.project.name, name=module.name)
        # mods.append(im)
        # print(im)
        # im.save()

    return {"valid": True, "message": "Parsed file successfully"}

# @transaction.atomic
# def update_module_list(vuid, project, module):
#     p = Project.objects.get(pk=project)
#
#     return {"valid": True, "message": "Parsed file successfully"}


def upload_vuid(uploaded_file, user, project_id):
    vuid = VUID(filename=uploaded_file.name, file=uploaded_file, project_id=project_id, upload_by=user)
    vuid.save()

    result = parse_out_module_names(vuid)
    if not result['valid']:
        vuid.delete()
        return result

    return {"valid": True, "message": "File uploaded and parsed successfully"}


# def create_modules(vuid):
#     wb = load_workbook(vuid.file.path)
#     ws = wb.active
#     indexes = [ws.columns[0].index(x) for x in set(ws.columns[0])]
#     # uq = set(ws.columns[0])
#
#     for index in indexes:
#         yield (index, wb[index])
#
#     # for cell0bj in uq:
#     #     print(cell0bj.value)



