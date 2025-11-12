"""
VWorld GetLegendGraphic API 테스트 스크립트

이 스크립트는 VWorld Image API의 GetLegendGraphic 요청을 테스트하고
레전드 이미지를 다운로드합니다.
"""

import requests
import os
from datetime import datetime

# VWorld API 키
API_KEY = "82E0F346-3308-3E16-AD90-3E36EB0A6895"

# GetLegendGraphic API Base URL
LEGEND_API_URL = "https://api.vworld.kr/req/image"

# 테스트할 레이어 목록
TEST_LAYERS = [
    # 용도지역지구 관련
    {
        'layer': 'lt_c_uq111',  # 용도지구1종(개발진흥지구)
        'style': 'lt_c_uq111',
        'description': '용도지구1종(개발진흥지구)'
    },
    {
        'layer': 'lt_c_uq112',  # 용도지구2종(경관지구)
        'style': 'lt_c_uq112',
        'description': '용도지구2종(경관지구)'
    },
    {
        'layer': 'lt_c_uq113',  # 용도지구3종(고도지구)
        'style': 'lt_c_uq113',
        'description': '용도지구3종(고도지구)'
    },
    # 토지 관련
    {
        'layer': 'lp_pa_cbnd_bonbun',  # 연속지적도 본번
        'style': 'lp_pa_cbnd_bonbun',
        'description': '연속지적도(본번)'
    },
    {
        'layer': 'lp_pa_cbnd_bubun',  # 연속지적도 부번
        'style': 'lp_pa_cbnd_bubun',
        'description': '연속지적도(부번)'
    },
    # 도시계획
    {
        'layer': 'lt_c_upisuq153',  # 도시계획시설(공간시설)
        'style': 'lt_c_upisuq153',
        'description': '도시계획시설(공간시설)'
    },
    # 경계
    {
        'layer': 'lt_c_ademd',  # 읍면동
        'style': 'lt_c_ademd',
        'description': '행정구역(읍면동)'
    },
]


def download_legend(layer, style, output_dir='legends', type_param='ALL'):
    """
    레전드 이미지를 다운로드합니다.
    
    :param layer: 레이어 이름
    :param style: 스타일 이름
    :param output_dir: 저장 디렉토리
    :param type_param: TYPE 파라미터 (ALL, POINT, LINE, POLYGON 등)
    :return: (success, file_path, error_message)
    """
    # 파라미터 구성
    params = {
        'service': 'image',
        'request': 'GetLegendGraphic',
        'format': 'png',
        'layer': layer,
        'style': style,
        'type': type_param,
        'key': API_KEY
    }
    
    try:
        # API 요청
        print(f"\n{'='*60}")
        print(f"레이어: {layer}")
        print(f"스타일: {style}")
        print(f"타입: {type_param}")
        print(f"요청 URL: {LEGEND_API_URL}")
        print(f"파라미터: {params}")
        
        response = requests.get(LEGEND_API_URL, params=params, timeout=30)
        
        print(f"응답 상태 코드: {response.status_code}")
        print(f"응답 Content-Type: {response.headers.get('Content-Type')}")
        print(f"응답 크기: {len(response.content)} bytes")
        
        # 응답 확인
        if response.status_code != 200:
            error_msg = f"HTTP 오류: {response.status_code}"
            print(f"[ERROR] {error_msg}")
            
            # XML 오류 응답인 경우 내용 출력
            if 'xml' in response.headers.get('Content-Type', '').lower():
                print(f"오류 내용:\n{response.text[:500]}")
            
            return False, None, error_msg
        
        # Content-Type 확인
        content_type = response.headers.get('Content-Type', '')
        
        # 이미지가 아닌 경우 (오류 응답)
        if 'image' not in content_type.lower():
            print(f"[WARNING] 이미지가 아닌 응답 수신: {content_type}")
            print(f"응답 내용:\n{response.text[:500]}")
            return False, None, f"이미지가 아닌 응답: {content_type}"
        
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        # 파일 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{layer}_{style}_{type_param}_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"[SUCCESS] 파일 저장: {filepath}")
        return True, filepath, None
        
    except requests.exceptions.Timeout:
        error_msg = "요청 시간 초과"
        print(f"[ERROR] {error_msg}")
        return False, None, error_msg
        
    except requests.exceptions.RequestException as e:
        error_msg = f"요청 오류: {str(e)}"
        print(f"[ERROR] {error_msg}")
        return False, None, error_msg
        
    except Exception as e:
        error_msg = f"예상치 못한 오류: {str(e)}"
        print(f"[ERROR] {error_msg}")
        return False, None, error_msg


def test_all_layers():
    """모든 테스트 레이어에 대해 레전드를 다운로드합니다."""
    print("\n" + "="*60)
    print("VWorld GetLegendGraphic API 테스트")
    print("="*60)
    
    results = []
    
    for layer_info in TEST_LAYERS:
        layer = layer_info['layer']
        style = layer_info['style']
        description = layer_info['description']
        
        print(f"\n[{description}]")
        
        # ALL 타입으로 다운로드
        success, filepath, error = download_legend(layer, style, type_param='ALL')
        
        results.append({
            'layer': layer,
            'style': style,
            'description': description,
            'success': success,
            'filepath': filepath,
            'error': error
        })
    
    # 결과 요약
    print("\n" + "="*60)
    print("테스트 결과 요약")
    print("="*60)
    
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)
    
    print(f"\n성공: {success_count}/{total_count}")
    
    print("\n성공한 레이어:")
    for r in results:
        if r['success']:
            print(f"  [OK] {r['description']} ({r['layer']})")
            print(f"       파일: {r['filepath']}")
    
    print("\n실패한 레이어:")
    for r in results:
        if not r['success']:
            print(f"  [FAIL] {r['description']} ({r['layer']})")
            print(f"         오류: {r['error']}")
    
    return results


def test_type_parameters(layer='lt_c_uq111', style='lt_c_uq111'):
    """
    다양한 TYPE 파라미터를 테스트합니다.
    
    :param layer: 테스트할 레이어
    :param style: 테스트할 스타일
    """
    print("\n" + "="*60)
    print(f"TYPE 파라미터 테스트: {layer}")
    print("="*60)
    
    type_params = ['ALL', 'POINT', 'LINE', 'POLYGON']
    
    for type_param in type_params:
        download_legend(layer, style, output_dir='legends/type_test', type_param=type_param)


def generate_usage_report():
    """활용 방안 보고서를 생성합니다."""
    report = """
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
    \"\"\"VWorld 레전드 이미지 다운로드\"\"\"
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
    \"\"\"QGIS에서 레전드 표시\"\"\"
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
"""
    
    # 보고서 저장
    report_path = 'legends/LEGEND_USAGE_REPORT.md'
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n활용 방안 보고서 생성: {report_path}")
    return report


if __name__ == '__main__':
    # 모든 레이어 테스트
    results = test_all_layers()
    
    # TYPE 파라미터 테스트 (선택적)
    # test_type_parameters()
    
    # 활용 방안 보고서 생성
    generate_usage_report()
    
    print("\n" + "="*60)
    print("테스트 완료!")
    print("="*60)
    print("\n생성된 파일:")
    print("  - legends/ 디렉토리에 범례 이미지")
    print("  - legends/LEGEND_USAGE_REPORT.md - 활용 방안 보고서")

