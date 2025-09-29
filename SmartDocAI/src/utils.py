"""
유틸리티 함수 모듈
공통적으로 사용되는 헬퍼 함수들 제공
"""

import os
import re
import hashlib
from typing import List, Dict, Any
from datetime import datetime
import streamlit as st

def validate_environment() -> Dict[str, bool]:
    """
    환경 변수 검증
    
    Returns:
        Dict[str, bool]: 환경 변수별 설정 여부
    """
    required_vars = {
        'AZURE_OPENAI_API_KEY': os.getenv('AZURE_OPENAI_API_KEY'),
        'AZURE_OPENAI_ENDPOINT': os.getenv('AZURE_OPENAI_ENDPOINT'),
        'AZURE_OPENAI_DEPLOYMENT_NAME': os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
        'AZURE_SEARCH_ENDPOINT': os.getenv('AZURE_SEARCH_ENDPOINT'),
        'AZURE_SEARCH_API_KEY': os.getenv('AZURE_SEARCH_API_KEY')
    }
    
    return {key: bool(value) for key, value in required_vars.items()}

def format_file_size(size_bytes: int) -> str:
    """
    파일 크기를 읽기 쉬운 형태로 포맷팅
    
    Args:
        size_bytes: 바이트 단위 파일 크기
        
    Returns:
        str: 포맷팅된 파일 크기
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

def sanitize_filename(filename: str) -> str:
    """
    파일명 정리 (특수문자 제거)
    
    Args:
        filename: 원본 파일명
        
    Returns:
        str: 정리된 파일명
    """
    # 특수문자 제거하고 공백을 언더스코어로 변경
    sanitized = re.sub(r'[^\w\s-]', '', filename)
    sanitized = re.sub(r'[-\s]+', '_', sanitized)
    return sanitized.strip('_')

def generate_document_id(filename: str, content: str) -> str:
    """
    문서 고유 ID 생성
    
    Args:
        filename: 파일명
        content: 문서 내용
        
    Returns:
        str: 문서 ID
    """
    # 파일명과 내용의 해시값을 조합하여 고유 ID 생성
    combined = f"{filename}_{content[:100]}"
    return hashlib.md5(combined.encode()).hexdigest()[:12]

def extract_text_preview(text: str, max_length: int = 200) -> str:
    """
    텍스트 미리보기 생성
    
    Args:
        text: 원본 텍스트
        max_length: 최대 길이
        
    Returns:
        str: 미리보기 텍스트
    """
    if len(text) <= max_length:
        return text
    
    # 문장 경계에서 자르기
    truncated = text[:max_length]
    last_period = truncated.rfind('.')
    last_newline = truncated.rfind('\n')
    
    if last_period > max_length * 0.7:
        return truncated[:last_period + 1]
    elif last_newline > max_length * 0.7:
        return truncated[:last_newline]
    else:
        return truncated + "..."

def validate_file_type(filename: str) -> bool:
    """
    지원되는 파일 형식인지 확인
    
    Args:
        filename: 파일명
        
    Returns:
        bool: 지원 여부
    """
    supported_extensions = ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.ppt', '.pptx', '.hwp']
    extension = os.path.splitext(filename)[1].lower()
    return extension in supported_extensions

def validate_file_size(file_size: int, max_size_mb: int = 10) -> bool:
    """
    파일 크기 검증
    
    Args:
        file_size: 파일 크기 (바이트)
        max_size_mb: 최대 크기 (MB)
        
    Returns:
        bool: 크기 유효 여부
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_size <= max_size_bytes

def format_timestamp(timestamp: datetime) -> str:
    """
    타임스탬프 포맷팅
    
    Args:
        timestamp: datetime 객체
        
    Returns:
        str: 포맷팅된 시간 문자열
    """
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def clean_text(text: str) -> str:
    """
    텍스트 정리 (불필요한 공백, 특수문자 정리)
    
    Args:
        text: 원본 텍스트
        
    Returns:
        str: 정리된 텍스트
    """
    if not text:
        return ""
    
    # 연속된 공백을 하나로 변경
    text = re.sub(r'\s+', ' ', text)
    
    # 앞뒤 공백 제거
    text = text.strip()
    
    # 특수 문자 정리
    text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
    
    return text

def split_text_by_sentences(text: str) -> List[str]:
    """
    텍스트를 문장 단위로 분할
    
    Args:
        text: 분할할 텍스트
        
    Returns:
        List[str]: 문장 리스트
    """
    if not text:
        return []
    
    # 문장 구분자로 분할
    sentences = re.split(r'[.!?]+', text)
    
    # 빈 문장 제거 및 정리
    sentences = [clean_text(sentence) for sentence in sentences if clean_text(sentence)]
    
    return sentences

def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    두 텍스트 간의 유사도 계산 (간단한 Jaccard 유사도)
    
    Args:
        text1: 첫 번째 텍스트
        text2: 두 번째 텍스트
        
    Returns:
        float: 유사도 (0.0 ~ 1.0)
    """
    if not text1 or not text2:
        return 0.0
    
    # 단어 단위로 분할
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 and not words2:
        return 1.0
    
    # Jaccard 유사도 계산
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return intersection / union if union > 0 else 0.0

def get_file_extension(filename: str) -> str:
    """
    파일 확장자 추출
    
    Args:
        filename: 파일명
        
    Returns:
        str: 확장자 (소문자)
    """
    return os.path.splitext(filename)[1].lower()

def is_valid_url(url: str) -> bool:
    """
    URL 유효성 검사
    
    Args:
        url: 검사할 URL
        
    Returns:
        bool: 유효성 여부
    """
    url_pattern = re.compile(
        r'^https?://'  # http:// 또는 https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # 도메인
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # 포트
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url))

def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    텍스트 자르기
    
    Args:
        text: 원본 텍스트
        max_length: 최대 길이
        suffix: 뒤에 붙일 문자열
        
    Returns:
        str: 자른 텍스트
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def display_error_message(error: Exception, context: str = ""):
    """
    에러 메시지 표시 (Streamlit용)
    
    Args:
        error: 발생한 예외
        context: 에러 발생 컨텍스트
    """
    error_msg = f"❌ {context}: {str(error)}" if context else f"❌ {str(error)}"
    st.error(error_msg)

def display_success_message(message: str):
    """
    성공 메시지 표시 (Streamlit용)
    
    Args:
        message: 성공 메시지
    """
    st.success(f"✅ {message}")

def display_info_message(message: str):
    """
    정보 메시지 표시 (Streamlit용)
    
    Args:
        message: 정보 메시지
    """
    st.info(f"ℹ️ {message}")

def display_warning_message(message: str):
    """
    경고 메시지 표시 (Streamlit용)
    
    Args:
        message: 경고 메시지
    """
    st.warning(f"⚠️ {message}")

def create_progress_bar(progress: float, label: str = ""):
    """
    진행률 바 생성 (Streamlit용)
    
    Args:
        progress: 진행률 (0.0 ~ 1.0)
        label: 라벨
    """
    if label:
        st.progress(progress, text=label)
    else:
        st.progress(progress)

def format_duration(seconds: float) -> str:
    """
    시간을 읽기 쉬운 형태로 포맷팅
    
    Args:
        seconds: 초 단위 시간
        
    Returns:
        str: 포맷팅된 시간
    """
    if seconds < 60:
        return f"{seconds:.1f}초"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}분"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}시간"

def get_current_timestamp() -> str:
    """
    현재 시간의 타임스탬프 문자열 반환
    
    Returns:
        str: 타임스탬프 문자열
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def create_unique_filename(original_filename: str) -> str:
    """
    고유한 파일명 생성 (타임스탬프 추가)
    
    Args:
        original_filename: 원본 파일명
        
    Returns:
        str: 고유 파일명
    """
    name, ext = os.path.splitext(original_filename)
    timestamp = get_current_timestamp()
    return f"{name}_{timestamp}{ext}"
