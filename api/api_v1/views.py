from django.http import JsonResponse
import os
import requests


def ping_view(req, *args, **kwargs):
    return JsonResponse({'msg': 'pong'})


def search_view(req, *args, **kwargs):
    api_gateway = '{}://{}/'.format(os.environ.get('SCHEME'), os.environ.get('SERVICE_API'))
    q = req.GET.get('q', 'misc')
    page = req.GET.get('page', 1)
    res = requests.get(api_gateway + 'search', params={'q': q, 'page': page})
    if res.staus_code == 200:
        return JsonResponse(res.json())
    else:
        return JsonResponse({})
