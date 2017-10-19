from django.shortcuts import render
from django.http.response import JsonResponse


def ping_view(req, *args, **kwargs):
    return JsonResponse({'msg': 'pong'})
