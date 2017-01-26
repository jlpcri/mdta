from datetime import datetime
# from itertools import izip, takewhile
# from django.conf import settings
# from django.utils import timezone
from openpyxl import load_workbook
# import pysftp
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


def make_filename(path, name):
    if path.endswith('/') and name.startswith('/'):
        return "{0}{1}".format(path[:-1], name)
    elif path.endswith('/') or name.startswith('/'):
        return "{0}{1}".format(path, name)
    return "{0}/{1}".format(path, name)


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

    v = unicode(ws['A2'].value).strip()
    # if endswith '/', remove it
    if v[-1] == '/':
        v = v[:-1]
    i = v.find('/')
    path = v[i:].strip()
    slots = []

    for w in ws.rows[2:]:
        try:
            if no_language:
                language = Language.objects.get(project=vuid.project, name=unicode('english'))
            elif w[language_i].value is not None:
                language = Language.objects.get(project=vuid.project, name=unicode(w[language_i].value).strip().lower())
            else:
                language = Language.objects.get(project=vuid.project, name=unicode('english'))
        except Language.DoesNotExist:
            if no_language:
                language = Language(project=vuid.project, name=unicode('english'))
            else:
                language = Language(project=vuid.project, name=unicode(w[language_i].value).strip().lower())
            language.save()
        except Language.MultipleObjectsReturned:
            return {"valid": False, "message": "Parser error, multiple languages returned"}

        name = unicode(w[prompt_name_i].value).strip()
        verbiage = unicode(w[prompt_text_i].value).strip()
        vuid_time = w[date_changed_i].value.date() if w[date_changed_i].value is datetime else None

    return {"valid": True, "message": "Parsed file successfully"}


def upload_vuid(uploaded_file, user, project_id):
    # check if project root path is set
    # if not project_id.root_path:
    #     return {"valid": False, "message": "Please set root path, unable to upload"}

    vuid = VUID(filename=uploaded_file.name, file=uploaded_file, project_id=project_id, upload_by=user)
    vuid.save()

    # # check if any cell of 'vuid file header' is empty
    # if not verify_vuid_headers_empty(vuid):
    #     vuid.delete()
    #     return {"valid": False, "message": "Invalid file structure, unable to upload"}
    #
    # # check conflict between root path and vuid path
    # if not verify_root_path(vuid):
    #     vuid.delete()
    #     return {"valid": False, "message": "Invalid vuid path, unable to upload"}
    #
    # result = verify_vuid(vuid)
    # if not result['valid']:
    #     vuid.delete()
    #     return result
    # result = parse_vuid(vuid)
    # if not result['valid']:
    #     vuid.delete()
    #     return result
    #
    # if project.status == Project.TESTING:
    #     # set project status to "Initial"
    #     project.status = Project.INITIAL
    #     project.save()

    # status = UpdateStatus.objects.get_or_create(project=project)[0]
    # query_item = update_file_statuses.delay(project_id=project.pk, user_id=user.id)
    # status.query_id = query_item
    # status.running = True
    # status.save()
    return {"valid": True, "message": "File uploaded and parsed successfully"}


# def verify_vuid(vuid):
#     wb = load_workbook(vuid.file.path)
#     ws = wb.active
#     valid = False
#     message = "Invalid file structure, unable to upload"
#     if len(ws.rows) > 2:
#         if not verify_vuid_headers(vuid):
#             message = "Invalid file headers, unable to upload"
#         elif not verify_root_path(vuid):
#             message = "Invalid vuid path, unable to upload"
#         else:
#             valid = True
#             message = "Uploaded file successfully"
#     elif len(ws.rows) == 2:
#         if verify_vuid_headers(vuid):
#             message = "No records in file, unable to upload"
#     return {"valid": valid, "message": message}
#
#
# def verify_vuid_headers(vuid):
#     wb = load_workbook(vuid.file.path)
#     ws = wb.active
#     if len(ws.rows) >= 2:
#         try:
#             headers = set([str(i.value).lower() for i in ws.rows[0]])
#         except AttributeError:
#             return False
#         i = unicode(ws['A2'].value).strip().find('/')
#         if VUID_HEADER_NAME_SET.issubset(headers) and i != -1:
#             return True
#     return False


# def verify_vuid_headers_empty(vuid):
#     wb = load_workbook(vuid.file.path)
#     ws = wb.active
#     try:
#         headers = set([str(i.value).lower() for i in ws.rows[0]])
#     except AttributeError:
#         return False
#
#     try:
#         index = unicode(ws['A2'].value).strip().find('/')
#         vuid_path = ws['A2'].value.strip()[index:]
#     except AttributeError:
#         return False
#
#     return True
#
#
# def verify_root_path(vuid):
#     wb = load_workbook(vuid.file.path)
#     ws = wb.active
#     index = unicode(ws['A2'].value).strip().find('/')
#     vuid_path = ws['A2'].value.strip()[index:]
#     #print vuid_path, '-', vuid.project.root_path
#     if vuid_path.startswith(vuid.project.root_path):
#         return True
#     else:
#         return False


# def verify_update_root_path(project, new_path):
#     # if no vuids allow update root path
#     if project.vuid_set.all().count() == 0:
#         return True
#
#     old_path = project.root_path
#     if old_path.startswith(new_path):  # go up level, allowed
#         try:
#             with pysftp.Connection(project.bravo_server.address,
#                                    username=project.bravo_server.account,
#                                    private_key=settings.PRIVATE_KEY) as sftp:
#                 wc = sftp.execute('ls {0} -Rf | wc --l'.format(new_path))
#                 if int(wc[0]) > 15000:  # word count > 15k not allowed
#                     return False
#                 else:
#                     return True
#         except (pysftp.ConnectionException,
#                 pysftp.CredentialException,
#                 pysftp.AuthenticationException,
#                 pysftp.SSHException):
#             return False
#     else:  # go deep level, not allowed
#         return False
