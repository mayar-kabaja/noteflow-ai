from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url):
    """Extract YouTube video ID from various URL formats"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]*)',
        r'youtube\.com\/embed\/([^&\n?]*)',
        r'youtube\.com\/v\/([^&\n?]*)'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    # If it's just the video ID
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url

    return None

def get_youtube_transcript(video_url):
    """
    Get transcript from YouTube video URL
    Returns the transcript text and video title
    """
    try:
        video_id = extract_video_id(video_url)

        if not video_id:
            raise ValueError("Invalid YouTube URL")

        # Get transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine all text
        transcript_text = " ".join([item['text'] for item in transcript_list])

        return {
            'video_id': video_id,
            'transcript': transcript_text,
            'success': True
        }

    except Exception as e:
        print(f"Error getting YouTube transcript: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def get_video_title_from_url(video_url):
    """Extract video title from URL (simplified version)"""
    video_id = extract_video_id(video_url)
    if video_id:
        return f"YouTube Video ({video_id})"
    return "YouTube Video"
