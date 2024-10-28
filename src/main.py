from api.patent_api import fetch_patent_data
from api.utility_model_api import fetch_utility_model_data
from api.design_api import fetch_design_data
from api.trademark_api import fetch_trademark_data

def main():
    service_key = 'your_service_key'  # 발급받은 API 인증키 입력
    rgstNo = '1016699340000'  # 예시 등록번호

    # 특허 등록원부 API 호출
    patent_data = fetch_patent_data(rgstNo, service_key)
    if patent_data:
        print("특허 등록원부 데이터:", patent_data)
    
    # 실용신안 등록원부 API 호출
    utility_model_data = fetch_utility_model_data(rgstNo, service_key)
    if utility_model_data:
        print("실용신안 등록원부 데이터:", utility_model_data)

    # 디자인 등록원부 API 호출
    design_data = fetch_design_data(rgstNo, service_key)
    if design_data:
        print("디자인 등록원부 데이터:", design_data)

    # 상표 등록원부 API 호출
    trademark_data = fetch_trademark_data(rgstNo, service_key)
    if trademark_data:
        print("상표 등록원부 데이터:", trademark_data)

if __name__ == "__main__":
    main()
