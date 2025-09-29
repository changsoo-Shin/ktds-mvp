"""
검색 엔진 모듈
Azure AI Search를 활용한 벡터 검색 및 하이브리드 검색 기능 제공
"""

import os
import json
import re
import base64
from typing import List, Dict, Optional
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SemanticSearch,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField
)
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery
import tiktoken

class SearchEngine:
    """Azure AI Search 기반 검색 엔진"""
    
    def __init__(self):
        """검색 엔진 초기화"""
        self.endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.api_key = os.getenv("AZURE_SEARCH_API_KEY")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "smartdoc-index")
        
        # 환경변수 검증
        if not self.endpoint or not self.api_key:
            missing_vars = []
            if not self.endpoint:
                missing_vars.append("AZURE_SEARCH_ENDPOINT")
            if not self.api_key:
                missing_vars.append("AZURE_SEARCH_API_KEY")
            raise ValueError(f"Azure AI Search 설정이 필요합니다. 누락된 환경변수: {', '.join(missing_vars)}")
        
        # 엔드포인트 URL 정규화 (끝에 슬래시 없으면 추가)
        if not self.endpoint.endswith('/'):
            self.endpoint += '/'
        
        print(f"Azure AI Search 설정:")
        print(f"- 엔드포인트: {self.endpoint}")
        print(f"- 인덱스 이름: {self.index_name}")
        
        try:
            # 클라이언트 초기화
            self.credential = AzureKeyCredential(self.api_key)
            self.search_client = SearchClient(
                endpoint=self.endpoint,
                index_name=self.index_name,
                credential=self.credential
            )
            
            self.index_client = SearchIndexClient(
                endpoint=self.endpoint,
                credential=self.credential
            )
            
            # 토크나이저 초기화
            self.encoding = tiktoken.get_encoding("cl100k_base")
            
            # 인덱스 생성 확인
            self._ensure_index_exists()
            
        except Exception as e:
            raise Exception(f"Azure AI Search 클라이언트 초기화 실패: {str(e)}")
    
    def _sanitize_document_key(self, filename: str) -> str:
        """
        파일명을 Azure Search 문서 키 규칙에 맞게 변환
        
        Azure Search 문서 키 규칙:
        - 문자(letters), 숫자(digits), 언더스코어(_), 대시(-), 등호(=)만 허용
        - 최대 1024자
        
        Args:
            filename: 원본 파일명
            
        Returns:
            str: 변환된 문서 키
        """
        # 파일 확장자 분리
        name_without_ext = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1]
        
        # 비ASCII 문자(한글 등)가 포함된 경우 Base64 인코딩 사용
        if not name_without_ext.isascii():
            # UTF-8로 인코딩한 후 Base64로 변환 (URL-safe)
            encoded_bytes = name_without_ext.encode('utf-8')
            sanitized_name = base64.urlsafe_b64encode(encoded_bytes).decode('ascii')
            # Base64 패딩 문자 '='는 Azure Search에서 허용되므로 그대로 유지
        else:
            # ASCII 문자만 있는 경우 기존 방식 사용
            # 허용되지 않는 문자를 언더스코어로 대체
            # 허용 문자: 영문자, 숫자, 언더스코어, 대시, 등호
            sanitized_name = re.sub(r'[^a-zA-Z0-9_\-=]', '_', name_without_ext)
            
            # 연속된 언더스코어를 하나로 줄이기
            sanitized_name = re.sub(r'_{2,}', '_', sanitized_name)
            
            # 시작과 끝의 언더스코어 제거
            sanitized_name = sanitized_name.strip('_')
        
        # 확장자가 있으면 추가 (점도 언더스코어로 변환)
        if ext:
            sanitized_ext = re.sub(r'[^a-zA-Z0-9_\-=]', '_', ext)
            sanitized_name = f"{sanitized_name}{sanitized_ext}"
        
        # 빈 문자열이면 기본값 사용
        if not sanitized_name:
            sanitized_name = "document"
        
        # 길이 제한 (1024자)
        if len(sanitized_name) > 1000:  # 청크 인덱스를 위한 여유 공간
            sanitized_name = sanitized_name[:1000]
        
        return sanitized_name
    
    def _ensure_index_exists(self):
        """인덱스 존재 확인 및 생성"""
        try:
            # 인덱스 존재 확인
            self.index_client.get_index(self.index_name)
            print(f"기존 인덱스 '{self.index_name}' 확인됨")
        except Exception as e:
            print(f"인덱스 '{self.index_name}' 찾을 수 없음: {str(e)}")
            # 인덱스가 없으면 생성
            self._create_index()
    
    def _create_index(self):
        """검색 인덱스 생성"""
        try:
            index = SearchIndex(
                name=self.index_name,
                fields=[
                    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
                    SearchableField(name="title", type=SearchFieldDataType.String),
                    SearchableField(name="content", type=SearchFieldDataType.String),
                    SimpleField(name="source", type=SearchFieldDataType.String),
                    SimpleField(name="chunk_index", type=SearchFieldDataType.Int32),
                    SearchField(
                        name="content_vector",
                        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        vector_search_dimensions=1536,  # OpenAI embedding dimension
                        vector_search_profile_name="myHnswProfile"
                    )
                ],
                vector_search=VectorSearch(
                    algorithms=[HnswAlgorithmConfiguration(name="myHnsw")],
                    profiles=[VectorSearchProfile(
                        name="myHnswProfile", 
                        algorithm_configuration_name="myHnsw"
                    )]
                ),
                semantic_search=SemanticSearch(
                    configurations=[
                        SemanticConfiguration(
                            name="my-semantic-config",
                            prioritized_fields=SemanticPrioritizedFields(
                                title_field=SemanticField(field_name="title"),
                                content_fields=[SemanticField(field_name="content")]
                            )
                        )
                    ]
                )
            )
            
            self.index_client.create_index(index)
            print(f"인덱스 '{self.index_name}' 생성 완료")
            
        except Exception as e:
            print(f"인덱스 생성 실패: {str(e)}")
            # 실제 운영환경에서는 에러 처리 필요
    
    def add_documents(self, documents: List[Dict]):
        """
        문서를 검색 인덱스에 추가
        
        Args:
            documents: 문서 리스트 (content 필드 포함)
        """
        try:
            search_documents = []
            
            for doc_idx, document in enumerate(documents):
                # 문서를 청크로 분할
                chunks = self._chunk_document(document['content'])
                
                # 파일명을 Azure Search 키 규칙에 맞게 변환
                sanitized_name = self._sanitize_document_key(document['name'])
                
                for chunk_idx, chunk in enumerate(chunks):
                    # 문서 ID 생성 (변환된 파일명 사용)
                    doc_id = f"{sanitized_name}_{chunk_idx}"
                    
                    search_doc = {
                        "id": doc_id,
                        "title": document['name'],
                        "content": chunk,
                        "source": document['name'],
                        "chunk_index": chunk_idx,
                        "content_vector": []  # 실제로는 embedding 생성 필요
                    }
                    
                    search_documents.append(search_doc)
            
            # 배치로 문서 업로드
            if search_documents:
                result = self.search_client.upload_documents(search_documents)
                print(f"{len(search_documents)}개 문서 청크 업로드 완료")
                
        except Exception as e:
            print(f"문서 업로드 실패: {str(e)}")
            raise
    
    def _chunk_document(self, content: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        문서를 청크로 분할
        
        Args:
            content: 문서 내용
            chunk_size: 청크 크기 (토큰 수)
            overlap: 청크 간 겹치는 부분 (토큰 수)
            
        Returns:
            List[str]: 분할된 청크 리스트
        """
        if not content.strip():
            return []
        
        # 텍스트를 토큰으로 분할
        tokens = self.encoding.encode(content)
        
        if len(tokens) <= chunk_size:
            return [content]
        
        chunks = []
        start = 0
        
        while start < len(tokens):
            end = start + chunk_size
            
            # 토큰을 다시 텍스트로 변환
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)
            
            chunks.append(chunk_text.strip())
            
            start = end - overlap
            if start >= len(tokens):
                break
        
        return chunks
    
    def search(self, query: str, top_k: int = 5, include_vector: bool = False) -> List[Dict]:
        """
        검색 수행
        
        Args:
            query: 검색 쿼리
            top_k: 반환할 결과 수
            include_vector: 벡터 검색 포함 여부
            
        Returns:
            List[Dict]: 검색 결과 리스트
        """
        try:
            search_results = []
            
            # 하이브리드 검색 (텍스트 + 시맨틱)
            search_options = {
                "search_text": query,
                "top": top_k,
                "include_total_count": True,
                "query_type": "semantic",
                "semantic_configuration_name": "my-semantic-config"
            }
            
            # 벡터 검색 포함 (실제로는 embedding 생성 필요)
            if include_vector:
                # 여기서는 간단한 텍스트 검색만 수행
                pass
            
            results = self.search_client.search(**search_options)
            
            for result in results:
                search_results.append({
                    'title': result.get('title', ''),
                    'content': result.get('content', ''),
                    'source': result.get('source', ''),
                    'score': result.get('@search.score', 0),
                    'reranker_score': result.get('@search.reranker_score', 0)
                })
            
            return search_results
            
        except Exception as e:
            print(f"검색 실패: {str(e)}")
            return []
    
    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        시맨틱 검색 수행
        
        Args:
            query: 검색 쿼리
            top_k: 반환할 결과 수
            
        Returns:
            List[Dict]: 검색 결과 리스트
        """
        try:
            search_options = {
                "search_text": query,
                "top": top_k,
                "query_type": "semantic",
                "semantic_configuration_name": "my-semantic-config",
                "query_language": "ko-KR",
                "speller": "lexicon"
            }
            
            results = self.search_client.search(**search_options)
            search_results = []
            
            for result in results:
                search_results.append({
                    'title': result.get('title', ''),
                    'content': result.get('content', ''),
                    'source': result.get('source', ''),
                    'score': result.get('@search.score', 0),
                    'reranker_score': result.get('@search.reranker_score', 0),
                    'captions': result.get('@search.captions', [])
                })
            
            return search_results
            
        except Exception as e:
            print(f"시맨틱 검색 실패: {str(e)}")
            return []
    
    def hybrid_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        하이브리드 검색 (텍스트 + 벡터 + 시맨틱)
        
        Args:
            query: 검색 쿼리
            top_k: 반환할 결과 수
            
        Returns:
            List[Dict]: 검색 결과 리스트
        """
        try:
            # 텍스트 검색 결과
            text_results = self.search(query, top_k)
            
            # 시맨틱 검색 결과
            semantic_results = self.semantic_search(query, top_k)
            
            # 결과 통합 및 중복 제거
            all_results = {}
            
            for result in text_results + semantic_results:
                content = result['content']
                if content not in all_results:
                    all_results[content] = result
                else:
                    # 점수 높은 것을 선택
                    if result['score'] > all_results[content]['score']:
                        all_results[content] = result
            
            # 점수 기준으로 정렬
            final_results = list(all_results.values())
            final_results.sort(key=lambda x: x['score'], reverse=True)
            
            return final_results[:top_k]
            
        except Exception as e:
            print(f"하이브리드 검색 실패: {str(e)}")
            return []
    
    def get_index_stats(self) -> Dict:
        """
        인덱스 통계 정보 반환
        
        Returns:
            Dict: 인덱스 통계
        """
        try:
            index = self.index_client.get_index(self.index_name)
            
            # 문서 수 확인
            count_result = self.search_client.get_document_count()
            
            return {
                'index_name': self.index_name,
                'document_count': count_result,
                'fields': [field.name for field in index.fields],
                'vector_search_profiles': [profile.name for profile in index.vector_search.profiles] if index.vector_search else [],
                'semantic_configurations': [config.name for config in index.semantic_search.configurations] if index.semantic_search else []
            }
            
        except Exception as e:
            print(f"인덱스 통계 조회 실패: {str(e)}")
            return {}
    
    def clear_index(self):
        """인덱스의 모든 문서 삭제"""
        try:
            # 모든 문서 검색
            results = self.search_client.search(search_text="*", top=1000)
            document_ids = [result['id'] for result in results]
            
            if document_ids:
                # 문서 삭제
                self.search_client.delete_documents([{"id": doc_id} for doc_id in document_ids])
                print(f"{len(document_ids)}개 문서 삭제 완료")
            
        except Exception as e:
            print(f"인덱스 초기화 실패: {str(e)}")
