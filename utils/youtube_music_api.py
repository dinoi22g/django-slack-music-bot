from googleapiclient.discovery import build


class YoutubeMusicAPI:
    """
        Youtube Music API
    """

    def __init__(self, api_key):
        """
        初始化
        :param api_key:
        """
        self.api = build('youtube', 'v3', developerKey=api_key)

    def search(self, query, max_result=10):
        """
        搜尋音樂
        videoCategoryId  => 查詢類型

        :param query:
        :param max_result:
        :return:
        """
        search_response = self.api.search().list(
            q=query,
            type='video',
            part='id,snippet',
            videoCategoryId=10,  # 音樂為10
            maxResults=max_result
        ).execute()

        music_list = []
        for item in search_response['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            thumbnails = item['snippet']['thumbnails']['default']['url']
            music_list.append({'video_id': video_id, 'title': title, 'thumbnails': thumbnails})
        return music_list

    def get_link(self, video_id, music_link=True):
        """
        取得連結網址

        :param video_id:
        :param music_link:
        :return:
        """
        if music_link:
            return 'https://music.youtube.com/watch?v=' + video_id
        else:
            return 'https://youtube.com/watch?v=' + video_id


