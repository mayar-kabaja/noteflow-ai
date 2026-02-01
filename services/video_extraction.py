try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
except ImportError:
    # Fallback for older versions
    from youtube_transcript_api import YouTubeTranscriptApi
    TranscriptsDisabled = Exception
    NoTranscriptFound = Exception
    VideoUnavailable = Exception
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
            print(f"ERROR: Invalid YouTube URL: {video_url}", flush=True)
            raise ValueError("Invalid YouTube URL format")

        print("=== YOUTUBE TRANSCRIPT REQUEST ===", flush=True)
        print(f"Video ID: {video_id}", flush=True)
        print(f"Full URL: {video_url}", flush=True)

        # Try multiple language options (including auto-generated)
        languages_to_try = [
            ['en'],       # English
            ['a.en'],     # Auto-generated English
            ['ar'],       # Arabic
            ['a.ar'],     # Auto-generated Arabic
            ['es'],       # Spanish
            ['fr'],       # French
            ['de'],       # German
            ['pt'],       # Portuguese
            ['ru'],       # Russian
            ['hi'],       # Hindi
            ['ja'],       # Japanese
            ['ko'],       # Korean
        ]

        transcript_data = None
        last_error = None

        for languages in languages_to_try:
            try:
                print(f"Trying languages: {languages}", flush=True)
                # Use the correct API method
                api_result = YouTubeTranscriptApi().fetch(video_id, languages=languages)
                # Extract segments from the result
                transcript_data = api_result.segments if hasattr(api_result, 'segments') else api_result
                print(f"Successfully got transcript with {len(transcript_data)} segments", flush=True)
                break
            except TranscriptsDisabled as e:
                print(f"ERROR: Transcripts disabled for video {video_id}", flush=True)
                return {
                    'success': False,
                    'error': "⚠️ This video has transcripts disabled.\n\n"
                             "Please try:\n"
                             "1. A different video with captions enabled\n"
                             "2. Uploading the video file directly"
                }
            except NoTranscriptFound as e:
                last_error = e
                print(f"No transcript found for {languages}", flush=True)
                continue
            except VideoUnavailable as e:
                print(f"ERROR: Video {video_id} is unavailable", flush=True)
                return {
                    'success': False,
                    'error': "⚠️ This video is unavailable.\n\n"
                             "It might be:\n"
                             "• Private or deleted\n"
                             "• Region-restricted\n"
                             "• Age-restricted\n\n"
                             "Try a different public video."
                }
            except Exception as e:
                last_error = e
                print(f"Error with {languages}: {type(e).__name__}: {str(e)}", flush=True)
                continue

        # If no transcript found after all attempts
        if not transcript_data:
            error_msg = str(last_error) if last_error else "Unknown error"
            print(f"ERROR: No transcripts available. Last error: {error_msg}", flush=True)
            return {
                'success': False,
                'error': "⚠️ No captions/transcripts available for this video.\n\n"
                         "Please try:\n"
                         "1. A video with auto-generated captions\n"
                         "2. Uploading the video file directly\n\n"
                         "💡 Most YouTube videos have auto-captions!"
            }

        print(f"Processing {len(transcript_data)} transcript segments", flush=True)

        # Combine all text - handle both dict and object formats
        transcript_text = " ".join([
            item.text if hasattr(item, 'text') else item['text']
            for item in transcript_data
        ])

        return {
            'video_id': video_id,
            'transcript': transcript_text,
            'success': True
        }

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error getting YouTube transcript: {str(e)}\n{error_details}", flush=True)
        return {
            'success': False,
            'error': f"Could not retrieve transcript: {str(e)}"
        }

def get_video_title_from_url(video_url):
    """Extract video title from URL (simplified version)"""
    video_id = extract_video_id(video_url)
    if video_id:
        return f"YouTube Video ({video_id})"
    return "YouTube Video"
