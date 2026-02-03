
"""
Audio transcription service using AssemblyAI API
"""
import time
import assemblyai as aai
from config import Config

aai.settings.api_key = Config.ASSEMBLYAI_API_KEY

# Longer timeout for upload + polling (SDK default 30s; large files need more)
aai.settings.http_timeout = 300.0  # 5 minutes


def format_transcription_error(error):
    """
    Format AssemblyAI API errors into user-friendly messages

    Args:
        error: Exception from API call

    Returns:
        str: User-friendly error message
    """
    error_str = str(error)

    # Check for rate limit error (429)
    if 'rate limit' in error_str.lower() or '429' in error_str:
        return "⏳ AssemblyAI rate limit reached. Please wait a few minutes and try again, or upgrade your plan at https://www.assemblyai.com/pricing for higher limits."

    # Check for quota/credit errors
    if 'quota' in error_str.lower() or 'insufficient' in error_str.lower() or 'credit' in error_str.lower():
        return "💳 AssemblyAI quota exceeded. Please check your account balance at https://www.assemblyai.com/app/account"

    # Check for authentication errors
    if 'auth' in error_str.lower() or '401' in error_str or '403' in error_str or 'api key' in error_str.lower():
        return "🔑 Authentication error. Please check your AssemblyAI API key configuration."

    # Check for timeout / write operation timed out (upload or polling)
    if 'timeout' in error_str.lower() or 'write operation' in error_str.lower():
        return "⏱️ Transcription request timed out. Please try again with a shorter audio file."

    # Check for file errors
    if 'file' in error_str.lower() or 'upload' in error_str.lower():
        return "📁 Error uploading audio file. Please ensure the file is a valid audio format."

    # Generic error
    return f"❌ Transcription error: {error_str[:200]}"


def transcribe_audio(audio_file_path, max_retries=3):
    """
    Transcribe audio file using AssemblyAI API
    Supports automatic language detection for 100+ languages.
    Retries on timeout/upload errors (e.g. write operation timed out).

    Args:
        audio_file_path (str): Path to the audio file
        max_retries (int): Number of attempts on timeout/transient errors

    Returns:
        str: Transcribed text
    """
    config = aai.TranscriptionConfig(language_detection=True)
    last_error = None

    for attempt in range(max_retries):
        try:
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(audio_file_path, config=config)

            if transcript.status == aai.TranscriptStatus.error:
                friendly_error = format_transcription_error(Exception(transcript.error))
                raise Exception(friendly_error)

            return transcript.text
        except Exception as e:
            last_error = e
            err_str = str(e).lower()
            # Retry on timeout / write operation timed out (transient)
            is_timeout = 'timeout' in err_str or 'write operation' in err_str
            if is_timeout and attempt + 1 < max_retries:
                time.sleep(5 * (attempt + 1))  # 5s, 10s backoff
                continue
            # If it's already a formatted error, re-raise it
            if '⏳' in str(e) or '💳' in str(e) or '🔑' in str(e) or '⏱️' in str(e) or '📁' in str(e):
                raise
            friendly_error = format_transcription_error(e)
            raise Exception(friendly_error)

    if last_error is not None:
        friendly_error = format_transcription_error(last_error)
        raise Exception(friendly_error)


def transcribe_audio_with_timestamps(audio_file_path):
    """
    Transcribe audio file with timestamps and speaker detection

    Args:
        audio_file_path (str): Path to the audio file

    Returns:
        dict: Transcribed text with timestamps and speaker labels
    """
    try:
        config = aai.TranscriptionConfig(speaker_labels=True)
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file_path, config=config)

        if transcript.status == aai.TranscriptStatus.error:
            # Format the error message
            friendly_error = format_transcription_error(Exception(transcript.error))
            raise Exception(friendly_error)

        # Return structured data with timestamps and speakers
        return {
            'text': transcript.text,
            'utterances': [
                {
                    'text': utterance.text,
                    'start': utterance.start,
                    'end': utterance.end,
                    'speaker': utterance.speaker
                }
                for utterance in transcript.utterances
            ] if transcript.utterances else []
        }
    except Exception as e:
        # If it's already a formatted error, re-raise it
        if '⏳' in str(e) or '💳' in str(e) or '🔑' in str(e) or '⏱️' in str(e) or '📁' in str(e):
            raise
        # Otherwise, format the error
        friendly_error = format_transcription_error(e)
        raise Exception(friendly_error)
