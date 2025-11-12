# Quick Vworld - QGIS Plugin

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![QGIS](https://img.shields.io/badge/QGIS-3.22%2B-green.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)

한국 VWorld Open API를 통해 공간 데이터를 QGIS로 쉽게 다운로드할 수 있는 플러그인입니다.

## ✨ 주요 기능

### 🗺️ WFS 데이터 다운로드
- **캔버스 범위** 또는 **레이어 범위**로 데이터 다운로드
- 선택한 피처만 사용하여 범위 지정 가능
- 도시계획 관련 레이어 지원

### 📊 범례 표시 기능
- VWorld GetLegendGraphic API 통합
- 레이어 다운로드 전 범례 확인
- 시각적으로 레이어 내용 파악

### 🎯 지원 레이어
- **도시계획시설**: 공간시설 (lt_c_upisuq153)
- **용도지구**: 개발진흥지구, 경관지구, 고도지구
- **토지**: 연속지적도 (본번/부번)
- **경계**: 행정구역 (시도/시군구/읍면동/리)
- 향후 167종의 VWorld 레이어 확장 예정

## 🚀 설치 방법

### 방법 1: QGIS 플러그인 관리자 (추천)
1. QGIS 메뉴: `플러그인` > `플러그인 관리 및 설치`
2. "Quick Vworld" 검색
3. `설치` 클릭

### 방법 2: 수동 설치
1. 이 레포지토리 클론 또는 다운로드
2. QGIS 플러그인 디렉토리로 복사:
   - **Windows**: `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\QuickVworld`
   - **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/QuickVworld`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/QuickVworld`
3. QGIS 재시작 후 플러그인 활성화

## 📖 사용 방법

### 1. 기본 데이터 다운로드

1. **플러그인 실행**
   - QGIS 메뉴: `플러그인` > `Quick Vworld`
   
2. **범위 선택**
   - **캔버스 범위**: 현재 화면에 보이는 영역
   - **레이어 범위**: 기존 레이어의 범위 사용
   
3. **레이어 타입 선택**
   - 드롭다운에서 원하는 레이어 선택
   
4. **다운로드**
   - `다운로드` 버튼 클릭

### 2. 범례 확인

1. 레이어 타입 선택
2. `범례 보기` 버튼 클릭
3. 범례 다이얼로그에서 레이어 정보 확인

## 🔧 API 설정

### VWorld API 키
플러그인에는 기본 API 키가 포함되어 있습니다. 개인 API 키를 사용하려면:

1. [VWorld 개발자센터](https://www.vworld.kr/dev/v4dv_apiJoinPage.do)에서 API 키 발급
2. `definitions/layers.py`에서 `DEFAULT_API_KEY` 수정

```python
DEFAULT_API_KEY = "YOUR_API_KEY_HERE"
```

## 🏗️ 개발

### 프로젝트 구조

```
QuickVworld/
├── core/
│   ├── api/
│   │   ├── downloader.py          # HTTP 다운로더
│   │   ├── vworld_client.py       # WFS API 클라이언트
│   │   └── legend_client.py       # 범례 API 클라이언트
│   ├── processor.py               # 데이터 처리
│   └── utilities.py               # 유틸리티
├── ui/
│   ├── main_dialog.py             # 메인 다이얼로그
│   └── legend_dialog.py           # 범례 다이얼로그
├── definitions/
│   └── layers.py                  # 레이어 정의
├── test_legend_graphic.py         # 범례 API 테스트
└── quick_vworld.py                # 플러그인 엔트리포인트
```

### 개발 환경 설정

```bash
# 레포지토리 클론
git clone https://github.com/YOUR_USERNAME/qgis-quickvworld.git
cd qgis-quickvworld

# QGIS 플러그인 디렉토리에 심볼릭 링크 생성 (Linux/macOS)
ln -s $(pwd) ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/QuickVworld

# 테스트 (Python 환경 필요)
python test_legend_graphic.py
```

### 의존성

- **QGIS**: 3.22 이상
- **Python**: 3.7 이상
- **PyQt5**: QGIS에 포함
- **requests**: 테스트 스크립트용 (선택)

## 📚 문서

- **[빠른 요약](QUICK_SUMMARY_KO.md)**: 범례 API 통합 요약
- **[통합 가이드](LEGEND_INTEGRATION_SUMMARY.md)**: 상세 구현 가이드
- **[활용 방안](legends/LEGEND_USAGE_REPORT.md)**: 범례 활용 방법
- **[VWorld API 문서](VWORLD_API_DOCUMENT.md)**: VWorld API 레퍼런스
- **[개발 가이드](README_VWORLD_PLUGIN_DEV.md)**: 플러그인 개발 가이드

## 🤝 기여

기여를 환영합니다! 다음과 같은 방법으로 참여할 수 있습니다:

1. 이슈 제보
2. 기능 제안
3. Pull Request
4. 문서 개선

### Pull Request 가이드

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 변경 로그

### v1.0.0 (2025-11-12)

**새로운 기능:**
- ✨ VWorld WFS API 통합
- ✨ 캔버스/레이어 범위 선택
- ✨ 도시계획시설 레이어 다운로드
- ✨ GetLegendGraphic API 통합
- ✨ 범례 표시 다이얼로그

**문서:**
- 📚 API 문서 작성
- 📚 사용자 가이드 작성
- 📚 개발자 가이드 작성

## 🐛 알려진 이슈

- 일부 레이어는 범례를 제공하지 않을 수 있음
- 대용량 데이터 다운로드 시 시간이 걸릴 수 있음
- 네트워크 연결 필요 (오프라인 모드 미지원)

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🙏 감사의 말

- **VWorld**: 공간정보 오픈플랫폼 제공
- **QGIS**: 오픈소스 GIS 플랫폼
- **QuickOSM**: 플러그인 구조 참고

## 📞 연락처

- **이슈**: [GitHub Issues](https://github.com/YOUR_USERNAME/qgis-quickvworld/issues)
- **이메일**: quickvworld@example.com
- **홈페이지**: https://github.com/YOUR_USERNAME/qgis-quickvworld

## 🌟 Star History

도움이 되었다면 Star를 눌러주세요! ⭐

---

**Made with ❤️ for QGIS and VWorld users**
