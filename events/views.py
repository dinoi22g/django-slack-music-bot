from datetime import datetime
import json
import slack
from django.http import JsonResponse
from google.cloud.firestore_v1 import FieldFilter
from rest_framework import status
from rest_framework.decorators import api_view
import requests
from events.blocks import single_music_block, multi_music_block
from slack_music_bot import settings
from utils.youtube_music_api import YoutubeMusicAPI


@api_view(['POST'])
def slack_events(request):
    data = json.loads(request.body.decode('utf-8'))

    if data.get('type') is not None:
        data_type = data['type']

        # Slack verification web hook url
        if data_type == 'url_verification':
            return JsonResponse({'challenge': data['challenge']}, status=status.HTTP_200_OK)

        # Slack event callback
        elif data_type == 'event_callback':
            # Message type
            event = data['event']
            if event['type'] == 'message' and event.get('subtype') is None:
                if 'bot_id' not in event:
                    if (event.get('message') is not None and event['message'].get('subtype', '') != 'bot_message') or event.get('message') is None:
                        channel_id = event['channel']
                        text = event['text']
                        ytmusic_api = YoutubeMusicAPI(api_key=getattr(settings, 'YOUTUBE_API_KEY', ''))
                        search_list = ytmusic_api.search(text, 1)

                        if len(search_list):
                            search_result = search_list[0]

                            slack_client = slack.WebClient(token=getattr(settings, 'SLACK_BOT_TOKEN', ''))
                            blocks = single_music_block(text, search_result)
                            slack_client.chat_postMessage(channel=channel_id, blocks=blocks)

            return JsonResponse({}, status=status.HTTP_200_OK)

    return JsonResponse({}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def slack_interactions(request):
    if request.POST.get('payload') is not None:
        data = json.loads(request.POST['payload'])

        # response url
        response_url = data['response_url']

        # action
        action = data['actions'][0]
        action_id = action['action_id']

        # user
        user = data['user']
        user_id = user['id']

        # channel
        channel_id = data['container']['channel_id']

        try:
            value = json.loads(action['value'])
        except json.JSONDecodeError as e:
            value = action['value']

        if action_id == 'get_five_music':
            ytmusic_api = YoutubeMusicAPI(api_key=getattr(settings, 'YOUTUBE_API_KEY', ''))
            search_list = ytmusic_api.search(value['query'], 6)

            if len(search_list):
                blocks = multi_music_block(search_list)
                requests.post(response_url, json={"blocks": blocks})
        elif action_id == 'add_favorite_list':
            music_title = value['title']
            music_id = value['video_id']

            slack_client = slack.WebClient(token=getattr(settings, 'SLACK_BOT_TOKEN', ''))

            firestore = getattr(settings, 'FIRESTORE')
            query = firestore.collection('favorite_musics').where(filter=FieldFilter('user_id', '==', user_id)).where(filter=FieldFilter('video_id', '==', music_id))

            if not len(query.get()):
                doc = firestore.collection(u'favorite_musics').add({
                    'user_id': user_id,
                    'name': music_title,
                    'video_id': music_id,
                    'creation_date': datetime.now()
                })

                if doc:
                    slack_client.chat_postMessage(channel=channel_id, text=f'「{music_title}」已添加到最愛清單啦 :tada:')
                else:
                    slack_client.chat_postMessage(channel=channel_id, text=f'「{music_title}」添加失敗，請重新嘗試QQ')
            else:
                slack_client.chat_postMessage(channel=channel_id, text=f'「{music_title}」已經在最愛清單內。')

        return JsonResponse({}, status=status.HTTP_200_OK)

    return JsonResponse({}, status=status.HTTP_403_FORBIDDEN)
