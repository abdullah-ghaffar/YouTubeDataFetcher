from googleapiclient.discovery import build
import pandas as pd

# Replace with your own API key
API_KEY = ''
youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_videos_to_excel(query, max_results=300):
    all_videos = []  # List to store all retrieved videos
    next_page_token = None

    while len(all_videos) < max_results:
        # Search for videos related to the query
        request = youtube.search().list(
            part='snippet',
            q=query,
            type='video',
            maxResults=50,  # Maximum per request is 50
            pageToken=next_page_token
        )
        response = request.execute()

        # Collect video information
        for item in response['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            channel_title = item['snippet']['channelTitle']
            published_at = item['snippet']['publishedAt']

            # Construct the thumbnail URL in the desired format
            thumbnail_url = f'https://i.ytimg.com/vi/{video_id}/hq720.jpg'

            # Append video details to the list
            all_videos.append({
                'Title': title,
                'Channel': channel_title,
                'Published At': published_at,
                'Video URL': f'https://www.youtube.com/watch?v={video_id}',
                'Thumbnail URL': thumbnail_url  # Add constructed thumbnail URL
            })

        # Get the next page token to continue fetching
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break  # Exit loop if there are no more pages

    # Limit the results to the maximum specified
    filtered_videos = all_videos[:max_results]

    # Create a DataFrame from the video data
    df = pd.DataFrame(filtered_videos)

    # Save the DataFrame to an Excel file
    output_file = 'youtube_videos_hq720_only_converted.xlsx'
    df.to_excel(output_file, index=False)

    print(f'Saved {len(filtered_videos)} videos to {output_file}.')

# Example usage
search_videos_to_excel("viral")

