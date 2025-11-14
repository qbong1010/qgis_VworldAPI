
# VWorld GetLegendGraphic API 활용 방안

## 1. API 개요

### 1.1 기본 정보
- **API URL**: https://api.vworld.kr/req/image
- **요청 타입**: GetLegendGraphic
- **응답 형식**: PNG 이미지

### 1.2 파라미터
- `service`: image (고정값)
- `request`: GetLegendGraphic (고정값)
- `format`: png (이미지 포맷)
- `layer`: 레이어 이름 (예: lt_c_uq111)
- `style`: 스타일 이름 (보통 레이어 이름과 동일)
- `type`: 범례 타입 (ALL, POINT, LINE, POLYGON)
- `key`: API 인증키

## 2. QGIS 플러그인 활용 방안

### 2.1 레이어 다운로드 시 범례 자동 표시
플러그인에서 VWorld 레이어를 다운로드할 때 해당 레이어의 범례 이미지를 함께 다운로드하여 
QGIS 레이어 스타일 패널에 표시할 수 있습니다.

**구현 방법:**
1. WFS로 레이어 데이터 다운로드
2. GetLegendGraphic으로 범례 이미지 다운로드
3. QgsMessageBar 또는 별도 다이얼로그에서 범례 표시
4. 레이어 메타데이터에 범례 이미지 경로 저장

### 2.2 범례 기반 심볼로지 적용
범례 이미지를 분석하여 QGIS 심볼로지를 자동으로 설정할 수 있습니다.

**구현 방법:**
1. 범례 이미지 다운로드
2. 이미지 OCR로 텍스트 추출 (선택사항)
3. 색상 팔레트 추출
4. QML 스타일 파일 생성 또는 직접 스타일 적용

### 2.3 사용자 레이어 선택 UI 개선
레이어 선택 다이얼로그에 각 레이어의 범례 미리보기를 표시하여 
사용자가 레이어 내용을 쉽게 파악할 수 있습니다.

**구현 방법:**
1. 레이어 목록 다이얼로그에 범례 섬네일 추가
2. 범례 이미지 캐싱으로 성능 최적화
3. 툴팁에 상세 범례 표시

### 2.4 오프라인 범례 데이터베이스
자주 사용되는 레이어의 범례를 미리 다운로드하여 로컬 데이터베이스에 저장,
오프라인 환경에서도 범례를 확인할 수 있습니다.

**구현 방법:**
1. 주요 레이어 범례 사전 다운로드
2. SQLite 또는 파일 시스템에 저장
3. 플러그인 배포 시 포함

## 3. 기술적 구현 사항

### 3.1 Python 코드 예제

```python
import requests
from qgis.PyQt.QtGui import QPixmap

def download_legend(layer, style, api_key):
    """VWorld 레전드 이미지 다운로드"""
    url = "https://api.vworld.kr/req/image"
    params = {
        'service': 'image',
        'request': 'GetLegendGraphic',
        'format': 'png',
        'layer': layer,
        'style': style,
        'type': 'ALL',
        'key': api_key
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.content
    return None

def display_legend_in_qgis(legend_data):
    """QGIS에서 레전드 표시"""
    pixmap = QPixmap()
    pixmap.loadFromData(legend_data)
    
    # QLabel 또는 QMessageBox에 표시
    # 또는 레이어 속성 다이얼로그에 추가
    return pixmap
```

### 3.2 QGIS 통합 포인트

1. **QgsMapLayer 메타데이터**
   - 레전드 URL을 레이어 메타데이터에 저장
   - `layer.setCustomProperty('vworld_legend_url', url)`

2. **레이어 트리 컨텍스트 메뉴**
   - "VWorld 범례 보기" 메뉴 항목 추가
   - 클릭 시 범례 이미지 표시

3. **다이얼로그 위젯**
   - QTextBrowser 또는 QLabel에 HTML로 임베딩
   - `<img src="data:image/png;base64,{base64_data}" />`

## 4. 제약사항 및 고려사항

### 4.1 제약사항
- API 호출 제한이 있을 수 있음 (API 키별)
- 일부 레이어는 범례를 제공하지 않을 수 있음
- 네트워크 연결 필요

### 4.2 고려사항
- 범례 이미지 캐싱으로 반복 다운로드 방지
- 에러 처리 (404, 타임아웃 등)
- 사용자에게 범례 표시 옵션 제공

## 5. 향후 확장 가능성

### 5.1 다중 언어 범례
- 한국어/영어 범례 지원
- 사용자 언어 설정에 따라 자동 선택

### 5.2 대화형 범례
- 범례 항목 클릭 시 해당 피처만 표시
- 범례 기반 필터링 기능

### 5.3 범례 편집 기능
- 다운로드한 범례를 기반으로 커스텀 범례 생성
- QML 스타일 파일로 저장

## 6. 참고 자료
- VWorld OpenAPI: https://www.vworld.kr/dev/v4dv_wmsguide2_s001.do
- QGIS Python API: https://qgis.org/pyqgis/
- WMS GetLegendGraphic 표준: https://www.ogc.org/standards/wms
