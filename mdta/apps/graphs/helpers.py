from datetime import datetime
# from itertools import izip, takewhile
# from django.conf import settings
# from django.utils import timezone
from openpyxl import load_workbook
import unicodecsv
from django.db import transaction

from mdta.apps.projects.models import Project, Module, VUID, Language


PAGE_NAME = "page name"
PROMPT_NAME = "prompt name"
PROMPT_TEXT = "prompt text"
LANGUAGE = "language"
STATE_NAME = "state name"
DATE_CHANGED = "date changed"

VUID_HEADER_NAME_SET = {
    PROMPT_NAME,
    PROMPT_TEXT,
    DATE_CHANGED
}


# def make_filename(path, name):
#     if path.endswith('/') and name.startswith('/'):
#         return "{0}{1}".format(path[:-1], name)
#     elif path.endswith('/') or name.startswith('/'):
#         return "{0}{1}".format(path, name)
#     return "{0}/{1}".format(path, name)


@transaction.atomic
def parse_vuid(vuid):
    wb = load_workbook(vuid.file.path)
    ws = wb.active

    headers = [str(i.value).lower() for i in ws.rows[0]]
    try:
        prompt_name_i = headers.index(PROMPT_NAME)
        prompt_text_i = headers.index(PROMPT_TEXT)
        date_changed_i = headers.index(DATE_CHANGED)
    except ValueError:
        return {"valid": False, "message": "Parser error, invalid headers"}

    no_language = False
    try:
        language_i = headers.index(LANGUAGE)
    except ValueError:
        no_language = True

    for w in ws.rows[2:]:
        try:
            if no_language:
                language = Language.objects.get(project=vuid.project, name=str('english'))
            elif w[language_i].value is not None:
                language = Language.objects.get(project=vuid.project, name=str(w[language_i].value).strip().lower())
            else:
                language = Language.objects.get(project=vuid.project, name=str('english'))
        except Language.DoesNotExist:
            if no_language:
                language = Language(project=vuid.project, name=str('english'))
            else:
                language = Language(project=vuid.project, name=str(w[language_i].value).strip().lower())
            language.save()
        except Language.MultipleObjectsReturned:
            return {"valid": False, "message": "Parser error, multiple languages returned"}

        name = str(w[prompt_name_i].value).strip()

    return {"valid": True, "message": "Parsed file successfully"}


def upload_vuid(uploaded_file, user, project_id):
    vuid = VUID(filename=uploaded_file.name, file=uploaded_file, project_id=project_id, upload_by=user)
    vuid.save()

    result = parse_vuid(vuid)
    if not result['valid']:
        vuid.delete()
        return result

    return {"valid": True, "message": "File uploaded and parsed successfully"}


