import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from google.cloud.firestore_v1 import FieldFilter
from rest_framework import status
from rest_framework.decorators import api_view

from favorite_list.blocks import favorite_list_block
from slack_music_bot import settings
from utils.youtube_music_api import YoutubeMusicAPI


@api_view(['POST'])
def favorite_list_command(request):
    data = request.POST

    user_id = data['user_id']

    firestore = getattr(settings, 'FIRESTORE')
    query = firestore.collection('favorite_musics').where(filter=FieldFilter('user_id', '==', user_id))
    docs = query.stream()

    ytmusic_api = YoutubeMusicAPI(api_key=getattr(settings, 'YOUTUBE_API_KEY', ''))

    response = {
        'blocks': favorite_list_block(docs)
    }

    print(json.dumps(response))
    return JsonResponse(response, status=status.HTTP_200_OK)