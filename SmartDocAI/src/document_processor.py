"""
문서 처리 모듈
PDF, Word, 텍스트 파일에서 내용을 추출하는 기능 제공
"""

import io
import os
from typing import Union, List, Dict
import PyPDF2
import docx
from streamlit.runtime.uploaded_file_manager import UploadedFile

class DocumentProcessor:
    """문서 처리 클래스"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.doc', '.txt']
    
    def extract_content(self, file: UploadedFile) -> str:
        """
        업로드된 파일에서 텍스트 내용 추출
        
        Args:
            file: Streamlit UploadedFile 객체
            
        Returns:
            str: 추출된 텍스트 내용
        """
        file_extension = os.path.splitext(file.name)[1].lower()
        
        try:
            if file_extension == '.pdf':
                return self._extract_from_pdf(file)
            elif file_extension in ['.docx', '.doc']:
                return self._extract_from_word(file)
            elif file_extension == '.txt':
                return self._extract_from_text(file)
            else:
                raise ValueError(f"지원하지 않는 파일 형식: {file_extension}")
                
        except Exception as e:
            raise Exception(f"문서 처리 중 오류 발생: {str(e)}")
    
    def _extract_from_pdf(self, file: UploadedFile) -> str:
        """PDF 파일에서 텍스트 추출"""
        try:
            # 파일을 바이트로 읽기
            file_bytes = file.read()
            
            # PDF 리더 생성
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            
            text_content = ""
            
            # 모든 페이지에서 텍스트 추출
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text() + "\n"
            
            if not text_content.strip():
                raise Exception("PDF에서 텍스트를 추출할 수 없습니다.")
            
            return text_content.strip()
            
        except Exception as e:
            raise Exception(f"PDF 처리 실패: {str(e)}")
    
    def _extract_from_word(self, file: UploadedFile) -> str:
        """Word 파일에서 텍스트 추출"""
        try:
            # 파일을 바이트로 읽기
            file_bytes = file.read()
            
            # Word 문서 열기
            doc = docx.Document(io.BytesIO(file_bytes))
            
            text_content = ""
            
            # 모든 단락에서 텍스트 추출
            for paragraph in doc.paragraphs:
                text_content += paragraph.text + "\n"
            
            # 표에서 텍스트 추출
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text_content += cell.text + " "
                    text_content += "\n"
            
            if not text_content.strip():
                raise Exception("Word 문서에서 텍스트를 추출할 수 없습니다.")
            
            return text_content.strip()
            
        except Exception as e:
            raise Exception(f"Word 문서 처리 실패: {str(e)}")
    
    def _extract_from_text(self, file: UploadedFile) -> str:
        """텍스트 파일에서 내용 읽기"""
        try:
            # 파일을 문자열로 디코딩
            file_bytes = file.read()
            
            # 다양한 인코딩 시도
            encodings = ['utf-8', 'cp949', 'euc-kr', 'latin-1']
            
            for encoding in encodings:
                try:
                    text_content = file_bytes.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise Exception("파일 인코딩을 인식할 수 없습니다.")
            
            if not text_content.strip():
                raise Exception("텍스트 파일이 비어있습니다.")
            
            return text_content.strip()
            
        except Exception as e:
            raise Exception(f"텍스트 파일 처리 실패: {str(e)}")
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        텍스트를 청크로 분할
        
        Args:
            text: 분할할 텍스트
            chunk_size: 청크 크기 (문자 수)
            overlap: 청크 간 겹치는 부분 (문자 수)
            
        Returns:
            List[str]: 분할된 텍스트 청크 리스트
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # 문장 경계에서 분할 시도
            if end < len(text):
                # 마지막 문장 끝 찾기
                last_period = text.rfind('.', start, end)
                last_newline = text.rfind('\n', start, end)
                
                if last_period > start:
                    end = last_period + 1
                elif last_newline > start:
                    end = last_newline + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def extract_metadata(self, file: UploadedFile) -> Dict[str, str]:
        """
        파일 메타데이터 추출
        
        Args:
            file: Streamlit UploadedFile 객체
            
        Returns:
            Dict[str, str]: 메타데이터 딕셔너리
        """
        return {
            'name': file.name,
            'size': str(file.size),
            'type': file.type,
            'extension': os.path.splitext(file.name)[1].lower()
        }
    
    def is_supported_format(self, filename: str) -> bool:
        """
        파일 형식 지원 여부 확인
        
        Args:
            filename: 파일명
            
        Returns:
            bool: 지원 여부
        """
        extension = os.path.splitext(filename)[1].lower()
        return extension in self.supported_formats
    
    def get_file_info(self, file: UploadedFile) -> Dict[str, Union[str, int]]:
        """
        파일 정보 반환
        
        Args:
            file: Streamlit UploadedFile 객체
            
        Returns:
            Dict: 파일 정보
        """
        return {
            'name': file.name,
            'size_bytes': file.size,
            'size_kb': round(file.size / 1024, 2),
            'type': file.type,
            'extension': os.path.splitext(file.name)[1].lower(),
            'supported': self.is_supported_format(file.name)
        }
