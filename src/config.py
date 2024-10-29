# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_SERVICE_KEY: str = os.getenv("API_SERVICE_KEY", "Ut1Rh63x")  # 기본값으로 설정된 API 키
    BASE_URL: str = "https://apis.data.go.kr/1430000/PttRgstRtInfoInqSvc"
    
    # API Endpoints
    DESIGN_API_URL: str = f"{BASE_URL}/getDesignHistory"
    PATENT_API_URL: str = f"{BASE_URL}/getPatentRegisterHistory"
    UTILITY_MODEL_API_URL: str = f"{BASE_URL}/getUtilityModelHistory"
    TRADEMARK_API_URL: str = f"{BASE_URL}/getMarkHistory"

settings = Settings()