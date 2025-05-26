from googleapiclient.discovery import build

def get_youtube_trending_videos(api_key, max_results=10):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode="TH",
        maxResults=max_results
    )
    response = request.execute()
    videos = []
    for item in response['items']:
        video_data = {
            'title': item['snippet']['title'],
            'channel': item['snippet']['channelTitle'],
            'views': int(item['statistics'].get('viewCount', 0)),
            'likes': int(item['statistics'].get('likeCount', 0)),
            'comments': int(item['statistics'].get('commentCount', 0))
        }
        videos.append(video_data)
    return videos

if __name__ == "__main__":
    API_KEY = 'YOUR_API_KEY'  # ใส่ API key ของคุณตรงนี้
    trending_videos = get_youtube_trending_videos(API_KEY, max_results=10)
    for idx, video in enumerate(trending_videos, start=1):
        print(f"{idx}. {video['title']} - ช่อง: {video['channel']} - ยอดวิว: {video['views']}")
