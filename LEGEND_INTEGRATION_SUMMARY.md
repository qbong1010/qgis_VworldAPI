# VWorld GetLegendGraphic API 통합 완료 보고서

## 📋 작업 요약

VWorld Image API의 `GetLegendGraphic` 요청을 활용하여 QuickVworld 플러그인에 범례 표시 기능을 통합했습니다.

---

## ✅ 구현 완료 사항

### 1. API 테스트 및 검증

#### 테스트 결과
- **테스트 레이어**: 7개
- **성공률**: 100% (7/7)
- **다운로드된 범례 이미지**: `legends/` 디렉토리

#### 테스트한 레이어
| 레이어 코드 | 레이어 이름 | 이미지 크기 | 상태 |
|------------|------------|-----------|------|
| `lt_c_uq111` | 용도지구1종(개발진흥지구) | 11,283 bytes | ✅ 성공 |
| `lt_c_uq112` | 용도지구2종(경관지구) | 3,660 bytes | ✅ 성공 |
| `lt_c_uq113` | 용도지구3종(고도지구) | 2,925 bytes | ✅ 성공 |
| `lp_pa_cbnd_bonbun` | 연속지적도(본번) | 456 bytes | ✅ 성공 |
| `lp_pa_cbnd_bubun` | 연속지적도(부번) | 456 bytes | ✅ 성공 |
| `lt_c_upisuq153` | 도시계획시설(공간시설) | 4,976 bytes | ✅ 성공 |
| `lt_c_ademd` | 행정구역(읍면동) | 968 bytes | ✅ 성공 |

### 2. 새로운 모듈 구현

#### 2.1 `core/api/legend_client.py`
VWorld Legend API 클라이언트 모듈

**주요 클래스:**
```python
class VworldLegendClient(Downloader):
    """VWorld GetLegendGraphic API 클라이언트"""
    
    def fetch_legend(self, layer, style=None, legend_type='ALL')
    def fetch_legend_as_pixmap(self, layer, style=None, legend_type='ALL')
    def build_url(self)
```

**주요 함수:**
```python
def get_legend_url(layer, style=None, legend_type='ALL', api_key=None)
def download_legend(layer, style=None, legend_type='ALL', api_key=None)
def download_legend_pixmap(layer, style=None, legend_type='ALL', api_key=None)
```

#### 2.2 `ui/legend_dialog.py`
범례 표시 다이얼로그 모듈

**주요 클래스:**
```python
class LegendDialog(QDialog):
    """범례를 표시하는 다이얼로그"""
    
    def __init__(self, layer_name, layer_label=None, parent=None)
    def get_pixmap(self)
```

**주요 함수:**
```python
def show_legend_dialog(layer_name, layer_label=None, parent=None)
```

### 3. 기존 모듈 수정

#### 3.1 `ui/main_dialog.py`
- "범례 보기" 버튼 추가
- `show_legend()` 메서드 구현
- 범례 다이얼로그 통합

#### 3.2 `core/api/__init__.py`
- 범례 클라이언트 모듈 export 추가

#### 3.3 `ui/__init__.py`
- 범례 다이얼로그 모듈 export 추가

---

## 🔧 API 사용법

### GetLegendGraphic API 기본 정보

**API URL:**
```
https://api.vworld.kr/req/image
```

**필수 파라미터:**
- `service`: `image` (고정값)
- `request`: `GetLegendGraphic` (고정값)
- `format`: `png` (이미지 포맷)
- `layer`: 레이어 이름 (예: `lt_c_uq111`)
- `style`: 스타일 이름 (보통 레이어 이름과 동일)
- `type`: 범례 타입 (`ALL`, `POINT`, `LINE`, `POLYGON`)
- `key`: API 인증키

**요청 예제:**
```
https://api.vworld.kr/req/image?
service=image&
request=GetLegendGraphic&
format=png&
layer=lt_c_uq111&
style=lt_c_uq111&
type=ALL&
key=82E0F346-3308-3E16-AD90-3E36EB0A6895
```

---

## 💻 사용 예제

### 1. Python 코드에서 직접 사용

```python
from core.api.legend_client import download_legend_pixmap
from qgis.PyQt.QtWidgets import QLabel

# 범례 이미지 다운로드
pixmap = download_legend_pixmap('lt_c_upisuq153')

if pixmap:
    # QLabel에 표시
    label = QLabel()
    label.setPixmap(pixmap)
    label.show()
```

### 2. 범례 URL만 가져오기

```python
from core.api.legend_client import get_legend_url

url = get_legend_url('lt_c_upisuq153')
print(url)
# https://api.vworld.kr/req/image?service=image&request=GetLegendGraphic&...
```

### 3. 다이얼로그로 표시

```python
from ui.legend_dialog import show_legend_dialog

show_legend_dialog('lt_c_upisuq153', '도시계획시설(공간시설)')
```

### 4. 플러그인 UI에서 사용

QuickVworld 플러그인 메인 다이얼로그:
1. 레이어 타입 선택
2. "범례 보기" 버튼 클릭
3. 범례 다이얼로그 표시

---

## 🎯 활용 방안

### 1. 레이어 다운로드 시 범례 자동 표시

**구현 방법:**
```python
def download_data(self):
    # ... 기존 다운로드 코드 ...
    
    # 레이어 다운로드 후
    if layer:
        # 범례 다운로드 및 표시
        pixmap = download_legend_pixmap(typename)
        if pixmap:
            # 레이어 메타데이터에 저장
            layer.setCustomProperty('vworld_legend', True)
            
            # 사용자에게 범례 표시 여부 확인
            reply = QMessageBox.question(
                self, '범례 보기',
                '다운로드한 레이어의 범례를 확인하시겠습니까?',
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                show_legend_dialog(typename, layer_name)
```

### 2. 레이어 컨텍스트 메뉴에 추가

**구현 방법:**
```python
# quick_vworld.py에서
def add_layer_context_menu(self):
    """레이어 트리 컨텍스트 메뉴에 '범례 보기' 추가"""
    layer_tree_view = self.iface.layerTreeView()
    
    action = QAction("VWorld 범례 보기", self.iface.mainWindow())
    action.triggered.connect(self.show_layer_legend)
    
    layer_tree_view.addAction(action)

def show_layer_legend(self):
    """선택한 레이어의 범례 표시"""
    layer = self.iface.activeLayer()
    
    if layer and layer.customProperty('vworld_legend'):
        typename = layer.customProperty('vworld_typename')
        show_legend_dialog(typename, layer.name())
```

### 3. 범례 기반 스타일 자동 적용

**구현 아이디어:**
```python
from PIL import Image
import numpy as np

def extract_colors_from_legend(legend_path):
    """범례 이미지에서 색상 팔레트 추출"""
    img = Image.open(legend_path)
    pixels = np.array(img)
    
    # 주요 색상 추출 (k-means clustering 등)
    colors = extract_dominant_colors(pixels)
    
    return colors

def apply_legend_style(layer, typename):
    """범례 기반으로 레이어 스타일 적용"""
    # 범례 다운로드
    legend_path = download_legend(typename)
    
    if legend_path:
        # 색상 추출
        colors = extract_colors_from_legend(legend_path)
        
        # QGIS 스타일 적용
        # ... QML 생성 또는 심볼 직접 설정 ...
```

### 4. 오프라인 범례 캐싱

**구현 방법:**
```python
import os
import json
from pathlib import Path

class LegendCache:
    """범례 이미지 캐시 관리"""
    
    def __init__(self, cache_dir=None):
        if cache_dir is None:
            cache_dir = Path.home() / '.quickvworld' / 'legend_cache'
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.index_file = self.cache_dir / 'index.json'
        self.index = self._load_index()
    
    def get_cached_legend(self, typename):
        """캐시에서 범례 가져오기"""
        if typename in self.index:
            filepath = self.cache_dir / self.index[typename]['filename']
            if filepath.exists():
                return str(filepath)
        
        return None
    
    def cache_legend(self, typename, legend_path):
        """범례를 캐시에 저장"""
        filename = f"{typename}_legend.png"
        target_path = self.cache_dir / filename
        
        # 파일 복사
        import shutil
        shutil.copy(legend_path, target_path)
        
        # 인덱스 업데이트
        self.index[typename] = {
            'filename': filename,
            'cached_at': datetime.now().isoformat()
        }
        
        self._save_index()
    
    def _load_index(self):
        """인덱스 파일 로드"""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_index(self):
        """인덱스 파일 저장"""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)
```

### 5. 사용자 설정 추가

**구현 방법:**
```python
# 설정 다이얼로그에 추가
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 범례 자동 표시 옵션
        self.auto_show_legend_checkbox = QCheckBox(
            "레이어 다운로드 후 자동으로 범례 표시"
        )
        
        # 범례 캐싱 옵션
        self.cache_legends_checkbox = QCheckBox(
            "범례 이미지 캐싱 활성화 (오프라인 사용 가능)"
        )
        
        # ... UI 구성 ...
```

---

## 📊 범례 이미지 예시

### lt_c_uq111 (용도지구1종 - 개발진흥지구)
- 다양한 색상과 패턴으로 구분
- 경제자유구역, 복합용도지구, 산업유통개발진흥지구 등
- 크기: 11,283 bytes

### lt_c_upisuq153 (도시계획시설 - 공간시설)
- 광장, 공원, 녹지, 유원지 등
- 간단한 색상 구분
- 크기: 4,976 bytes

---

## 🔍 기술적 세부사항

### API 응답 형식
- **Content-Type**: `image/png`
- **이미지 포맷**: PNG
- **크기**: 레이어별로 다름 (약 456 bytes ~ 11 KB)

### 네트워크 고려사항
- **타임아웃**: 30초
- **재시도**: 현재 미구현 (향후 추가 가능)
- **오류 처리**: HTTP 상태 코드 및 Content-Type 검증

### 캐싱 전략
- 임시 파일로 다운로드 후 QPixmap으로 로드
- 필요 시 영구 저장소에 캐싱 가능
- 메모리 관리: QPixmap은 Qt 메모리 관리 시스템 사용

---

## 🚀 향후 개선 사항

### 1. 자동 스타일 적용
- 범례 이미지 분석하여 QGIS 심볼로지 자동 생성
- OCR로 범례 텍스트 추출
- 색상 팔레트 자동 추출 및 적용

### 2. 다국어 지원
- 한국어/영어 범례 지원 (API가 제공하는 경우)
- UI 언어에 따라 자동 선택

### 3. 대화형 범례
- 범례 항목 클릭 시 해당 피처만 표시
- 범례 기반 필터링 기능
- 범례와 맵 뷰 연동

### 4. 범례 편집 기능
- 다운로드한 범례를 기반으로 커스텀 범례 생성
- QML 스타일 파일로 저장
- 범례 이미지 주석 추가

### 5. 성능 최적화
- 범례 이미지 프리로딩
- 백그라운드 다운로드
- 썸네일 생성 및 캐싱

---

## 📚 참고 자료

### VWorld API 문서
- **WMS/WFS API 2.0**: https://www.vworld.kr/dev/v4dv_wmsguide2_s001.do
- **Image API**: GetLegendGraphic 요청 (WMS 표준 기반)

### OGC 표준
- **WMS 1.3.0**: https://www.ogc.org/standards/wms
- **GetLegendGraphic**: WMS 표준의 일부

### QGIS 문서
- **PyQGIS API**: https://qgis.org/pyqgis/
- **QPixmap**: https://doc.qt.io/qt-5/qpixmap.html
- **레이어 스타일링**: https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/

---

## 🎓 사용자 가이드

### 플러그인에서 범례 보기

1. **Quick Vworld 다이얼로그 열기**
   - QGIS 메뉴: `플러그인` > `Quick Vworld`
   
2. **레이어 선택**
   - "레이어 타입" 섹션에서 원하는 레이어 선택
   
3. **범례 보기**
   - "범례 보기" 버튼 클릭
   - 범례 다이얼로그가 표시되며 이미지 자동 다운로드
   
4. **범례 확인**
   - 범례 이미지 확인
   - 필요 시 스크롤하여 전체 범례 확인
   - "닫기" 버튼으로 다이얼로그 닫기

---

## 🐛 알려진 제약사항

1. **네트워크 연결 필요**
   - 범례 다운로드 시 인터넷 연결 필요
   - 오프라인 환경에서는 캐시된 범례만 사용 가능

2. **API 호출 제한**
   - VWorld API 키별 호출 제한 있음
   - 과도한 호출 시 제한될 수 있음

3. **일부 레이어 미지원**
   - 모든 VWorld 레이어가 범례를 제공하지는 않음
   - 범례 없는 경우 오류 메시지 표시

4. **이미지 품질**
   - API에서 제공하는 이미지 품질에 의존
   - 고해상도 범례는 제공되지 않을 수 있음

---

## ✨ 결론

VWorld GetLegendGraphic API를 성공적으로 QuickVworld 플러그인에 통합했습니다.

**주요 성과:**
- ✅ 7개 레이어 테스트 완료 (100% 성공률)
- ✅ 범례 다운로드 클라이언트 모듈 구현
- ✅ 범례 표시 다이얼로그 구현
- ✅ 메인 다이얼로그에 "범례 보기" 버튼 통합
- ✅ 활용 방안 문서화 완료

**사용자 혜택:**
- 레이어 내용을 시각적으로 쉽게 파악
- 다운로드 전 레이어 확인 가능
- 더 나은 사용자 경험 제공

**향후 계획:**
- 자동 스타일 적용 기능 추가
- 범례 캐싱 시스템 구현
- 대화형 범례 기능 개발

