import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Azure OpenAI 설정
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "2024-02-15-preview")
    
    # Azure AI Search 설정
    AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
    AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
    AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "travel_destinations")
    
    # Azure Computer Vision 설정
    COMPUTER_VISION_KEY = os.getenv("COMPUTER_VISION_KEY")
    COMPUTER_VISION_ENDPOINT = os.getenv("COMPUTER_VISION_ENDPOINT")
    
    # 기타 API
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    
    # 모델 설정
    CHAT_MODEL = "gpt-4.1-mini"  # 실제 배포된 모델명으로 변경 필요
    EMBEDDING_MODEL = "text-embedding-3-small"
