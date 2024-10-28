# 네트워크 최적화를 위한 네트워크 점검 유틸 폴더
HTTP/3 (QUIC) 지원 여부, `Keep-Alive` 및 TLS 설정을 확인하는 코드를 모아두었습니다. 서버에서 사용하는 HTTP 버전, `Keep-Alive` 지원 여부, 그리고 TLS 프로토콜의 버전을 확인할 수 있습니다.

## 주요 기능
- **HTTP/3 (QUIC) 지원 확인**: 제공된 API 엔드포인트에서 QUIC (HTTP/3) 연결을 확인합니다.
- **Keep-Alive 및 TLS 확인**: 서버가 `Keep-Alive`를 지원하는지, 그리고 어떤 버전의 TLS를 사용하는지 확인합니다.

## QUIC (HTTP/3) 프로토콜 제한
### **미지원 프로토콜**
여기 해당 API 엔드포인트는 **HTTP/3 (QUIC)** 프로토콜을 지원하지 않고 있네요. HTTP/3는 최신 HTTP 프로토콜이지만, 많은 서버는 여전히 **HTTP/1.1** 또는 **HTTP/2**에 해당합니다.

이번 프로젝트에서 사용하는 API (`http://apis.data.go.kr/1430000/PttRgstRtInfoInqSvc`)도 **HTTP/3**를 지원하지 않는다는 것을 확인했습니다.


network_check.py를 통해서
HTTP/3로 API 연결을 시도하면 다음과 같은 오류가 확인할 수 있습니다:

```
[Error 8] nodename nor servname provided, or not known
```

이 오류는 서버가 QUIC 프로토콜을 인식하지 못하거나 지원하지 않는다는 것을 의미합니다. 따라서, 유틸리티는 서버가 지원하는 **HTTP/2** 또는 **HTTP/1.1**로 기본 설정됩니다.

### **Keep-Alive 및 TLS**
QUIC 프로토콜 외에도, 서버가 **Keep-Alive** 연결을 지원하는지와 사용하는 **TLS 버전**을 확인할 수 있습니다. 
**HTTP/1.1**은 보통 `Keep-Alive`를 지원하지만, 서버에서 명시적으로 비활성화할 수도 있으니, 네트워크 점검하는 겸 확인하는 것도 좋을 것 같습니다. 

서버에서 `Connection: close` 헤더를 명시적으로 설정하면, 매 요청마다 새로운 연결이 생성됩니다.

현재 API에서 확인된 결과는 다음과 같습니다:
- **Keep-Alive**: 해당 API는 `Keep-Alive` 연결을 지원하지 않으며, 응답 헤더에서 `Connection: close`가 설정되어 있네요.
- **TLS 버전**: 서버는 **HTTP/1.1**로 응답하고 있으며, TLS를 사용하고 있다는 것도 확인했습니다.

## 네트워크 최적화를 위한 네트워크 점검 유틸 사용 방법

네트워크 확인 유틸리티를 사용하려면 `network_check.py` 또는 관련 스크립트를 실행하세요:

```bash
python /path/to/your/utils/network_check.py
```

위 스크립트는 아래와 같은 내용을 파악할 수 있도록 도와줄겁니다... 아마도(?):
- 서버에서 사용하는 HTTP 버전 (예: HTTP/1.1, HTTP/2)
- Keep-Alive 상태 (활성화/비활성화)
- 서버에서 사용하는 TLS 버전
