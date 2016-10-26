from django.shortcuts import render
from django.http import JsonResponse

from mdta.apps.runner.utils import emergency_test


def demo(request, project_id):
    c, f, result = emergency_test()
    return JsonResponse({'c': c, 'f': f, 'result': result})
