# Vworld QGIS 플러그인 개발 가이드

> QuickOSM 플러그인 분석을 통한 Vworld API QGIS 플러그인 개발 레퍼런스

## 📋 개요

이 레퍼런스는 QGIS의 QuickOSM 플러그인을 분석하여 Vworld Open API를 활용한 QGIS 플러그인 개발을 위한 가이드를 제공합니다.

### 분석 대상
- **플러그인**: QuickOSM v2.4.1
- **기능**: OSM(OpenStreetMap) 데이터를 Overpass API를 통해 다운로드하고 QGIS 레이어로 생성
- **적용 대상**: Vworld Open API를 사용한 한국 공간 데이터 플러그인

## 📂 문서 구성

### 1. 메인 레퍼런스 문서
**파일**: `VWORLD_PLUGIN_REFERENCE.md`

포괄적인 플러그인 개발 가이드:
- 플러그인 디렉토리 구조
- 필수 파일 및 메타데이터
- 플러그인 진입점 및 초기화
- API 연결 및 데이터 다운로드
- 데이터 파싱 및 레이어 생성
- UI 구성 요소
- Processing 알고리즘 등록
- QGIS 내부 API 활용
- 코드 스니펫 모음

### 2. 코드 스니펫 (`code_snippets/`)

실제 사용 가능한 코드 예제:

#### 01. 플러그인 진입점 (`01_plugin_entry.py`)
- `__init__.py` 구현
- `classFactory` 함수

#### 02. 메인 플러그인 클래스 (`02_main_plugin_class.py`)
- 플러그인 초기화
- GUI 설정
- Processing 등록
- 언로드 처리

#### 03. API 다운로더 (`03_api_downloader.py`)
- `QgsFileDownloader` 사용
- 동기식 다운로드 구현
- GET/POST 요청

#### 04. Vworld API 클라이언트 (`04_vworld_api_client.py`)
- Vworld API URL 생성
- 데이터 다운로드
- 응답 검증

#### 05. 레이어 생성 (`05_layer_creation.py`)
- 벡터 레이어 생성
- 메타데이터 추가
- 프로젝트에 추가
- 스타일 적용

#### 06. Processing 알고리즘 (`06_processing_algorithm.py`)
- `QgsProcessingAlgorithm` 구현
- 파라미터 정의
- Processing Provider

#### 07. 전체 워크플로우 (`07_complete_workflow.py`)
- 통합 프로세스
- 진행 상황 표시
- 레이어 재로드

#### 08. 예외 처리 (`08_exception_handling.py`)
- 커스텀 예외 클래스
- 예외 처리 헬퍼
- 사용자 친화적 에러 표시

## 🚀 빠른 시작

### 1. 기본 플러그인 구조 생성

```bash
VworldPlugin/
├── __init__.py
├── metadata.txt
├── vworld_plugin.py
├── core/
│   └── api/
├── ui/
├── processing/
└── resources/
```

### 2. 필수 파일 작성

#### `__init__.py`
```python
def classFactory(iface):
    from VworldPlugin.vworld_plugin import VworldPlugin
    return VworldPlugin(iface)
```

#### `metadata.txt`
```ini
[general]
name=Vworld Plugin
qgisMinimumVersion=3.22
description=Download Vworld data
hasProcessingProvider=yes
```

### 3. 메인 클래스 구현

`code_snippets/02_main_plugin_class.py` 참고

### 4. API 연결 구현

`code_snippets/04_vworld_api_client.py` 참고

## 🔧 핵심 기능 구현

### API 데이터 다운로드

```python
from VworldPlugin.core.api.vworld_api import build_vworld_url, VworldAPI

# URL 생성
url = build_vworld_url(
    service='wfs',
    request='GetFeature',
    api_key='YOUR_KEY',
    typename='lt_c_aisresc',
    bbox='126.9,37.5,127.0,37.6'
)

# 다운로드
client = VworldAPI(url, 'YOUR_KEY')
data_file = client.fetch_data()
```

### 레이어 생성

```python
from VworldPlugin.core.parser.data_parser import create_and_load_layer

layer = create_and_load_layer(
    data_file,
    'Buildings',
    add_to_project=True,
    apply_style=True
)
```

### 전체 프로세스

```python
from VworldPlugin.core.process import download_vworld_data

num_layers = download_vworld_data(
    api_key='YOUR_KEY',
    layer_type='lt_c_aisresc',
    bbox=bbox,
    layer_name='Seoul Buildings'
)
```

## 📊 주요 QGIS API

### 레이어 관리
```python
from qgis.core import QgsVectorLayer, QgsProject

layer = QgsVectorLayer(path, name, "ogr")
QgsProject.instance().addMapLayer(layer)
```

### 네트워크 요청
```python
from qgis.core import QgsFileDownloader

downloader = QgsFileDownloader(url, output_path)
```

### Processing 알고리즘
```python
from qgis.core import QgsProcessingAlgorithm

class MyAlgorithm(QgsProcessingAlgorithm):
    def processAlgorithm(self, parameters, context, feedback):
        # 구현
        pass
```

### UI 메시지
```python
from qgis.core import Qgis

iface.messageBar().pushMessage(
    "Title",
    "Message",
    level=Qgis.Info
)
```

## 🎯 Vworld API 레이어 타입

### 주요 레이어

| 레이어 ID | 설명 | 비고 |
|-----------|------|------|
| `lt_c_aisresc` | 건물 | 건축물대장 |
| `lt_c_ademd_info` | 행정동 | 행정구역 |
| `lt_c_uq151` | 도로 | 도로명주소 |
| `lp_pa_cbnd_bonbun` | 토지 | 토지이용 |
| `lt_c_wkmbbsn` | 상수도 | 상수도관로 |

### API 요청 예제

```python
# WFS GetFeature
url = build_vworld_url(
    service='wfs',
    request='GetFeature',
    api_key='YOUR_KEY',
    typename='lt_c_aisresc',
    bbox='126.9,37.5,127.0,37.6',
    srsname='EPSG:4326',
    maxFeatures=1000
)

# WMS GetMap
url = build_vworld_url(
    service='wms',
    request='GetMap',
    api_key='YOUR_KEY',
    layers='lt_c_aisresc',
    bbox='126.9,37.5,127.0,37.6',
    width=512,
    height=512
)
```

## 🛠️ 개발 환경 설정

### 1. QGIS 설치
```bash
# Windows
choco install qgis

# Ubuntu
sudo apt install qgis
```

### 2. 플러그인 디렉토리
- **Windows**: `C:\Users\{username}\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins`
- **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`
- **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins`

### 3. 개발 도구
- **Qt Designer**: UI 디자인
- **PyCharm** 또는 **VS Code**: IDE
- **Plugin Reloader**: 플러그인 재로드

## 📚 QuickOSM에서 배운 패턴

### 1. 모듈화된 구조
- `core/`: 비즈니스 로직
- `ui/`: 사용자 인터페이스
- `processing/`: Processing 알고리즘
- `definitions/`: 상수 및 Enum

### 2. API 연결 패턴
- `Downloader` 베이스 클래스
- `ConnexionOAPI` (Vworld의 경우 `VworldAPI`)
- 동기식 다운로드 (QEventLoop)

### 3. 데이터 처리 흐름
```
API 요청 → 다운로드 → 파싱 → 레이어 생성 → 프로젝트 추가
```

### 4. 에러 처리
- 커스텀 예외 클래스
- 사용자 친화적 메시지
- 상세 정보 제공

### 5. UI 패턴
- 베이스 패널 클래스
- 시그널/슬롯 연결
- 진행 상황 표시

## 🔍 디버깅 팁

### 1. 로깅
```python
import logging
LOGGER = logging.getLogger('VworldPlugin')
LOGGER.info("Debug message")
```

### 2. QGIS 로그 패널
```python
from qgis.core import QgsMessageLog, Qgis

QgsMessageLog.logMessage(
    "Debug info",
    "VworldPlugin",
    Qgis.Info
)
```

### 3. Python 콘솔
QGIS Python 콘솔에서 직접 테스트 가능

### 4. Plugin Reloader
개발 중 플러그인을 다시 컴파일하지 않고 재로드

## 🌐 참고 자료

### QGIS 공식 문서
- **PyQGIS Developer Cookbook**: https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/
- **QGIS Python API**: https://qgis.org/pyqgis/
- **Plugin Development**: https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/plugins/

### QuickOSM 플러그인
- **GitHub**: https://github.com/3liz/QuickOSM
- **문서**: https://docs.3liz.org/QuickOSM/

### Vworld Open API
- **API 문서**: https://www.vworld.kr/dev/v4dv_apiref2_s001.do
- **서비스 신청**: https://www.vworld.kr/dev/v4dv_2ddataguide2_s001.do

### Qt/PyQt
- **Qt Designer**: UI 디자인 도구
- **PyQt5 Documentation**: https://www.riverbankcomputing.com/static/Docs/PyQt5/

## 💡 모범 사례

### 1. 코드 구조
- 관심사의 분리 (UI, 비즈니스 로직, 데이터)
- 재사용 가능한 컴포넌트
- 명확한 책임 분리

### 2. 에러 처리
- 모든 API 호출에 예외 처리
- 사용자 친화적 에러 메시지
- 로그에 상세 정보 기록

### 3. 성능
- 대용량 데이터는 페이징 처리
- 비동기 처리 (필요 시)
- 임시 파일 정리

### 4. 사용자 경험
- 진행 상황 표시
- 취소 가능한 작업
- 명확한 피드백

### 5. 문서화
- 주석 작성
- docstring 추가
- README 제공

## 🚦 개발 체크리스트

### 필수 파일
- [ ] `__init__.py` (classFactory)
- [ ] `metadata.txt`
- [ ] 메인 플러그인 클래스
- [ ] 아이콘 파일

### 기능 구현
- [ ] API 연결
- [ ] 데이터 다운로드
- [ ] 레이어 생성
- [ ] UI 다이얼로그
- [ ] Processing 알고리즘 (선택)

### 품질
- [ ] 에러 처리
- [ ] 로깅
- [ ] 진행 상황 표시
- [ ] 다국어 지원 (선택)

### 테스트
- [ ] API 연결 테스트
- [ ] 레이어 생성 테스트
- [ ] 에러 케이스 테스트
- [ ] 다양한 QGIS 버전 테스트

## 📝 라이선스

이 레퍼런스 문서는 QuickOSM 플러그인(GPL v3)을 분석하여 작성되었습니다.

## 🤝 기여

개선 사항이나 오류를 발견하시면 이슈를 등록해주세요.

---

**작성일**: 2025-11-11  
**기반 플러그인**: QuickOSM v2.4.1  
**작성자**: Plugin Developer  
**목적**: Vworld API QGIS 플러그인 개발 레퍼런스

