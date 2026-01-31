"""
Configuration file for NoteFlow AI application
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # File upload settings
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB max file size (for video files)
    ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg', 'flac', 'webm', 'opus'}
    ALLOWED_BOOK_EXTENSIONS = {'pdf', 'epub', 'txt', 'docx', 'doc'}
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'webm', 'flv', 'm4v'}

    # API Keys
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    ASSEMBLYAI_API_KEY = os.environ.get('ASSEMBLYAI_API_KEY')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///noteflow.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
