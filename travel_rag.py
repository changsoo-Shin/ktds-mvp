import os
from typing import List, Dict, Any
from langchain_openai import AzureChatOpenAI
from config import Config

class TravelRAG:
    def __init__(self):
        try:
            print(f"Azure OpenAI 설정 확인:")
            print(f"- Endpoint: {Config.AZURE_ENDPOINT}")
            print(f"- API Key: {'설정됨' if Config.OPENAI_API_KEY else '설정되지 않음'}")
            print(f"- API Version: {Config.OPENAI_API_VERSION}")
            print(f"- Model: {Config.CHAT_MODEL}")
            
            self.llm = AzureChatOpenAI(
                azure_endpoint=Config.AZURE_ENDPOINT,
                api_key=Config.OPENAI_API_KEY,
                api_version=Config.OPENAI_API_VERSION,
                azure_deployment=Config.CHAT_MODEL,
                temperature=0.7
            )
            print("Azure OpenAI 초기화 성공!")
        except Exception as e:
            print(f"Azure OpenAI 초기화 오류: {e}")
            self.llm = None
    
    def get_destination_info(self, destination: str) -> Dict[str, Any]:
        """특정 여행지 정보 조회"""
        if not self.llm:
            return {"error": "Azure OpenAI가 초기화되지 않았습니다. API 설정을 확인해주세요."}
        
        prompt = f"""
        {destination}에 대한 여행 정보를 다음 형식으로 정리해주세요:
        
        ## 🏛️ 주요 관광지
        - [유명한 관광지 3-5개]
        
        ## 🎯 추천 활동
        - [할 수 있는 활동들]
        
        ## 📅 최적 방문 시기
        - [언제 가는 것이 좋은지]
        
        ## 🚌 교통 정보
        - [주요 교통수단과 방법]
        
        ## 💰 예상 비용
        - [대략적인 비용 정보]
        
        ## 💡 팁과 주의사항
        - [실용적인 팁들]
        """
        
        try:
            response = self.llm.invoke(prompt)
            return {
                "destination": destination,
                "info": response.content
            }
        except Exception as e:
            return {"error": f"API 호출 중 오류가 발생했습니다: {str(e)}"}
    
    def generate_itinerary(self, destination: str, days: int, interests: List[str], budget: str, start_date=None) -> Dict[str, Any]:
        """맞춤 여행일정 생성"""
        if not self.llm:
            return {"error": "Azure OpenAI가 초기화되지 않았습니다. API 설정을 확인해주세요."}
        
        # 시작일 처리
        from datetime import datetime, timedelta
        if start_date is None:
            # 시작일이 없으면 오늘부터 시작
            start_datetime = datetime.now()
        else:
            # 시작일이 있으면 해당 날짜부터 시작
            if hasattr(start_date, 'date'):
                start_datetime = datetime.combine(start_date, datetime.min.time())
            else:
                start_datetime = start_date
        
        start_date_str = start_datetime.strftime("%Y년 %m월 %d일 (%A)")
        
        # 각 날짜 계산
        date_list = []
        for i in range(days):
            current_date = start_datetime + timedelta(days=i)
            date_str = current_date.strftime("%Y년 %m월 %d일 (%A)")
            date_list.append(f"Day {i+1}: {date_str}")
        
        # 일정 생성 프롬프트
        prompt = f"""
        {destination}에서 {days}일간의 여행일정을 만들어주세요.
        
        여행자 정보:
        - 관심사: {', '.join(interests)}
        - 예산: {budget}
        - 여행 기간: {days}일
        - 시작 날짜: {start_date_str}
        
        다음 형식으로 일정을 만들어주세요:
        
        ## 📅 {days}일 여행일정 (시작: {start_date_str})
        
        """
        
        # 각 날짜별로 상세 일정 추가
        for i, date_info in enumerate(date_list):
            prompt += f"""
        ### {date_info}
        **오전 (9:00-12:00)**
        - 활동: [구체적인 활동]
        - 장소: [정확한 위치]
        - 예상 비용: [비용]
        - 소요시간: [시간]
        
        **오후 (13:00-18:00)**
        - 활동: [구체적인 활동]
        - 장소: [정확한 위치]
        - 예상 비용: [비용]
        - 소요시간: [시간]
        
        **저녁 (19:00-22:00)**
        - 활동: [구체적인 활동]
        - 장소: [정확한 위치]
        - 예상 비용: [비용]
        - 소요시간: [시간]
        
        """
        
        prompt += f"""
        ## 💰 총 예상 비용
        - 숙박: [비용]
        - 식사: [비용]
        - 교통: [비용]
        - 관광: [비용]
        - 기타: [비용]
        - **총합: [총 비용]**
        
        ## 🎯 여행 팁
        - [실용적인 팁들]
        - [주의사항]
        - [추가 추천사항]
        """
        
        try:
            response = self.llm.invoke(prompt)
            return {
                "destination": destination,
                "days": days,
                "interests": interests,
                "budget": budget,
                "itinerary": response.content
            }
        except Exception as e:
            return {"error": f"API 호출 중 오류가 발생했습니다: {str(e)}"}
