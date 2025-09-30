"""
AI 어시스턴트 모듈
Azure OpenAI를 활용한 질문-답변 및 문서 분석 기능 제공
"""

import os
from typing import List, Dict, Optional
from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

class AIAssistant:
    """Azure OpenAI 기반 AI 어시스턴트"""
    
    def __init__(self):
        """AI 어시스턴트 초기화"""
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4.1-mini")
        
        if not all([self.api_key, self.endpoint]):
            raise ValueError("Azure OpenAI 설정이 필요합니다.")
        
        # OpenAI 클라이언트 초기화
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.endpoint
        )
        
        # LangChain 모델 초기화
        self.llm = AzureChatOpenAI(
            azure_deployment=self.deployment_name,
            openai_api_version=self.api_version,
            azure_endpoint=self.endpoint,
            openai_api_key=self.api_key,
            temperature=0.7,
            max_tokens=2000
        )
        
        # 시스템 프롬프트 설정
        self.system_prompt = """당신은 SmartDoc AI의 지능형 문서 분석 어시스턴트입니다.

주요 역할:
1. 업로드된 문서의 내용을 바탕으로 정확하고 유용한 답변을 제공합니다.
2. 문서에서 찾을 수 없는 정보는 명확히 말하고, 추측은 피합니다.
3. 답변은 한국어로 제공하며, 친근하고 전문적인 톤을 유지합니다.
4. 필요시 관련 문서의 출처나 페이지를 명시합니다.

답변 형식:
- 질문에 대한 직접적인 답변
- 관련된 추가 정보나 맥락 설명
- 필요시 문서의 해당 부분 인용

항상 정확하고 도움이 되는 정보를 제공하도록 노력하세요."""
    
    def ask_question(self, question: str, documents: List[Dict], search_engine=None) -> str:
        """
        문서 기반 질문-답변
        
        Args:
            question: 사용자 질문
            documents: 문서 리스트
            search_engine: 검색 엔진 (선택사항)
            
        Returns:
            str: AI 응답
        """
        try:
            # 관련 문서 검색
            relevant_docs = self._find_relevant_documents(question, documents, search_engine)
            
            # 컨텍스트 구성
            context = self._build_context(relevant_docs)
            
            # 프롬프트 생성
            prompt = self._create_prompt(question, context)
            
            # AI 응답 생성
            response = self._generate_response(prompt)
            
            return response
            
        except Exception as e:
            return f"죄송합니다. 답변 생성 중 오류가 발생했습니다: {str(e)}"
    
    def _find_relevant_documents(self, question: str, documents: List[Dict], search_engine=None) -> List[Dict]:
        """
        질문과 관련된 문서 찾기
        
        Args:
            question: 사용자 질문
            documents: 전체 문서 리스트
            search_engine: 검색 엔진
            
        Returns:
            List[Dict]: 관련 문서 리스트
        """
        relevant_docs = []
        
        # 검색 엔진이 있으면 활용
        if search_engine:
            try:
                search_results = search_engine.hybrid_search(question, top_k=3)
                for result in search_results:
                    relevant_docs.append({
                        'name': result.get('source', ''),
                        'content': result.get('content', ''),
                        'score': result.get('score', 0)
                    })
            except Exception as e:
                print(f"검색 엔진 오류: {str(e)}")
        
        # 검색 결과가 부족하면 전체 문서에서 키워드 매칭
        if not relevant_docs:
            question_keywords = question.lower().split()
            for doc in documents:
                content_lower = doc['content'].lower()
                matches = sum(1 for keyword in question_keywords if keyword in content_lower)
                if matches > 0:
                    relevant_docs.append({
                        'name': doc['name'],
                        'content': doc['content'][:2000],  # 처음 2000자만
                        'score': matches / len(question_keywords)
                    })
        
        # 점수 기준으로 정렬
        relevant_docs.sort(key=lambda x: x['score'], reverse=True)
        return relevant_docs[:3]  # 상위 3개만 반환
    
    def _build_context(self, documents: List[Dict]) -> str:
        """
        문서 컨텍스트 구성
        
        Args:
            documents: 관련 문서 리스트
            
        Returns:
            str: 구성된 컨텍스트
        """
        if not documents:
            return "관련 문서를 찾을 수 없습니다."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"""
문서 {i}: {doc['name']}
내용: {doc['content']}
---
""")
        
        return "\n".join(context_parts)
    
    def _create_prompt(self, question: str, context: str) -> List[Dict]:
        """
        AI 프롬프트 생성
        
        Args:
            question: 사용자 질문
            context: 문서 컨텍스트
            
        Returns:
            List[Dict]: 프롬프트 메시지 리스트
        """
        user_prompt = f"""
사용자 질문: {question}

관련 문서 내용:
{context}

위 문서 내용을 바탕으로 사용자의 질문에 정확하고 유용한 답변을 제공해주세요.
문서에서 찾을 수 없는 정보는 명확히 말하고, 추측은 피해주세요.
답변은 한국어로 제공해주세요.
"""
        
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    
    def _generate_response(self, messages: List[Dict]) -> str:
        """
        AI 응답 생성
        
        Args:
            messages: 프롬프트 메시지 리스트
            
        Returns:
            str: AI 응답
        """
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                top_p=0.9
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"AI 응답 생성 실패: {str(e)}")
    
    def summarize_document(self, document: Dict) -> str:
        """
        문서 요약 생성
        
        Args:
            document: 문서 딕셔너리 (name, content 포함)
            
        Returns:
            str: 문서 요약
        """
        try:
            summary_prompt = f"""
다음 문서의 내용을 요약해주세요:

문서명: {document['name']}
내용: {document['content'][:4000]}  # 처음 4000자만

요약 요구사항:
1. 주요 내용을 3-5개 포인트로 정리
2. 핵심 키워드와 개념 포함
3. 문서의 목적이나 결론 요약
4. 한국어로 작성

요약:
"""
            
            messages = [
                {"role": "system", "content": "당신은 문서 요약 전문가입니다. 주어진 문서의 핵심 내용을 명확하고 간결하게 요약해주세요."},
                {"role": "user", "content": summary_prompt}
            ]
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=0.3,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"문서 요약 생성 실패: {str(e)}"
    
    def classify_document(self, document: Dict) -> str:
        """
        문서 분류
        
        Args:
            document: 문서 딕셔너리
            
        Returns:
            str: 문서 카테고리
        """
        try:
            classification_prompt = f"""
다음 문서를 적절한 카테고리로 분류해주세요:

문서명: {document['name']}
내용: {document['content'][:2000]}  # 처음 2000자만

분류 카테고리:
- 학술/연구: 논문, 연구보고서, 학술 자료
- 비즈니스: 사업계획서, 보고서, 제안서
- 기술: 기술문서, 매뉴얼, 가이드
- 법률/정책: 법률문서, 정책자료, 규정
- 교육: 교재, 교육자료, 강의노트
- 일반: 기타 문서

분류 결과만 간단히 답변해주세요.
"""
            
            messages = [
                {"role": "system", "content": "당신은 문서 분류 전문가입니다. 주어진 문서를 적절한 카테고리로 분류해주세요."},
                {"role": "user", "content": classification_prompt}
            ]
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=0.1,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return "분류 실패"
    
    def extract_keywords(self, document: Dict, num_keywords: int = 10) -> List[str]:
        """
        문서에서 키워드 추출
        
        Args:
            document: 문서 딕셔너리
            num_keywords: 추출할 키워드 수
            
        Returns:
            List[str]: 키워드 리스트
        """
        try:
            keyword_prompt = f"""
다음 문서에서 가장 중요한 키워드 {num_keywords}개를 추출해주세요:

문서명: {document['name']}
내용: {document['content'][:3000]}  # 처음 3000자만

요구사항:
1. 문서의 핵심 개념과 주제를 나타내는 키워드
2. 중요한 고유명사, 전문용어 포함
3. 키워드는 쉼표로 구분하여 나열
4. 한국어 키워드 우선, 필요시 영어 포함

키워드:
"""
            
            messages = [
                {"role": "system", "content": "당신은 키워드 추출 전문가입니다. 문서의 핵심을 나타내는 중요한 키워드들을 추출해주세요."},
                {"role": "user", "content": keyword_prompt}
            ]
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=0.2,
                max_tokens=200
            )
            
            keywords_text = response.choices[0].message.content.strip()
            keywords = [kw.strip() for kw in keywords_text.split(',')]
            
            return keywords[:num_keywords]
            
        except Exception as e:
            return []
    
    def get_document_insights(self, document: Dict) -> Dict[str, str]:
        """
        문서 인사이트 생성
        
        Args:
            document: 문서 딕셔너리
            
        Returns:
            Dict[str, str]: 인사이트 딕셔너리
        """
        try:
            # 요약, 분류, 키워드 추출을 병렬로 수행
            summary = self.summarize_document(document)
            category = self.classify_document(document)
            keywords = self.extract_keywords(document)
            
            return {
                'summary': summary,
                'category': category,
                'keywords': ', '.join(keywords),
                'word_count': len(document['content'].split()),
                'char_count': len(document['content'])
            }
            
        except Exception as e:
            return {
                'summary': f"인사이트 생성 실패: {str(e)}",
                'category': "알 수 없음",
                'keywords': "",
                'word_count': 0,
                'char_count': 0
            }
