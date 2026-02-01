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

        print(f"=== YOUTUBE TRANSCRIPT REQUEST ===", flush=True)
        print(f"Video ID: {video_id}", flush=True)
        print(f"Full URL: {video_url}", flush=True)

        # Try to list available transcripts first
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            print(f"Available transcripts found!", flush=True)

            # Try to get any available transcript
            try:
                # Try manually created transcripts first
                transcript = transcript_list.find_manually_created_transcript(['en', 'en-US', 'en-GB'])
                print(f"Found manually created English transcript", flush=True)
            except:
                try:
                    # Try generated transcripts
                    transcript = transcript_list.find_generated_transcript(['en', 'en-US', 'en-GB'])
                    print(f"Found auto-generated English transcript", flush=True)
                except:
                    # Get any available transcript
                    transcript = next(iter(transcript_list))
                    print(f"Using available transcript: {transcript.language}", flush=True)

            # Fetch the transcript data
            transcript_data = transcript.fetch()
            print(f"Transcript fetched successfully: {len(transcript_data)} segments", flush=True)

        except TranscriptsDisabled:
            print(f"ERROR: Transcripts are disabled for video {video_id}", flush=True)
            return {
                'success': False,
                'error': "⚠️ This video has transcripts disabled. Please try:\n1. A different video with captions\n2. Uploading the video file directly\n3. A video with auto-generated captions enabled"
            }
        except NoTranscriptFound:
            print(f"ERROR: No transcripts found for video {video_id}", flush=True)
            return {
                'success': False,
                'error': "⚠️ No captions/transcripts available for this video. Please try:\n1. A video with captions enabled\n2. Uploading the video file directly"
            }
        except VideoUnavailable:
            print(f"ERROR: Video {video_id} is unavailable", flush=True)
            return {
                'success': False,
                'error': "⚠️ This video is unavailable. It might be:\n1. Private or deleted\n2. Region-restricted\n3. Age-restricted\nTry a different public video."
            }
        except Exception as e:
            print(f"ERROR listing transcripts: {type(e).__name__}: {str(e)}", flush=True)
            return {
                'success': False,
                'error': f"Failed to access YouTube video: {str(e)}"
            }

        # If we got here but no transcript_data, something went wrong
        if not transcript_data:
            return {
                'success': False,
                'error': "No transcript data retrieved. The video may not have captions enabled."
            }

        print(f"Transcript fetched successfully, {len(transcript_data)} segments", flush=True)

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
