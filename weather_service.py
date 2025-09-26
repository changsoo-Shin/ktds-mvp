import requests
import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from config import Config

class WeatherService:
    def __init__(self):
        self.api_key = Config.WEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, city: str) -> Dict[str, Any]:
        """현재 날씨 정보 조회"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "kr"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
                "wind_speed": data["wind"]["speed"],
                "visibility": data.get("visibility", 0) / 1000  # km로 변환
            }
            
        except Exception as e:
            return {"error": f"날씨 정보를 가져올 수 없습니다: {str(e)}"}
    
    def get_forecast(self, city: str, days: int = 5) -> Dict[str, Any]:
        """5일간 날씨 예보 조회"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "kr"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # 날짜별로 그룹화
            forecast_by_date = {}
            for item in data["list"]:
                date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
                if date not in forecast_by_date:
                    forecast_by_date[date] = []
                
                forecast_by_date[date].append({
                    "time": datetime.fromtimestamp(item["dt"]).strftime("%H:%M"),
                    "temperature": item["main"]["temp"],
                    "description": item["weather"][0]["description"],
                    "icon": item["weather"][0]["icon"],
                    "humidity": item["main"]["humidity"],
                    "wind_speed": item["wind"]["speed"]
                })
            
            # 요약 정보 생성
            summary = []
            for date, forecasts in list(forecast_by_date.items())[:days]:
                temps = [f["temperature"] for f in forecasts]
                descriptions = [f["description"] for f in forecasts]
                
                summary.append({
                    "date": date,
                    "min_temp": min(temps),
                    "max_temp": max(temps),
                    "avg_temp": sum(temps) / len(temps),
                    "description": max(set(descriptions), key=descriptions.count),  # 가장 빈번한 설명
                    "icon": forecasts[0]["icon"]
                })
            
            return {
                "city": data["city"]["name"],
                "country": data["city"]["country"],
                "forecast": summary
            }
            
        except Exception as e:
            return {"error": f"날씨 예보를 가져올 수 없습니다: {str(e)}"}
    
    def get_weather_advice(self, weather_data: Dict[str, Any]) -> str:
        """날씨에 따른 여행 조언 생성"""
        if "error" in weather_data:
            return "날씨 정보를 확인할 수 없어 여행 조언을 제공할 수 없습니다."
        
        temp = weather_data.get("temperature", 0)
        description = weather_data.get("description", "")
        humidity = weather_data.get("humidity", 0)
        wind_speed = weather_data.get("wind_speed", 0)
        
        advice = []
        
        # 온도 기반 조언
        if temp < 0:
            advice.append("❄️ 매우 추운 날씨입니다. 따뜻한 옷을 준비하세요.")
        elif temp < 10:
            advice.append("🧥 쌀쌀한 날씨입니다. 겉옷을 챙기세요.")
        elif temp < 25:
            advice.append("🌤️ 쾌적한 날씨입니다. 야외 활동에 좋습니다.")
        elif temp < 35:
            advice.append("☀️ 더운 날씨입니다. 자외선 차단제와 충분한 수분을 준비하세요.")
        else:
            advice.append("🔥 매우 더운 날씨입니다. 실내 활동을 권장합니다.")
        
        # 날씨 설명 기반 조언
        if "rain" in description.lower():
            advice.append("☔ 비가 올 예정입니다. 우산을 준비하세요.")
        elif "snow" in description.lower():
            advice.append("❄️ 눈이 올 예정입니다. 미끄러운 길에 주의하세요.")
        elif "cloud" in description.lower():
            advice.append("☁️ 흐린 날씨입니다. 사진 촬영 시 조명을 고려하세요.")
        
        # 습도 기반 조언
        if humidity > 80:
            advice.append("💧 습도가 높습니다. 통풍이 잘 되는 옷을 입으세요.")
        
        # 바람 기반 조언
        if wind_speed > 10:
            advice.append("💨 바람이 강합니다. 모자나 스카프를 고정하세요.")
        
        return "\n".join(advice) if advice else "일반적인 여행 준비를 하시면 됩니다."
