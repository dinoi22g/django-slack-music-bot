import json

from slack_music_bot import settings
from utils.youtube_music_api import YoutubeMusicAPI


def favorite_list_block(docs):
    blocks = []

    ytmusic_api = YoutubeMusicAPI(api_key=getattr(settings, 'YOUTUBE_API_KEY', ''))

    for doc in docs:
        doc_dict = doc.to_dict()
        doc_dict['creation_date'] = str(doc_dict['creation_date'])

        blocks.append({
            "type": "header",
            "text": {
                "type": "plain_text",
                "text":  doc_dict['name'],
                "emoji": True
            }
        })

        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ytmusic_api.get_link(doc_dict['video_id'])
            },
            "accessory": {
                "type": "overflow",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "刪除",
                            "emoji": True
                        },
                        "value": doc_dict['video_id']
                    },
                ],
                "action_id": "delete_favorite_music"
            }
        })

        blocks.append({
            "type": "divider"
        })

    return blocks
