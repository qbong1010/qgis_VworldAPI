# QGIS 플러그인 개발 레퍼런스 (QuickOSM 기반)
> Vworld API 플러그인 개발을 위한 QuickOSM 플러그인 구조 분석 문서

## 목차
1. [플러그인 디렉토리 구조](#1-플러그인-디렉토리-구조)
2. [필수 파일 및 메타데이터](#2-필수-파일-및-메타데이터)
3. [플러그인 진입점 및 초기화](#3-플러그인-진입점-및-초기화)
4. [API 연결 및 데이터 다운로드](#4-api-연결-및-데이터-다운로드)
5. [데이터 파싱 및 레이어 생성](#5-데이터-파싱-및-레이어-생성)
6. [UI 구성 요소](#6-ui-구성-요소)
7. [Processing 알고리즘 등록](#7-processing-알고리즘-등록)
8. [QGIS 내부 API 활용](#8-qgis-내부-api-활용)
9. [코드 스니펫 모음](#9-코드-스니펫-모음)

---

## 1. 플러그인 디렉토리 구조

QGIS 플러그인은 다음과 같은 표준 구조를 따릅니다:

```
VworldPlugin/
├── __init__.py                 # 플러그인 진입점 (classFactory)
├── metadata.txt                # 플러그인 메타데이터 (필수)
├── vworld_plugin.py            # 메인 플러그인 클래스
│
├── core/                       # 핵심 로직
│   ├── __init__.py
│   ├── api/                    # API 연결
│   │   ├── __init__.py
│   │   ├── vworld_api.py       # Vworld API 클라이언트
│   │   └── downloader.py       # 다운로더
│   ├── parser/                 # 데이터 파싱
│   │   ├── __init__.py
│   │   └── data_parser.py
│   ├── process.py              # 데이터 처리 흐름
│   └── utilities/              # 유틸리티
│       ├── __init__.py
│       └── tools.py
│
├── ui/                         # UI 컴포넌트
│   ├── __init__.py
│   ├── dialog.py               # 메인 다이얼로그
│   ├── base_panel.py           # 패널 베이스 클래스
│   └── query_panel.py          # 쿼리 패널
│
├── processing/                 # Processing 알고리즘
│   ├── __init__.py
│   ├── provider.py             # Processing Provider
│   └── algorithms/
│       ├── __init__.py
│       └── download_data.py
│
├── resources/                  # 리소스 파일
│   ├── icons/                  # 아이콘
│   ├── ui/                     # Qt Designer UI 파일
│   │   └── main_window.ui
│   └── styles/                 # QML 스타일
│
├── i18n/                       # 다국어 번역 파일
│   └── vworld_ko.qm
│
└── definitions/                # 정의 및 상수
    ├── __init__.py
    └── constants.py
```

### 핵심 디렉토리 설명

- **core/**: 비즈니스 로직, API 통신, 데이터 처리
- **ui/**: 사용자 인터페이스 컴포넌트
- **processing/**: QGIS Processing 프레임워크 통합
- **resources/**: 아이콘, UI 파일, 스타일 등
- **i18n/**: 다국어 지원 파일
- **definitions/**: 상수, Enum 정의

---

## 2. 필수 파일 및 메타데이터

### 2.1 `__init__.py` (플러그인 진입점)

QGIS가 플러그인을 로드하기 위해 반드시 필요한 파일입니다.

```python
"""Vworld Plugin init."""

__copyright__ = 'Copyright 2025, Your Organization'
__license__ = 'GPL version 3'
__email__ = 'your@email.com'


# noinspection PyDocstring,PyPep8Naming
def classFactory(iface):
    """플러그인 로드 진입점"""
    from VworldPlugin.vworld_plugin import VworldPlugin
    return VworldPlugin(iface)
```

### 2.2 `metadata.txt` (플러그인 메타데이터)

플러그인의 메타정보를 정의하는 필수 파일입니다.

```ini
[general]
name=Vworld Plugin
qgisMinimumVersion=3.22
qgisMaximumVersion=3.99
description=Download Vworld data using Vworld API
about=Fetch geospatial data from Vworld Open API and create QGIS layers
author=Your Name
email=your@email.com
hasProcessingProvider=yes
server=False

# Version information
version=1.0.0
changelog=
 Version 1.0.0:
 * Initial release
 * Vworld API integration

# Tags
tags=vworld,download,korea,open data,api

# Links
homepage=https://github.com/your-repo
tracker=https://github.com/your-repo/issues
repository=https://github.com/your-repo
icon=resources/icons/vworld_icon.svg

# Status flags
experimental=False
deprecated=False
```

**주요 필드 설명:**
- `hasProcessingProvider=yes`: Processing 알고리즘 제공
- `qgisMinimumVersion`: 최소 QGIS 버전
- `server=False`: 서버 플러그인 아님

---

## 3. 플러그인 진입점 및 초기화

### 3.1 메인 플러그인 클래스 (`vworld_plugin.py`)

```python
"""Vworld Plugin main entry point."""

import logging
from qgis.core import Qgis, QgsApplication
from qgis.PyQt.QtCore import QCoreApplication, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu

from VworldPlugin.processing.provider import VworldProvider
from VworldPlugin.ui.dialog import VworldDialog

LOGGER = logging.getLogger('VworldPlugin')


class VworldPlugin:
    """메인 플러그인 클래스"""

    def __init__(self, iface):
        """
        생성자
        
        :param iface: QGIS 인터페이스 인스턴스
        :type iface: QgsInterface
        """
        self.iface = iface
        
        # 번역 설정
        self.setup_translation()
        
        # Processing Provider
        self.provider = None
        
        # UI 요소
        self.toolbar = None
        self.menu = None
        self.main_action = None

    def setup_translation(self):
        """다국어 번역 설정"""
        locale = QgsSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            os.path.dirname(__file__),
            'i18n',
            f'vworld_{locale}.qm'
        )
        
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

    def initProcessing(self):
        """Processing Provider 초기화"""
        self.provider = VworldProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        """사용자 인터페이스 초기화"""
        # Processing 초기화
        self.initProcessing()
        
        # 아이콘 설정
        icon = QIcon(os.path.join(
            os.path.dirname(__file__),
            'resources/icons/vworld_icon.svg'
        ))
        
        # 툴바 추가
        self.toolbar = self.iface.addToolBar('Vworld')
        self.toolbar.setObjectName('Vworld')
        
        # 메뉴 설정
        self.menu = QMenu('Vworld')
        self.menu.setIcon(icon)
        self.iface.vectorMenu().addMenu(self.menu)
        
        # 메인 액션
        self.main_action = QAction(
            icon, 
            'Vworld Data Download…', 
            self.iface.mainWindow()
        )
        self.main_action.triggered.connect(self.open_dialog)
        self.toolbar.addAction(self.main_action)
        self.menu.addAction(self.main_action)
        
        LOGGER.info("Vworld Plugin loaded successfully")

    def unload(self):
        """플러그인 언로드"""
        # 메뉴 제거
        self.iface.removePluginVectorMenu('&Vworld', self.main_action)
        
        # 툴바 아이콘 제거
        self.iface.removeToolBarIcon(self.main_action)
        
        # Processing Provider 제거
        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)

    def open_dialog(self):
        """메인 다이얼로그 열기"""
        dialog = VworldDialog(self.iface)
        dialog.exec()
```

**핵심 메서드:**
- `__init__`: 플러그인 초기화
- `initGui()`: UI 요소 생성 (필수)
- `unload()`: 플러그인 종료 시 정리 (필수)
- `initProcessing()`: Processing 알고리즘 등록

---

## 4. API 연결 및 데이터 다운로드

### 4.1 다운로더 베이스 클래스 (`core/api/downloader.py`)

```python
"""데이터 다운로더"""

import logging
from qgis.core import Qgis, QgsFileDownloader
from qgis.PyQt.QtCore import QByteArray, QEventLoop, QUrl

LOGGER = logging.getLogger('VworldPlugin')


class Downloader:
    """HTTP 다운로더 베이스 클래스"""

    def __init__(self, url: str = None):
        """생성자"""
        self._url = QUrl(url) if url else None
        self.result_path = None
        self.errors = []

    def error(self, messages: str):
        """에러 메시지 저장"""
        self.errors = messages
        LOGGER.error(f"Download error: {messages}")

    @staticmethod
    def canceled():
        """다운로드 취소"""
        LOGGER.info('Request canceled')

    @staticmethod
    def completed():
        """다운로드 완료"""
        LOGGER.info('Request completed')

    def download(self, use_post=False):
        """
        데이터 다운로드
        
        :param use_post: POST 방식 사용 여부
        """
        if use_post:
            # POST 요청
            downloader = QgsFileDownloader(
                self._url,
                self.result_path,
                delayStart=True,
                httpMethod=Qgis.HttpMethod.Post,
                data=QByteArray(str.encode("data=your_post_data"))
            )
        else:
            # GET 요청
            downloader = QgsFileDownloader(
                self._url, 
                self.result_path, 
                delayStart=True
            )
        
        # 이벤트 루프로 동기 처리
        loop = QEventLoop()
        downloader.downloadExited.connect(loop.quit)
        downloader.downloadError.connect(self.error)
        downloader.downloadCanceled.connect(self.canceled)
        downloader.downloadCompleted.connect(self.completed)
        downloader.startDownload()
        loop.exec()
```

### 4.2 Vworld API 클라이언트 (`core/api/vworld_api.py`)

```python
"""Vworld API 연결"""

import logging
import os
from qgis.PyQt.QtCore import QDir, QFileInfo, QTemporaryFile
from VworldPlugin.core.api.downloader import Downloader
from VworldPlugin.core.exceptions import VworldAPIException

LOGGER = logging.getLogger('VworldPlugin')


class VworldAPI(Downloader):
    """Vworld Open API 클라이언트"""

    def __init__(self, url: str, api_key: str):
        """
        생성자
        
        :param url: API 엔드포인트 URL
        :param api_key: Vworld API 키
        """
        super().__init__(url)
        self.api_key = api_key
        
        # 임시 파일 생성
        temporary = QTemporaryFile(
            os.path.join(QDir.tempPath(), 'vworld-XXXXXX.geojson')
        )
        temporary.open()
        self.result_path = temporary.fileName()
        temporary.close()

    def fetch_data(self, params: dict) -> str:
        """
        데이터 가져오기
        
        :param params: API 파라미터
        :return: 결과 파일 경로
        """
        # URL에 파라미터 추가
        from qgis.PyQt.QtCore import QUrlQuery
        query = QUrlQuery()
        query.addQueryItem('key', self.api_key)
        
        for key, value in params.items():
            query.addQueryItem(key, str(value))
        
        self._url.setQuery(query)
        
        LOGGER.info(f"Fetching data from: {self._url.toString()}")
        
        # 다운로드 실행
        self.download()
        
        # 에러 체크
        if self.errors:
            raise VworldAPIException(f"API Error: {', '.join(self.errors)}")
        
        # 파일 존재 확인
        file_info = QFileInfo(self.result_path)
        if not file_info.exists() or not file_info.isFile():
            raise FileNotFoundError(f"Downloaded file not found: {self.result_path}")
        
        return self.result_path


def build_vworld_url(
    service: str,
    request: str,
    api_key: str,
    **kwargs
) -> str:
    """
    Vworld API URL 생성
    
    :param service: 서비스 종류 (예: WFS)
    :param request: 요청 종류 (예: GetFeature)
    :param api_key: API 키
    :param kwargs: 추가 파라미터
    :return: 완성된 URL
    """
    base_url = "https://api.vworld.kr/req/{service}".format(service=service)
    
    # 기본 파라미터
    params = {
        'service': service,
        'request': request,
        'key': api_key,
        'format': 'json',
        'version': '2.0.0'
    }
    
    # 추가 파라미터 병합
    params.update(kwargs)
    
    # URL 구성
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    return f"{base_url}?{query_string}"
```

**Vworld API 예제:**
```python
# 사용 예시
api_url = build_vworld_url(
    service='wfs',
    request='GetFeature',
    api_key='YOUR_API_KEY',
    typename='lt_c_aisresc',  # 레이어명
    bbox='126.9,37.5,127.0,37.6'  # 영역
)

client = VworldAPI(api_url, 'YOUR_API_KEY')
result_file = client.fetch_data({})
```

---

## 5. 데이터 파싱 및 레이어 생성

### 5.1 데이터 파서 (`core/parser/data_parser.py`)

```python
"""데이터 파서 및 레이어 생성"""

import logging
from qgis.core import (
    QgsVectorLayer,
    QgsProject,
    QgsLayerMetadata,
    QgsWkbTypes,
    QgsField
)
from qgis.PyQt.QtCore import QVariant

LOGGER = logging.getLogger('VworldPlugin')


class VworldParser:
    """Vworld 데이터 파서"""

    def __init__(
        self,
        data_file: str,
        layer_name: str = "Vworld Layer",
        output_format: str = "GeoJSON"
    ):
        """
        생성자
        
        :param data_file: 데이터 파일 경로
        :param layer_name: 레이어 이름
        :param output_format: 출력 포맷
        """
        self.data_file = data_file
        self.layer_name = layer_name
        self.output_format = output_format

    def create_layer(self) -> QgsVectorLayer:
        """
        벡터 레이어 생성
        
        :return: 생성된 레이어
        """
        LOGGER.info(f"Creating layer from: {self.data_file}")
        
        # GeoJSON 레이어 생성
        layer = QgsVectorLayer(
            self.data_file,
            self.layer_name,
            "ogr"
        )
        
        if not layer.isValid():
            raise Exception(f"Layer is not valid: {self.data_file}")
        
        # 인코딩 설정
        layer.setProviderEncoding('UTF-8')
        
        # 메타데이터 추가
        self.add_metadata(layer)
        
        return layer

    def add_metadata(self, layer: QgsVectorLayer):
        """레이어에 메타데이터 추가"""
        metadata = QgsLayerMetadata()
        metadata.setRights(['© Vworld Open API'])
        metadata.setLicenses(['Vworld Open API License'])
        layer.setMetadata(metadata)

    def add_to_project(self, layer: QgsVectorLayer):
        """프로젝트에 레이어 추가"""
        QgsProject.instance().addMapLayer(layer)
        LOGGER.info(f"Layer added to project: {layer.name()}")


def process_and_load_data(
    data_file: str,
    layer_name: str = "Vworld Data",
    add_to_project: bool = True
) -> QgsVectorLayer:
    """
    데이터 처리 및 로드
    
    :param data_file: 데이터 파일 경로
    :param layer_name: 레이어 이름
    :param add_to_project: 프로젝트에 추가 여부
    :return: 생성된 레이어
    """
    parser = VworldParser(data_file, layer_name)
    layer = parser.create_layer()
    
    if add_to_project:
        parser.add_to_project(layer)
    
    return layer
```

### 5.2 전체 프로세스 (`core/process.py`)

```python
"""전체 데이터 처리 프로세스"""

import logging
from qgis.core import QgsFeedback
from qgis.PyQt.QtWidgets import QDialog

from VworldPlugin.core.api.vworld_api import VworldAPI, build_vworld_url
from VworldPlugin.core.parser.data_parser import process_and_load_data

LOGGER = logging.getLogger('VworldPlugin')


def download_vworld_data(
    api_key: str,
    layer_type: str,
    bbox: str = None,
    layer_name: str = "Vworld Data",
    dialog: QDialog = None,
    feedback: QgsFeedback = None
) -> int:
    """
    Vworld 데이터 다운로드 및 레이어 생성
    
    :param api_key: Vworld API 키
    :param layer_type: 레이어 타입 (예: 'lt_c_aisresc')
    :param bbox: 바운딩 박스 (minx,miny,maxx,maxy)
    :param layer_name: 레이어 이름
    :param dialog: 다이얼로그 (진행상황 표시용)
    :param feedback: 피드백 객체
    :return: 생성된 레이어 수
    """
    
    if dialog:
        dialog.set_progress_text('Vworld API 연결 중...')
    
    # API URL 생성
    api_url = build_vworld_url(
        service='wfs',
        request='GetFeature',
        api_key=api_key,
        typename=layer_type,
        bbox=bbox if bbox else '',
        srsname='EPSG:4326'
    )
    
    # 데이터 다운로드
    if dialog:
        dialog.set_progress_text('데이터 다운로드 중...')
    
    client = VworldAPI(api_url, api_key)
    data_file = client.fetch_data({})
    
    if feedback and feedback.isCanceled():
        return 0
    
    # 레이어 생성 및 추가
    if dialog:
        dialog.set_progress_text('레이어 생성 중...')
    
    layer = process_and_load_data(data_file, layer_name)
    
    LOGGER.info(f"Successfully created layer: {layer.name()}")
    
    return 1
```

---

## 6. UI 구성 요소

### 6.1 베이스 패널 클래스 (`ui/base_panel.py`)

```python
"""패널 베이스 클래스"""

from qgis.PyQt.QtWidgets import QDialog


class BasePanel:
    """UI 패널 베이스 클래스"""

    def __init__(self, dialog: QDialog):
        self._dialog = dialog

    @property
    def dialog(self) -> QDialog:
        """다이얼로그 반환"""
        return self._dialog

    def setup_panel(self):
        """패널 설정 (서브클래스에서 구현)"""
        raise NotImplementedError
```

### 6.2 메인 다이얼로그 (`ui/dialog.py`)

```python
"""메인 다이얼로그"""

import logging
from qgis.core import Qgis, QgsFeedback
from qgis.PyQt.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QPushButton,
    QLineEdit,
    QComboBox,
    QProgressBar,
    QLabel
)

from VworldPlugin.core.process import download_vworld_data
from VworldPlugin.core.exceptions import VworldException

LOGGER = logging.getLogger('VworldPlugin')


class VworldDialog(QDialog):
    """메인 다이얼로그"""

    def __init__(self, iface, parent=None):
        """생성자"""
        super().__init__(parent)
        self.iface = iface
        self.feedback = QgsFeedback()
        
        self.setup_ui()

    def setup_ui(self):
        """UI 설정"""
        self.setWindowTitle('Vworld Data Download')
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # API 키 입력
        self.api_key_label = QLabel('API Key:')
        layout.addWidget(self.api_key_label)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText('Vworld API Key를 입력하세요')
        layout.addWidget(self.api_key_input)
        
        # 레이어 타입 선택
        self.layer_type_label = QLabel('Layer Type:')
        layout.addWidget(self.layer_type_label)
        
        self.layer_type_combo = QComboBox()
        self.layer_type_combo.addItems([
            'lt_c_aisresc',  # 건물
            'lt_c_ademd_info',  # 행정동
            # ... 추가 레이어
        ])
        layout.addWidget(self.layer_type_combo)
        
        # 진행 상태
        self.progress_label = QLabel('')
        layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        # 실행 버튼
        self.run_button = QPushButton('데이터 다운로드')
        self.run_button.clicked.connect(self.run_download)
        layout.addWidget(self.run_button)
        
        self.setLayout(layout)

    def set_progress_text(self, text: str):
        """진행 텍스트 설정"""
        self.progress_label.setText(text)

    def set_progress_percentage(self, percent: int):
        """진행률 설정"""
        self.progress_bar.setValue(percent)

    def run_download(self):
        """다운로드 실행"""
        api_key = self.api_key_input.text().strip()
        
        if not api_key:
            self.iface.messageBar().pushWarning(
                'Vworld Plugin',
                'API Key를 입력해주세요.'
            )
            return
        
        layer_type = self.layer_type_combo.currentText()
        
        try:
            self.run_button.setEnabled(False)
            self.set_progress_percentage(0)
            
            # 데이터 다운로드
            download_vworld_data(
                api_key=api_key,
                layer_type=layer_type,
                layer_name=layer_type,
                dialog=self,
                feedback=self.feedback
            )
            
            self.set_progress_percentage(100)
            self.iface.messageBar().pushSuccess(
                'Vworld Plugin',
                '데이터가 성공적으로 다운로드되었습니다.'
            )
            
        except VworldException as e:
            LOGGER.error(f"Vworld error: {e}")
            self.iface.messageBar().pushCritical(
                'Vworld Plugin',
                str(e)
            )
        except Exception as e:
            LOGGER.exception(e)
            self.iface.messageBar().pushCritical(
                'Vworld Plugin',
                f'오류 발생: {str(e)}'
            )
        finally:
            self.run_button.setEnabled(True)
```

---

## 7. Processing 알고리즘 등록

### 7.1 Provider (`processing/provider.py`)

```python
"""Processing Provider"""

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from VworldPlugin.processing.algorithms.download_data import DownloadVworldData


class VworldProvider(QgsProcessingProvider):
    """Vworld Processing Provider"""

    def id(self) -> str:
        """Provider ID"""
        return 'vworld'

    def name(self) -> str:
        """Provider 이름"""
        return 'Vworld'

    def icon(self):
        """아이콘"""
        return QIcon('path/to/icon.svg')

    def loadAlgorithms(self):
        """알고리즘 로드"""
        self.addAlgorithm(DownloadVworldData())
```

### 7.2 알고리즘 예제 (`processing/algorithms/download_data.py`)

```python
"""Vworld 데이터 다운로드 알고리즘"""

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterString,
    QgsProcessingParameterEnum,
    QgsProcessingOutputVectorLayer,
    QgsProcessingException
)

from VworldPlugin.core.process import download_vworld_data


class DownloadVworldData(QgsProcessingAlgorithm):
    """Vworld 데이터 다운로드 알고리즘"""

    # 파라미터 이름
    API_KEY = 'API_KEY'
    LAYER_TYPE = 'LAYER_TYPE'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def name(self):
        """알고리즘 ID"""
        return 'downloadvworlddata'

    def displayName(self):
        """표시 이름"""
        return 'Download Vworld Data'

    def group(self):
        """그룹"""
        return 'Download'

    def groupId(self):
        """그룹 ID"""
        return 'download'

    def shortHelpString(self):
        """도움말"""
        return 'Download data from Vworld Open API'

    def initAlgorithm(self, config=None):
        """알고리즘 초기화"""
        
        # API Key 파라미터
        self.addParameter(
            QgsProcessingParameterString(
                self.API_KEY,
                'Vworld API Key',
                defaultValue=''
            )
        )
        
        # Layer Type 파라미터
        self.addParameter(
            QgsProcessingParameterEnum(
                self.LAYER_TYPE,
                'Layer Type',
                options=[
                    'Building (lt_c_aisresc)',
                    'Administrative Dong (lt_c_ademd_info)'
                ],
                defaultValue=0
            )
        )
        
        # Output
        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT,
                'Output Layer'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """알고리즘 실행"""
        
        # 파라미터 가져오기
        api_key = self.parameterAsString(parameters, self.API_KEY, context)
        layer_type_idx = self.parameterAsEnum(parameters, self.LAYER_TYPE, context)
        
        layer_types = ['lt_c_aisresc', 'lt_c_ademd_info']
        layer_type = layer_types[layer_type_idx]
        
        if not api_key:
            raise QgsProcessingException('API Key is required')
        
        feedback.pushInfo(f'Downloading {layer_type}...')
        
        # 데이터 다운로드
        try:
            download_vworld_data(
                api_key=api_key,
                layer_type=layer_type,
                layer_name=layer_type,
                feedback=feedback
            )
        except Exception as e:
            raise QgsProcessingException(str(e))
        
        return {self.OUTPUT: layer_type}

    def createInstance(self):
        """인스턴스 생성"""
        return DownloadVworldData()
```

---

## 8. QGIS 내부 API 활용

### 8.1 레이어 관련 API

```python
from qgis.core import (
    QgsVectorLayer,
    QgsProject,
    QgsLayerMetadata,
    QgsField,
    QgsFeature
)
from qgis.PyQt.QtCore import QVariant

# 레이어 생성
layer = QgsVectorLayer("path/to/file.geojson", "Layer Name", "ogr")

# 레이어 유효성 검사
if layer.isValid():
    print("Layer is valid")

# 프로젝트에 레이어 추가
QgsProject.instance().addMapLayer(layer)

# 레이어 메타데이터 설정
metadata = QgsLayerMetadata()
metadata.setRights(['© Copyright Info'])
metadata.setLicenses(['License Info'])
layer.setMetadata(metadata)

# 레이어에서 feature 가져오기
features = layer.getFeatures()
for feature in features:
    print(feature.attributes())

# 필드 추가
layer.startEditing()
provider = layer.dataProvider()
provider.addAttributes([
    QgsField('new_field', QVariant.String)
])
layer.updateFields()
layer.commitChanges()
```

### 8.2 UI 관련 API

```python
from qgis.PyQt.QtWidgets import QMessageBox, QProgressBar
from qgis.core import Qgis

# 메시지 바 사용
iface.messageBar().pushMessage(
    "Title",
    "Message text",
    level=Qgis.Info,  # Info, Warning, Critical, Success
    duration=5  # 초
)

# 메시지 박스
QMessageBox.information(None, "Title", "Message")
QMessageBox.warning(None, "Title", "Warning")
QMessageBox.critical(None, "Title", "Error")

# 진행 표시
progress = QProgressBar()
progress.setMaximum(100)
progress.setValue(50)
```

### 8.3 Processing 관련 API

```python
import processing
from qgis.core import QgsProcessingFeedback

# Processing 알고리즘 실행
feedback = QgsProcessingFeedback()

result = processing.run(
    "native:buffer",
    {
        'INPUT': layer,
        'DISTANCE': 100,
        'OUTPUT': 'memory:'
    },
    feedback=feedback
)

buffered_layer = result['OUTPUT']
```

### 8.4 캔버스 및 좌표계 API

```python
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsRectangle,
    QgsProject
)

# 현재 캔버스 영역 가져오기
canvas = iface.mapCanvas()
extent = canvas.extent()

# 좌표계 변환
source_crs = QgsCoordinateReferenceSystem("EPSG:4326")
dest_crs = QgsCoordinateReferenceSystem("EPSG:5186")  # Korea 2000

transform = QgsCoordinateTransform(
    source_crs,
    dest_crs,
    QgsProject.instance()
)

transformed_extent = transform.transformBoundingBox(extent)

# 바운딩 박스
bbox = QgsRectangle(126.9, 37.5, 127.0, 37.6)
bbox_string = f"{bbox.xMinimum()},{bbox.yMinimum()},{bbox.xMaximum()},{bbox.yMaximum()}"
```

### 8.5 설정 저장/불러오기

```python
from qgis.PyQt.QtCore import QSettings

# 설정 저장
settings = QSettings()
settings.setValue('vworld_plugin/api_key', 'your_api_key')
settings.setValue('vworld_plugin/last_layer_type', 'lt_c_aisresc')

# 설정 불러오기
api_key = settings.value('vworld_plugin/api_key', '')
last_layer = settings.value('vworld_plugin/last_layer_type', '')
```

---

## 9. 코드 스니펫 모음

### 9.1 네트워크 요청

```python
"""네트워크 요청 스니펫"""

from qgis.core import QgsNetworkAccessManager, QgsBlockingNetworkRequest
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest
import json

def fetch_json_data(url: str) -> dict:
    """JSON 데이터 가져오기"""
    request = QNetworkRequest(QUrl(url))
    request.setHeader(
        QNetworkRequest.ContentTypeHeader,
        "application/json"
    )
    
    blocking_request = QgsBlockingNetworkRequest()
    error = blocking_request.get(request)
    
    if error == QgsBlockingNetworkRequest.NoError:
        reply = blocking_request.reply()
        content = reply.content()
        return json.loads(bytes(content))
    else:
        raise Exception(f"Network error: {error}")
```

### 9.2 임시 파일 생성

```python
"""임시 파일 생성"""

from qgis.PyQt.QtCore import QTemporaryFile, QDir
import os

def create_temp_file(suffix: str = '.geojson') -> str:
    """임시 파일 생성"""
    temp_file = QTemporaryFile(
        os.path.join(QDir.tempPath(), f'vworld-XXXXXX{suffix}')
    )
    temp_file.setAutoRemove(False)
    temp_file.open()
    path = temp_file.fileName()
    temp_file.close()
    return path
```

### 9.3 레이어 스타일 적용

```python
"""레이어 스타일"""

from qgis.core import (
    QgsSymbol,
    QgsSingleSymbolRenderer,
    QgsCategorizedSymbolRenderer,
    QgsRendererCategory,
    QgsWkbTypes
)
from qgis.PyQt.QtGui import QColor

def apply_simple_style(layer, color='red'):
    """단순 스타일 적용"""
    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol.setColor(QColor(color))
    renderer = QgsSingleSymbolRenderer(symbol)
    layer.setRenderer(renderer)
    layer.triggerRepaint()

def apply_categorized_style(layer, field_name):
    """카테고리별 스타일"""
    # 고유 값 가져오기
    unique_values = layer.uniqueValues(
        layer.fields().indexOf(field_name)
    )
    
    categories = []
    colors = ['red', 'blue', 'green', 'yellow', 'orange']
    
    for i, value in enumerate(unique_values):
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        symbol.setColor(QColor(colors[i % len(colors)]))
        category = QgsRendererCategory(
            value, 
            symbol, 
            str(value)
        )
        categories.append(category)
    
    renderer = QgsCategorizedSymbolRenderer(field_name, categories)
    layer.setRenderer(renderer)
    layer.triggerRepaint()
```

### 9.4 피처 필터링

```python
"""피처 필터링"""

from qgis.core import QgsExpression, QgsFeatureRequest

def filter_features(layer, expression_string):
    """표현식으로 피처 필터링"""
    expression = QgsExpression(expression_string)
    
    if expression.hasParserError():
        raise Exception(f"Expression error: {expression.parserErrorString()}")
    
    request = QgsFeatureRequest(expression)
    features = layer.getFeatures(request)
    
    return list(features)

# 사용 예
# filtered = filter_features(layer, "population > 1000")
```

### 9.5 에러 처리

```python
"""예외 처리 클래스"""

from qgis.core import Qgis

class VworldException(Exception):
    """Vworld 플러그인 예외"""
    
    def __init__(
        self, 
        message: str, 
        level: Qgis.MessageLevel = Qgis.Critical,
        duration: int = 5
    ):
        super().__init__(message)
        self.message = message
        self.level = level
        self.duration = duration


class VworldAPIException(VworldException):
    """API 관련 예외"""
    pass


class VworldDataException(VworldException):
    """데이터 처리 예외"""
    pass
```

### 9.6 로깅 설정

```python
"""로깅 설정"""

import logging
from qgis.core import Qgis, QgsMessageLog

def setup_logger(plugin_name: str) -> logging.Logger:
    """로거 설정"""
    logger = logging.getLogger(plugin_name)
    logger.setLevel(logging.INFO)
    
    # QGIS 로그 패널로 출력
    class QgsLogHandler(logging.Handler):
        def emit(self, record):
            log_message = self.format(record)
            level_map = {
                logging.DEBUG: Qgis.Info,
                logging.INFO: Qgis.Info,
                logging.WARNING: Qgis.Warning,
                logging.ERROR: Qgis.Critical,
                logging.CRITICAL: Qgis.Critical,
            }
            QgsMessageLog.logMessage(
                log_message,
                plugin_name,
                level_map.get(record.levelno, Qgis.Info)
            )
    
    handler = QgsLogHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
```

### 9.7 Qt Designer UI 로드

```python
"""UI 파일 로드"""

import os
from qgis.PyQt import uic

def load_ui(ui_file_name: str):
    """UI 파일 로드"""
    ui_file_path = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'ui',
        ui_file_name
    )
    return uic.loadUiType(ui_file_path)[0]

# 사용 예
# FORM_CLASS = load_ui('main_window.ui')
# class MyDialog(QDialog, FORM_CLASS):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
```

### 9.8 멀티쓰레딩

```python
"""멀티쓰레딩 처리"""

from qgis.PyQt.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    """다운로드 쓰레드"""
    
    # 시그널 정의
    finished = pyqtSignal(str)  # 완료 시 파일 경로
    error = pyqtSignal(str)     # 에러 메시지
    progress = pyqtSignal(int)  # 진행률
    
    def __init__(self, api_key, layer_type):
        super().__init__()
        self.api_key = api_key
        self.layer_type = layer_type
    
    def run(self):
        """쓰레드 실행"""
        try:
            # 다운로드 로직
            self.progress.emit(25)
            # ... 데이터 다운로드 ...
            self.progress.emit(75)
            # ... 처리 ...
            self.progress.emit(100)
            
            self.finished.emit('success')
        except Exception as e:
            self.error.emit(str(e))

# 사용 예
# thread = DownloadThread(api_key, layer_type)
# thread.finished.connect(on_finished)
# thread.error.connect(on_error)
# thread.progress.connect(on_progress)
# thread.start()
```

### 9.9 Vworld API 요청 예제

```python
"""Vworld API 요청 예제"""

def get_vworld_building_data(
    api_key: str,
    minx: float,
    miny: float,
    maxx: float,
    maxy: float
) -> str:
    """
    Vworld 건물 데이터 가져오기
    
    :param api_key: API 키
    :param minx: 최소 X 좌표
    :param miny: 최소 Y 좌표  
    :param maxx: 최대 X 좌표
    :param maxy: 최대 Y 좌표
    :return: GeoJSON 파일 경로
    """
    from VworldPlugin.core.api.vworld_api import build_vworld_url, VworldAPI
    
    # WFS GetFeature 요청
    url = build_vworld_url(
        service='wfs',
        request='GetFeature',
        api_key=api_key,
        typename='lt_c_aisresc',  # 건물
        bbox=f'{minx},{miny},{maxx},{maxy}',
        srsname='EPSG:4326',
        output='json',
        maxFeatures=1000
    )
    
    client = VworldAPI(url, api_key)
    result_file = client.fetch_data({})
    
    return result_file


def get_vworld_administrative_data(
    api_key: str,
    emd_cd: str = None  # 읍면동 코드
) -> str:
    """
    Vworld 행정구역 데이터
    
    :param api_key: API 키
    :param emd_cd: 읍면동 코드 (선택)
    :return: GeoJSON 파일 경로
    """
    from VworldPlugin.core.api.vworld_api import build_vworld_url, VworldAPI
    
    params = {
        'typename': 'lt_c_ademd_info',  # 행정동
    }
    
    if emd_cd:
        params['cql_filter'] = f"emd_cd='{emd_cd}'"
    
    url = build_vworld_url(
        service='wfs',
        request='GetFeature',
        api_key=api_key,
        **params
    )
    
    client = VworldAPI(url, api_key)
    result_file = client.fetch_data({})
    
    return result_file
```

---

## 요약

### QGIS 플러그인 개발 핵심 단계

1. **구조 설정**
   - `__init__.py`에 `classFactory` 함수 구현
   - `metadata.txt`에 플러그인 정보 작성

2. **메인 클래스 작성**
   - `initGui()`: UI 초기화
   - `unload()`: 정리 작업
   - `initProcessing()`: Processing 알고리즘 등록

3. **API 연동**
   - `QgsFileDownloader` 또는 `QgsBlockingNetworkRequest` 사용
   - 임시 파일로 데이터 저장

4. **데이터 처리**
   - `QgsVectorLayer`로 레이어 생성
   - `QgsProject.instance().addMapLayer()`로 추가

5. **UI 구성**
   - Qt Designer로 UI 설계 또는 코드로 작성
   - 시그널/슬롯으로 이벤트 처리

6. **Processing 통합**
   - `QgsProcessingProvider` 상속
   - `QgsProcessingAlgorithm` 구현

### 주요 QGIS API

- **레이어**: `QgsVectorLayer`, `QgsProject`
- **네트워크**: `QgsFileDownloader`, `QgsBlockingNetworkRequest`
- **UI**: `iface.messageBar()`, `QDialog`
- **Processing**: `QgsProcessingAlgorithm`, `processing.run()`
- **좌표계**: `QgsCoordinateReferenceSystem`, `QgsCoordinateTransform`

---

## 참고 자료

- QGIS Python API: https://qgis.org/pyqgis/
- PyQGIS Developer Cookbook: https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/
- QGIS Plugin Workshop: https://github.com/QGIS/QGIS-Documentation
- Vworld Open API: https://www.vworld.kr/dev/v4dv_apiref2_s001.do

---

**작성일**: 2025-11-11  
**기반 플러그인**: QuickOSM v2.4.1  
**목적**: Vworld API 플러그인 개발 레퍼런스

