import json

from slack_music_bot import settings
from utils.youtube_music_api import YoutubeMusicAPI


def single_music_block(query, music):
    """
    單首歌曲

    :param query:
    :param music:
    :return:
    """
    ytmusic_api = YoutubeMusicAPI(api_key=getattr(settings, 'YOUTUBE_API_KEY', ''))

    return [{
               "type": "header",
               "text": {
                   "type": "plain_text",
                   "text": music['title'],
                   "emoji": True
               }
           }, {
               "type": "section",
               "text": {
                   "type": "mrkdwn",
                   "text": ytmusic_api.get_link(music['video_id'])
               },
               "accessory": {
                   "type": "image",
                   "image_url": music['thumbnails'],
                   "alt_text": music['title']
               }
           }, {
               "type": "actions",
               "elements": [
                   {
                       "type": "button",
                       "text": {
                           "type": "plain_text",
                           "text": "加入最愛"
                       },
                       "style": "primary",
                       "value": json.dumps(music),
                       "action_id": "add_favorite_list"
                   },
                   {
                       "type": "button",
                       "text": {
                           "type": "plain_text",
                           "text": "列出五首"
                       },
                       "value": json.dumps(
                           {'query': query, 'first_video_id': music['video_id']}),
                       "action_id": "get_five_music"
                   }
               ]
           }]


def multi_music_block(music_list):
    """
    多首歌曲

    :param music_list:
    """

    ytmusic_api = YoutubeMusicAPI(api_key=getattr(settings, 'YOUTUBE_API_KEY', ''))

    blocks = []
    for music in music_list:
        blocks.append({
               "type": "header",
               "text": {
                   "type": "plain_text",
                   "text": music['title'],
                   "emoji": True
               }
           })

        blocks.append({
               "type": "section",
               "text": {
                   "type": "mrkdwn",
                   "text":  ytmusic_api.get_link(music['video_id'])
               },
               "accessory": {
                   "type": "image",
                   "image_url": music['thumbnails'],
                   "alt_text": music['title']
               }
           })

        blocks.append({
               "type": "actions",
               "elements": [
                   {
                       "type": "button",
                       "text": {
                           "type": "plain_text",
                           "text": "加入最愛"
                       },
                       "style": "primary",
                       "value": json.dumps(music),
                       "action_id": "add_favorite_list"
                   }
               ]
           })

    return blocks
