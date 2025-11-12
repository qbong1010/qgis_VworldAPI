# Vworld Open API 레퍼런스

## 0. API 키 정보

**APIKEY**: `82E0F346-3308-3E16-AD90-3E36EB0A6895`
- 발급일: 2025-08-22
- 만료일: 2026-02-22
- 참고: 개발단계에서는 하드코딩해서 사용해도 상관 없음

## 1. API 문서 링크

### 1.1 WMS/WFS API 2.0 (연속주제도 등 요청)
https://www.vworld.kr/dev/v4dv_wmsguide2_s001.do

### 1.2 검색 API 2.0
https://www.vworld.kr/dev/v4dv_search2_s001.do

### 1.3 Geocoder API 2.0
- 주소 → 좌표 변환: https://www.vworld.kr/dev/v4dv_geocoderguide2_s001.do
- 좌표 → 주소 변환: https://www.vworld.kr/dev/v4dv_geocoderguide2_s002.do

### 1.4 국가중점API 레퍼런스
https://www.vworld.kr/dtna/dtna_apiSvcList_s001.do

---

## 2. WMS/WFS API 2.0 상세 가이드

### 2.1 소개

- **WMS (Web Map Service)**: 고품질의 공간정보 지도 이미지 서비스 제공
- **WFS (Web Feature Service)**: 공간정보 피처(벡터) 데이터 서비스 제공
- 인증된 키를 사용하여 요청 URL을 서버에 전송
- WMS 1.3.0 / WFS 1.1.0 서비스 지원

### 2.2 요청 URL

#### WMS 요청 URL
```
https://api.vworld.kr/req/wms?key=인증키&[WMS Param]
```

**도메인 추가 (HTTPS, Flex 등 웹뷰어가 아닌 경우):**
```
https://api.vworld.kr/req/wms?key=인증키&domain=인증받은도메인&[WMS Param]
```

#### WFS 요청 URL
```
https://api.vworld.kr/req/wfs?key=인증키&[WFS Param]
```

**도메인 추가 (HTTPS, Flex 등 웹뷰어가 아닌 경우):**
```
https://api.vworld.kr/req/wfs?key=인증키&domain=인증받은도메인&[WFS Param]
```

### 2.3 서비스 대상 (총 167종)

#### 주요 카테고리
- **경계**: 광역시도, 리, 시군구, 읍면동 (4종)
- **관광**: 관광안내소, 전통시장현황 (2종)
- **교통**: 교통CCTV, 교통노드, 교통링크, 도로중심선 (4종)
- **국가지명**: 국가지명 (1종)
- **농업·농촌**: 농업진흥지역도, 영농여건불리농지도 (2종)
- **도시계획**: 개발행위허가제한지역, 도시계획시설 등 (12종)
- **문화재**: 국가유산보호도, 박물관미술관, 전통사찰보존 (3종)
- **사회복지**: 기타보호시설, 노인복지시설, 아동복지시설 등 (4종)
- **산업**: 주요상권, 창업보육센터 (2종)
- **산업단지**: 단지경계, 단지시설용지, 단지용도지역 등 (4종)
- **수자원**: 대권역, 중권역, 표준권역, 하천망 (4종)
- **용도지역지구**: 개발제한구역, 경관지구, 관리지역 등 (17종)
- **일반행정**: 도로명주소건물, 도로명주소도로, 건축물정보 (3종)
- **임업·산촌**: 산림입지도 (1종)
- **자연**: 단층, 배수등급, 수문지질단위 등 (14종)
- **정밀도로지도**: 과속방지턱, 노면표시, 신호등 등 (15종)
- **재난방재**: 산불위험예측지도, 소방서관할구역 등 (3종)
- **체육**: 국립자연공원, 등산로, 자전거보관소 등 (5종)
- **토지**: 사업지구경계도, 연속지적도, LX맵 (3종)
- **학교**: 고등학교학교군, 교육행정구역 등 (4종)
- **항공·공항**: 관제권, 비행금지구역, 훈련구역 등 (21종)
- **해양·수산**: 관리연안해역, 해양보호구역 등 (13종)
- **환경보호**: 골프장현황도, 상수원보호, 수질측정망 등 (8종)

### 2.4 주요 레이어 목록

**⚠️ 주의: WMS명, WFS명, 스타일명은 소문자만 가능**

#### 경계 (Boundary)
| 한글명 | WMS명 | WFS명 | 스타일명 | 비고 |
|--------|-------|-------|----------|------|
| 광역시도 | lt_c_adsido | lt_c_adsido_info | lt_c_adsido / lt_c_adsido_3d | 2D/3D |
| 시군구 | lt_c_adsigg | lt_c_adsigg_info | lt_c_adsigg / lt_c_adsigg_3d | 2D/3D |
| 읍면동 | lt_c_ademd | lt_c_ademd_info | lt_c_ademd / lt_c_ademd_3d | 2D/3D |
| 리 | lt_c_adri | lt_c_adri_info | lt_c_adri / lt_c_adri_3d | 2D/3D |

#### 일반행정 (Administration)
| 한글명 | WMS명 | WFS명 | 스타일명 | 비고 |
|--------|-------|-------|----------|------|
| 건축물정보 | lt_c_bldginfo | lt_c_bldginfo | - | 2D/3D |
| 도로명주소건물 | lt_c_spbd | - | lt_c_spbd / lt_c_spbd_nl | 2D/3D |
| 도로명주소도로 | lt_l_sprd | - | lt_l_sprd / lt_l_sprd_l | 2D/3D |

#### 토지 (Land)
| 한글명 | WMS명 | WFS명 | 스타일명 | 비고 |
|--------|-------|-------|----------|------|
| 연속지적도 | lp_pa_cbnd_bubun, lp_pa_cbnd_bonbun | lp_pa_cbnd_bubun | lp_pa_cbnd_bubun, lp_pa_cbnd_bonbun / lp_pa_cbnd_bubun_line, lp_pa_cbnd_bonbun_line | 2D/3D |
| LX맵 | lt_c_landinfobasemap | lt_c_landinfobasemap | lt_c_landinfobasemap | 2D/3D |

#### 교통 (Transportation)
| 한글명 | WMS명 | WFS명 | 스타일명 | 비고 |
|--------|-------|-------|----------|------|
| 도로중심선 | lt_l_n3a0020000 | lt_l_n3a0020000 | lt_l_n3a0020000 | 2D/3D |
| 교통CCTV | lt_p_utiscctv | lt_p_utiscctv | lt_p_utiscctv / lt_p_utiscctv_3d | 2D/3D |

---

## 3. WMS 상세정보

### 3.1 요청 파라미터

| 파라미터 | 필수 | 설명 | 유효값 |
|----------|------|------|--------|
| **service** | O | 요청 서비스명 | WMS (기본값) |
| **version** | O | 요청 서비스 버전 | 1.3.0 (기본값) |
| **request** | M | 요청 서비스 오퍼레이션 | GetMap, GetCapabilities |
| **key** | M | 발급받은 API key | - |
| **format** | O | 응답결과 포맷 | image/png (기본값) |
| **exceptions** | O | 에러 응답결과 포맷 | text/xml (기본값) |
| **layers** | M | 지도레이어 목록 (쉼표 분리, 최대 4개) | 레이어 목록 참고 |
| **styles** | O | LAYERS와 1:1 관계의 스타일 목록 | 레이어 목록 참고 |
| **bbox** | M | Bounding box (xmin,ymin,xmax,ymax) | ⚠️ EPSG:4326 등의 경우 (ymin,xmin,ymax,xmax) |
| **width** | M | 지도의 픽셀 너비 | 숫자 |
| **height** | M | 지도의 픽셀 높이 | 숫자 |
| **transparent** | O | 지도 배경의 투명도 여부 | TRUE, FALSE (기본값) |
| **bgcolor** | O | 배경색 정의부 | 0xFFFFFF (기본값) |
| **crs** | O | 좌표계 (응답결과 및 bbox) | EPSG:4326 (기본값) |
| **domain** | O | API KEY 발급 시 입력한 URL | HTTPS/Flex 등에서 필요 |

**M**: 필수 (Mandatory), **O**: 선택 (Optional)

### 3.2 GetFeatureInfo 요청 파라미터

| 파라미터 | 필수 | 설명 | 유효값 |
|----------|------|------|--------|
| **request** | M | 요청 오퍼레이션 | GetFeatureInfo |
| **query_layers** | M | 지도레이어 목록 (쉼표 분리) | 레이어 목록 참고 |
| **info_format** | O | 응답결과 포맷 | text/plain (기본값), application/json, text/html 등 |
| **feature_count** | O | 출력되는 피처의 최대 개수 | 기본값: 1 |
| **i** | M | 지도상의 X좌표 (왼쪽이 0) | - |
| **j** | M | 지도상의 Y좌표 (상단이 0) | - |

#### info_format 유효값
- `text/plain` (기본값, TEXT)
- `application/vnd.ogc.gml` (GML 2)
- `application/vnd.ogc.gml/3.1.1` (GML 3)
- `text/html` (HTML)
- `application/json` (JSON)
- `text/javascript` (JSONP)

### 3.3 WMS 사용 예제

```
https://api.vworld.kr/req/wms?
SERVICE=WMS&
REQUEST=GetMap&
VERSION=1.3.0&
LAYERS=lp_pa_cbnd_bonbun,lp_pa_cbnd_bubun&
STYLES=lp_pa_cbnd_bonbun_line,lp_pa_cbnd_bubun_line&
CRS=EPSG:900913&
BBOX=14133818.022824,4520485.8511757,14134123.770937,4520791.5992888&
WIDTH=256&
HEIGHT=256&
FORMAT=image/png&
TRANSPARENT=false&
BGCOLOR=0xFFFFFF&
EXCEPTIONS=text/xml&
KEY=[YOUR_API_KEY]&
DOMAIN=[YOUR_DOMAIN]
```

### 3.4 OGC WMS Specification
https://www.ogc.org/standard/wms

---

## 4. WFS 상세정보

### 4.1 WFS 컬럼 정보
**다운로드**: https://www.vworld.kr/contents/브이월드_WFS_컬럼정보.xlsx

### 4.2 요청 파라미터

| 파라미터 | 필수 | 설명 | 유효값 |
|----------|------|------|--------|
| **service** | O | 요청 서비스명 | WFS (기본값) |
| **version** | O | 요청 서비스 버전 | 1.1.0 (기본값) |
| **request** | M | 요청 서비스 오퍼레이션 | GetFeature, GetCapabilities |
| **key** | M | 발급받은 API key | - |
| **output** | O | 응답결과 포맷 | text/xml; subtype=gml/2.1.2 (기본값), GML2, GML3, application/json, text/javascript |
| **format_options** | O | JSONP 콜백 함수 이름 지정 | 기본값: parseResponse<br>예: `format_options=callback:func_callback` |
| **exceptions** | O | 에러 응답결과 포맷 | text/xml (기본값) |
| **typename** | M | 지도레이어 목록 (쉼표 분리, 최대 4개) | 레이어 목록 참고 |
| **featureid** | O | 요청 FEATURE ID | - |
| **bbox** | O | Bounding box | EPSG:4326: (ymin,xmin,ymax,xmax)<br>그 외: (xmin,ymin,xmax,ymax) |
| **propertyname** | O | 속성 목록 (쉼표 분리) | - |
| **maxfeatures** | O | 출력 피처 최대 개수 (v1.0.0) | 기본값: 1000, 최소: 1, 최대: 1000 |
| **count** | O | 출력 피처 최대 개수 (v2.0.0) | 기본값: 1000, 최소: 1, 최대: 1000 |
| **startindex** | O | 출력 피처 시작지점 (v2.0.0) | 예: startindex=10이면 11번째부터 |
| **sortby** | O | 정렬 속성 지정 | PropertyName [A\|D]<br>A: 오름차순, D: 내림차순<br>예: `sortby=Field1 D,Field A`<br>⚠️ encodeURIComponent로 변환 후 요청 |
| **srsname** | O | 좌표계 (응답결과 및 bbox) | EPSG:900913 (기본값) |
| **domain** | O | API KEY 발급 시 입력한 URL | HTTPS/Flex 등에서 필요 |
| **filter** | O | WFS FILTER 1.1 | ⚠️ encodeURIComponent로 변환 후 요청 |

### 4.3 WFS 사용 예제

```
https://api.vworld.kr/req/wfs?
SERVICE=WFS&
REQUEST=GetFeature&
TYPENAME=lt_c_uq111&
BBOX=13987670,3912271,14359383,4642932&
PROPERTYNAME=mnum,sido_cd,sigungu_cd,dyear,dnum,ucode,bon_bun,bu_bun,uname,sido_name,sigg_name,ag_geom&
VERSION=1.1.0&
MAXFEATURES=40&
SRSNAME=EPSG:900913&
OUTPUT=GML2&
EXCEPTIONS=text/xml&
KEY=[YOUR_API_KEY]&
DOMAIN=[YOUR_DOMAIN]&
FILTER=[WFS_FILTER]
```

### 4.4 OGC WFS Specification
https://www.ogc.org/standard/wfs

### 4.5 WFS FILTER 1.1 Specification
https://www.ogc.org/standard/filter

### 4.6 WFS FILTER 예제

#### PropertyIsEqualTo (같음)
```xml
<ogc:Filter>
    <ogc:PropertyIsEqualTo matchCase="true">
        <ogc:PropertyName>dyear</ogc:PropertyName>
        <ogc:Literal>2005</ogc:Literal>
    </ogc:PropertyIsEqualTo>
</ogc:Filter>
```

#### PropertyIsNotEqualTo (같지 않음)
```xml
<ogc:Filter>
    <ogc:PropertyIsNotEqualTo matchCase="true">
        <ogc:PropertyName>dyear</ogc:PropertyName>
        <ogc:Literal>2005</ogc:Literal>
    </ogc:PropertyIsNotEqualTo>
</ogc:Filter>
```

#### PropertyIsLessThan (작음)
```xml
<ogc:Filter>
    <ogc:PropertyIsLessThan matchCase="false">
        <ogc:PropertyName>dyear</ogc:PropertyName>
        <ogc:Literal>2005</ogc:Literal>
    </ogc:PropertyIsLessThan>
</ogc:Filter>
```

#### PropertyIsGreaterThan (큼)
```xml
<ogc:Filter>
    <ogc:PropertyIsGreaterThan matchCase="true">
        <ogc:PropertyName>dyear</ogc:PropertyName>
        <ogc:Literal>2005</ogc:Literal>
    </ogc:PropertyIsGreaterThan>
</ogc:Filter>
```

#### PropertyIsLike (LIKE 검색)
```xml
<ogc:Filter>
    <ogc:PropertyIsLike wildCard="*" singleChar="_" escapeChar="\">
        <ogc:PropertyName>sido_name</ogc:PropertyName>
        <ogc:Literal>서울*</ogc:Literal>
    </ogc:PropertyIsLike>
</ogc:Filter>
```

#### PropertyIsNull (NULL 체크)
```xml
<ogc:Filter>
    <ogc:PropertyIsNull>
        <ogc:PropertyName>remark</ogc:PropertyName>
    </ogc:PropertyIsNull>
</ogc:Filter>
```

#### PropertyIsBetween (범위)
```xml
<ogc:Filter>
    <ogc:PropertyIsBetween>
        <ogc:PropertyName>dyear</ogc:PropertyName>
        <ogc:LowerBoundary>
            <ogc:Literal>2000</ogc:Literal>
        </ogc:LowerBoundary>
        <ogc:UpperBoundary>
            <ogc:Literal>2005</ogc:Literal>
        </ogc:UpperBoundary>
    </ogc:PropertyIsBetween>
</ogc:Filter>
```

#### Intersects (공간 교차)
```xml
<ogc:Filter>
    <ogc:Intersects>
        <ogc:PropertyName>ag_geom</ogc:PropertyName>
        <Point srsName="EPSG:900913">
            <pos>14132768.287088 4494181.0225382</pos>
        </Point>
    </ogc:Intersects>
</ogc:Filter>
```

#### BBOX (바운딩 박스)
```xml
<ogc:Filter>
    <ogc:BBOX>
        <ogc:PropertyName>ag_geom</ogc:PropertyName>
        <Envelope srsDimension="2" srsName="EPSG:900913">
            <lowerCorner>14132768.287088 4494181.0225382</lowerCorner>
            <upperCorner>14132777.841717 4494190.5771668</upperCorner>
        </Envelope>
    </ogc:BBOX>
</ogc:Filter>
```

#### AND (논리곱)
```xml
<ogc:Filter>
    <ogc:And>
        <ogc:PropertyIsEqualTo>
            <ogc:PropertyName>sigg_name</ogc:PropertyName>
            <ogc:Literal>안양시동안구</ogc:Literal>
        </ogc:PropertyIsEqualTo>
        <ogc:PropertyIsLessThan>
            <ogc:PropertyName>ucode</ogc:PropertyName>
            <ogc:Literal>UQA112</ogc:Literal>
        </ogc:PropertyIsLessThan>
    </ogc:And>
</ogc:Filter>
```

#### OR (논리합)
```xml
<ogc:Filter>
    <ogc:Or>
        <ogc:PropertyIsGreaterThan>
            <ogc:PropertyName>ucode</ogc:PropertyName>
            <ogc:Literal>UQA113</ogc:Literal>
        </ogc:PropertyIsGreaterThan>
        <ogc:PropertyIsLessThan>
            <ogc:PropertyName>sigungu_cd</ogc:PropertyName>
            <ogc:Literal>174</ogc:Literal>
        </ogc:PropertyIsLessThan>
    </ogc:Or>
</ogc:Filter>
```

#### NOT (부정)
```xml
<ogc:Filter>
    <ogc:Not>
        <ogc:PropertyIsEqualTo>
            <ogc:PropertyName>sigg_name</ogc:PropertyName>
            <ogc:Literal>종로구</ogc:Literal>
        </ogc:PropertyIsEqualTo>
    </ogc:Not>
</ogc:Filter>
```

#### Spatial + Attribute (공간 + 속성 조합)
```xml
<ogc:Filter>
    <ogc:And>
        <ogc:PropertyIsLessThan>
            <ogc:PropertyName>sigungu_cd</ogc:PropertyName>
            <ogc:Literal>174</ogc:Literal>
        </ogc:PropertyIsLessThan>
        <ogc:Intersects>
            <ogc:PropertyName>ag_geom</ogc:PropertyName>
            <Point srsName="EPSG:900913">
                <pos>14132768.287088 4494181.0225382</pos>
            </Point>
        </ogc:Intersects>
    </ogc:And>
</ogc:Filter>
```

---

## 5. 공통 정보

### 5.1 지원 좌표계

| 좌표계 | EPSG 코드 |
|--------|-----------|
| WGS84 경위도 | EPSG:4326 |
| GRS80 경위도 | EPSG:4019 |
| Google Mercator | EPSG:3857, EPSG:900913 |
| 서부원점(GRS80) | EPSG:5180(50만), EPSG:5185 |
| 중부원점(GRS80) | EPSG:5181(50만), EPSG:5186 |
| 제주원점(GRS80, 55만) | EPSG:5182 |
| 동부원점(GRS80) | EPSG:5183(50만), EPSG:5187 |
| 동해(울릉)원점(GRS80) | EPSG:5184(50만), EPSG:5188 |
| UTM-K(GRS80) | EPSG:5179 |

### 5.2 오류 응답 구조

#### 응답 필드
| 항목명 | 타입 | 설명 |
|--------|------|------|
| **service** | 문자 | 요청 서비스 정보 Root |
| ㄴ name | 문자 | 요청 서비스명 |
| ㄴ version | 숫자 | 요청 서비스 버전 |
| ㄴ operation | 문자 | 요청 서비스 오퍼레이션 이름 |
| ㄴ time | 숫자 | 응답결과 생성 시간 |
| **status** | 문자 | 처리 결과 상태 (OK, NOT_FOUND, ERROR) |
| **error** | 문자 | 에러 정보 Root |
| ㄴ level | 숫자 | 에러 레벨 |
| ㄴ code | 문자 | 에러 코드 |
| ㄴ text | 문자 | 에러 메시지 |

### 5.3 오류 코드 및 메시지

| 코드 | 레벨 | 메시지 | 비고 |
|------|------|--------|------|
| **PARAM_REQUIRED** | 1 | 필수 파라미터인 `<파라미터명>`가 없어서 요청을 처리할수 없습니다. | - |
| **INVALID_TYPE** | 1 | `<파라미터명>` 파라미터 타입이 유효하지 않습니다. | 유효한 타입과 입력값 표시 |
| **INVALID_RANGE** | 1 | `<파라미터명>` 파라미터의 값이 유효한 범위를 넘었습니다. | 유효 범위와 입력값 표시 |
| **INVALID_KEY** | 2 | 등록되지 않은 인증키입니다. | - |
| **INCORRECT_KEY** | 2 | 인증키 정보가 올바르지 않습니다. (예: 도메인 불일치) | - |
| **UNAVAILABLE_KEY** | 2 | 임시로 인증키를 사용할 수 없는 상태입니다. | - |
| **OVER_REQUEST_LIMIT** | 2 | 서비스 사용량이 일일 제한량을 초과하여 더 이상 서비스를 사용할 수 없습니다. | - |
| **SYSTEM_ERROR** | 3 | 시스템 에러가 발생하였습니다. | - |
| **UNKNOWN_ERROR** | 3 | 알 수 없는 에러가 발생하였습니다. | - |

---

## 6. 검색 API 2.0 상세정보

### 6.1 소개

검색엔진 기반 주소(구 주소, 도로명주소)와 국가관심지점(명칭/장소) 검색 API입니다.

### 6.2 요청 URL

```
https://api.vworld.kr/req/search?key=인증키&[검색API 요청파라미터]
```

### 6.3 요청 파라미터

| 파라미터 | 필수 | 설명 | 유효값 |
|----------|------|------|--------|
| **service** | O | 요청 서비스명 | search (기본값) |
| **version** | O | 요청 서비스 버전 | 2.0 (기본값) |
| **request** | M | 요청 서비스 오퍼레이션 | search |
| **key** | M | 발급받은 API key | - |
| **format** | O | 응답결과 포맷 | json (기본값), xml |
| **errorFormat** | O | 에러 응답결과 포맷 (생략 시 format 값 사용) | json, xml |
| **size** | O | 한 페이지에 출력될 응답결과 건수 | 기본값: 10, 최소: 1, 최대: 1000 |
| **page** | O | 응답결과 페이지 번호 | 기본값: 1 |
| **query** | M | 검색 키워드 | 예: 장소(공간정보산업진흥원), 주소(판교로 344), 행정구역(삼평동), 도로명(판교로) |
| **type** | M | 검색 대상 | PLACE (장소), ADDRESS (주소), DISTRICT (행정구역), ROAD (도로명) |
| **category** | 조건부 | 검색 대상 하위 유형<br>⚠️ address, district는 필수 | 장소: 장소분류코드<br>주소: ROAD, PARCEL<br>행정구역: L1(시도), L2(시군구), L3(일반구), L4(읍면동) |
| **bbox** | O | 검색 영역 (minx,miny,maxx,maxy) | - |
| **crs** | O | 응답결과 좌표계 (응답, bbox에 적용) | EPSG:4326 (기본값) |
| **callback** | O | format=json일 경우 callback 함수 지원 | - |

**M**: 필수, **O**: 선택

**장소분류코드 다운로드**: https://www.vworld.kr/contents/브이월드_장소분류코드_20240712.xlsx

### 6.4 사용 예제

#### PLACE (장소) 검색
```
https://api.vworld.kr/req/search?
service=search&
request=search&
version=2.0&
crs=EPSG:900913&
bbox=14140071.146077,4494339.6527027,14160071.146077,4496339.6527027&
size=10&
page=1&
query=공간정보산업진흥원&
type=place&
format=json&
errorformat=json&
key=[YOUR_API_KEY]
```

#### ADDRESS (주소) 검색
```
https://api.vworld.kr/req/search?
service=search&
request=search&
version=2.0&
crs=EPSG:900913&
bbox=14140071.146077,4494339.6527027,14160071.146077,4496339.6527027&
size=10&
page=1&
query=성남시 분당구 판교로 242&
type=address&
category=road&
format=json&
errorformat=json&
key=[YOUR_API_KEY]
```

#### DISTRICT (행정구역) 검색
```
https://api.vworld.kr/req/search?
service=search&
request=search&
version=2.0&
crs=EPSG:900913&
bbox=14140071.146077,4494339.6527027,14160071.146077,4496339.6527027&
size=10&
page=1&
query=삼평동&
type=district&
category=L4&
format=json&
errorformat=json&
key=[YOUR_API_KEY]
```

#### ROAD (도로명) 검색
```
https://api.vworld.kr/req/search?
service=search&
request=search&
version=2.0&
crs=EPSG:900913&
bbox=14140071.146077,4494339.6527027,14160071.146077,4496339.6527027&
size=10&
page=1&
query=판교로&
type=road&
format=json&
errorformat=json&
key=[YOUR_API_KEY]
```

### 6.5 응답 결과 구조

#### 공통 응답 구조
| 항목명 | 타입 | 설명 |
|--------|------|------|
| **service** | 문자 | 요청 서비스 정보 Root |
| ㄴ name | 문자 | 요청 서비스명 |
| ㄴ version | 숫자 | 요청 서비스 버전 |
| ㄴ operation | 문자 | 요청 서비스 오퍼레이션 이름 |
| ㄴ time | 숫자 | 응답결과 생성 시간 (단위: ms) |
| **status** | 문자 | 처리 결과 상태 (OK, NOT_FOUND, ERROR) |
| **record** | - | 응답결과 건수 정보 Root |
| ㄴ total | 숫자 | 전체 결과 건수 |
| ㄴ current | 숫자 | 현재 반환된 결과 건수 |
| **page** | - | 응답결과 페이지 정보 Root |
| ㄴ total | 숫자 | 전체 페이지 수 |
| ㄴ current | 숫자 | 현재 페이지 번호 |
| ㄴ size | 숫자 | 페이지 당 반환되는 결과 건수 |
| **result** | - | 응답결과 Root |
| ㄴ crs | 문자 | 응답결과 좌표계 |
| ㄴ type | 문자 | 요청검색 대상 |
| ㄴ **items** | - | 응답결과 목록 Root |

#### 장소(PLACE) 응답 결과
**result.items.item 하위 필드**:

| 필드명 | 타입 | 설명 |
|--------|------|------|
| **id** | 문자 | ID |
| **title** | 문자 | 이름 (업체, 기관명) |
| **category** | 문자 | 장소 분류 유형 |
| **address** | - | 주소 Root |
| ㄴ road | 문자 | 도로 주소 |
| ㄴ parcel | 문자 | 지번 주소 |
| **point** | - | 주소 좌표 Root |
| ㄴ x | 숫자 | x좌표 |
| ㄴ y | 숫자 | y좌표 |

#### 주소(ADDRESS) 응답 결과
**result.items.item 하위 필드**:

| 필드명 | 타입 | 설명 |
|--------|------|------|
| **id** | 문자 | 주소의 ID (PNU 지번 코드) |
| **address** | - | 주소 Root |
| ㄴ zipcode | 숫자 | 우편번호 |
| ㄴ category | 문자 | 요청한 주소의 유형 |
| ㄴ road | 문자 | 도로 주소 |
| ㄴ parcel | 문자 | 지번 주소 |
| ㄴ bldnm | 문자 | 건물명 (category=road일 때만) |
| ㄴ bldnmdc | 문자 | 건물명 상세정보 (category=road일 때만) |
| **point** | - | 주소 좌표 Root |
| ㄴ x | 숫자 | x좌표 |
| ㄴ y | 숫자 | y좌표 |

#### 행정구역(DISTRICT) 응답 결과
**result.items.item 하위 필드**:

| 필드명 | 타입 | 설명 |
|--------|------|------|
| **id** | 문자 | 주소의 ID (행정구역코드) |
| **title** | 문자 | 행정구역명 |
| **geometry** | 문자 | 행정구역의 도로구간정보 파일 호출 (gml, geojson 포맷) |
| **point** | - | 주소 좌표 Root |
| ㄴ x | 숫자 | x좌표 |
| ㄴ y | 숫자 | y좌표 |

#### 도로명(ROAD) 응답 결과
**result.items.item 하위 필드**:

| 필드명 | 타입 | 설명 |
|--------|------|------|
| **id** | 문자 | 주소의 ID (도로명코드) |
| **title** | 문자 | 도로명 |
| **district** | 문자 | 도로를 포함하는 구역 |
| **geometry** | 문자 | 도로명의 도로구간정보 파일 호출 (gml, geojson 포맷) |

---

## 7. Geocoder API 2.0 - 주소를 좌표로 변환

### 7.1 소개

- 주소를 좌표로 변환하는 지오코딩 서비스를 제공합니다.
- 일일 지오코딩 요청건수는 최대 **40,000건**입니다.
- ⚠️ **API 요청은 실시간으로 사용해야 하며 별도의 저장장치나 데이터베이스에 저장할 수 없습니다.**

### 7.2 요청 URL

```
https://api.vworld.kr/req/address?service=address&request=getCoord&key=인증키&[요청파라미터]
```

### 7.3 요청 파라미터

| 파라미터 | 필수 | 설명 | 유효값 |
|----------|------|------|--------|
| **service** | O | 요청 서비스명 | address (기본값) |
| **version** | O | 요청 서비스 버전 | 2.0 (기본값) |
| **request** | M | 요청 서비스 오퍼레이션 | GetCoord |
| **key** | M | 발급받은 API key | - |
| **format** | O | 응답결과 포맷 | json (기본값), xml |
| **errorFormat** | O | 에러 응답결과 포맷 (생략 시 format 값 사용) | json, xml |
| **type** | M | 검색 주소 유형 | PARCEL (지번주소), ROAD (도로명주소) |
| **address** | M | 검색 키워드 | 지번: 법정동+지번 (예: 관양동 1588-8)<br>도로명: 시군구+도로명+건물번호 (예: 안양시 동안구 부림로169번길 22) |
| **refine** | O | 주소 정제 여부 (정제된 주소는 false로 빠른 처리) | true (기본값), false |
| **simple** | O | 응답결과 간략 출력 여부 | true, false (기본값) |
| **crs** | O | 응답결과 좌표계 | EPSG:4326 (기본값) |
| **callback** | O | format=json일 경우 callback 함수 지원 | - |

**M**: 필수, **O**: 선택

### 7.4 사용 예제

#### 기본 요청 (URL)
```
https://api.vworld.kr/req/address?
service=address&
request=getcoord&
version=2.0&
crs=epsg:4326&
address=%ED%9A%A8%EB%A0%B9%EB%A1%9C72%EA%B8%B8%2060&
refine=true&
simple=false&
format=xml&
type=road&
key=[YOUR_API_KEY]
```

#### Java 코드
```java
/* Java 코드 사용예제 */
String apikey = "[인증키]";
String searchType = "parcel";
String searchAddr = "삼평동 624";
String epsg = "epsg:4326";

StringBuilder sb = new StringBuilder("https://api.vworld.kr/req/address");
sb.append("?service=address");
sb.append("&request=getCoord");
sb.append("&format=json");
sb.append("&crs=" + epsg);
sb.append("&key=" + apikey);
sb.append("&type=" + searchType);
sb.append("&address=" + URLEncoder.encode(searchAddr, StandardCharsets.UTF_8));

try {
    URL url = new URL(sb.toString());
    BufferedReader reader = new BufferedReader(
        new InputStreamReader(url.openStream(), StandardCharsets.UTF_8)
    );
    
    JSONParser jspa = new JSONParser();
    JSONObject jsob = (JSONObject) jspa.parse(reader);
    JSONObject jsrs = (JSONObject) jsob.get("response");
    JSONObject jsResult = (JSONObject) jsrs.get("result");
    JSONObject jspoint = (JSONObject) jsResult.get("point");
    
    System.out.println(jspoint.get("x"));
    System.out.println(jspoint.get("y"));
} catch (IOException | ParseException e) {
    throw new RuntimeException(e);
}
```

#### Python 코드
```python
# Python 코드 사용예제
import requests

apiurl = "https://api.vworld.kr/req/address?"
params = {
    "service": "address",
    "request": "getcoord",
    "crs": "epsg:4326",
    "address": "판교로 242",
    "format": "json",
    "type": "road",
    "key": "[인증키]"
}

response = requests.get(apiurl, params=params)
if response.status_code == 200:
    print(response.json())
```

#### JavaScript (AJAX) 코드
```javascript
/* JS(AJAX) 코드 사용예제 */
$.ajax({
    url: "https://api.vworld.kr/req/address?",
    type: "GET",
    dataType: "jsonp",
    data: {
        service: "address",
        request: "GetCoord",
        version: "2.0",
        crs: "EPSG:4326",
        type: "ROAD",
        address: "서울특별시 강남구 봉은사로 524",
        format: "json",
        errorformat: "json",
        key: "[인증키]"
    },
    success: function (result) {
        console.log(result);
    }
});
```

#### R 코드
```r
# R 코드 사용예제
library(httr)
library(RCurl)

url <- "https://api.vworld.kr/req/address"
params <- list(
    service = "address",
    request = "getcoord",
    version = "2.0",
    address = "효령로72길",
    refine = "true",
    simple = "false",
    format = "json",
    type = "road",
    key = "[인증키]"
)

full_url <- paste0(
    url, "?service=", params$service,
    "&request=", params$request,
    "&version=", params$version,
    "&address=", curlEscape(params$address),
    "&refine=", params$refine,
    "&simple=", params$simple,
    "&format=", params$format,
    "&type=", params$type,
    "&key=", params$key
)

response <- GET(full_url)
content <- content(response, "text")
print(content)
```

### 7.5 응답 결과 구조

#### 응답 필드
| 항목명 | 타입 | 설명 |
|--------|------|------|
| **service** | - | 요청 서비스 정보 Root |
| ㄴ name | 문자 | 요청 서비스명 |
| ㄴ version | 숫자 | 요청 서비스 버전 |
| ㄴ operation | 문자 | 요청 서비스 오퍼레이션 이름 |
| ㄴ time | 숫자 | 응답결과 생성 시간 |
| **status** | 문자 | 처리 결과 상태 (OK, NOT_FOUND, ERROR) |
| **input** | - | 입력 주소 정보 Root (simple=true일 때 생략) |
| ㄴ type | 문자 | 입력 주소 유형 (ROAD, PARCEL) |
| ㄴ address | 문자 | 입력 주소 |
| **refined** | - | 정제 주소 정보 Root (refine=false 또는 simple=true일 때 생략) |
| ㄴ text | 문자 | 전체 주소 텍스트 |
| ㄴ **structure** | - | 구조화된 주소 Root |
| ㄴ ㄴ level0 | 문자 | 국가 |
| ㄴ ㄴ level1 | 문자 | 시·도 |
| ㄴ ㄴ level2 | 문자 | 시·군·구 |
| ㄴ ㄴ level3 | 문자 | (일반구)구 |
| ㄴ ㄴ level4L | 문자 | (도로)도로명, (지번)법정읍·면·동명 |
| ㄴ ㄴ level4A | 문자 | (도로)행정읍·면·동명, (지번)지원안함 |
| ㄴ ㄴ level4AC | 문자 | (도로)행정읍·면·동코드, (지번)지원안함 |
| ㄴ ㄴ level5 | 문자 | (도로)길, (지번)번지 |
| ㄴ ㄴ detail | 문자 | 상세주소 |
| **result** | - | 응답결과 Root |
| ㄴ crs | 문자 | 응답결과 좌표계 |
| ㄴ **point** | - | 주소 좌표 Root |
| ㄴ ㄴ x | 숫자 | x좌표 |
| ㄴ ㄴ y | 숫자 | y좌표 |

#### 응답 예제 (JSON)
```json
{
  "response": {
    "service": {
      "name": "address",
      "version": "2.0",
      "operation": "getcoord",
      "time": "123(ms)"
    },
    "status": "OK",
    "input": {
      "type": "ROAD",
      "address": "판교로 242"
    },
    "refined": {
      "text": "경기도 성남시 분당구 삼평동 판교로 242",
      "structure": {
        "level0": "대한민국",
        "level1": "경기도",
        "level2": "성남시 분당구",
        "level4L": "판교로",
        "level4A": "삼평동",
        "level5": "242"
      }
    },
    "result": {
      "crs": "EPSG:4326",
      "point": {
        "x": "127.111111",
        "y": "37.411111"
      }
    }
  }
}
```

---

## 8. Geocoder API 2.0 - 좌표를 주소로 변환 (역방향 지오코딩)

### 8.1 소개

- 좌표를 주소로 변환하는 역방향 지오코딩 서비스를 제공합니다.
- 일일 지오코딩 요청건수는 **무제한**으로 제공됩니다.
- ⚠️ **API 요청은 실시간으로 사용해야 하며 별도의 저장장치나 데이터베이스에 저장할 수 없습니다.**

### 8.2 요청 URL

```
https://api.vworld.kr/req/address?service=address&request=getAddress&key=인증키&[요청파라미터]
```

### 8.3 요청 파라미터

| 파라미터 | 필수 | 설명 | 유효값 |
|----------|------|------|--------|
| **service** | O | 요청 서비스명 | address (기본값) |
| **version** | O | 요청 서비스 버전 | 2.0 (기본값) |
| **request** | M | 요청 서비스 오퍼레이션 | GetAddress |
| **key** | M | 발급받은 API key | - |
| **format** | O | 응답결과 포맷 | json (기본값), xml |
| **errorFormat** | O | 에러 응답결과 포맷 (생략 시 format 값 사용) | json, xml |
| **point** | M | 주소를 찾을 좌표 | 포맷: x,y (예: 127.101313354,37.402352535) |
| **crs** | O | 응답결과 좌표계 | EPSG:4326 (기본값) |
| **type** | O | 검색 주소 유형 | PARCEL (지번), ROAD (도로명), BOTH (둘다, 기본값) |
| **zipcode** | O | 우편번호 반환 여부 | true (기본값), false |
| **simple** | O | 응답결과 간략 출력 여부 | true, false (기본값) |
| **callback** | O | format=json일 경우 callback 함수 지원 | - |

**M**: 필수, **O**: 선택

### 8.4 사용 예제

#### 기본 요청 (URL)
```
https://api.vworld.kr/req/address?
service=address&
request=getAddress&
version=2.0&
crs=epsg:4326&
point=126.978275264,37.566642192&
format=xml&
type=both&
zipcode=true&
simple=false&
key=[YOUR_API_KEY]
```

#### Java 코드
```java
/* Java 코드 사용예제 */
String apikey = "[인증키]";
String searchType = "road";
String searchPoint = "127.101313354,37.402352535";
String epsg = "epsg:4326";

StringBuilder sb = new StringBuilder("https://api.vworld.kr/req/address");
sb.append("?service=address");
sb.append("&request=getaddress");
sb.append("&format=json");
sb.append("&crs=" + epsg);
sb.append("&key=" + apikey);
sb.append("&type=" + searchType);
sb.append("&point=" + searchPoint);

try {
    JSONParser jspa = new JSONParser();
    JSONObject jsob = (JSONObject) jspa.parse(
        new BufferedReader(
            new InputStreamReader(
                new URL(sb.toString()).openStream(), 
                StandardCharsets.UTF_8
            )
        )
    );
    JSONObject jsrs = (JSONObject) jsob.get("response");
    JSONArray jsonArray = (JSONArray) jsrs.get("result");
    JSONObject jsonfor = new JSONObject();
    
    for (int i = 0; i < jsonArray.size(); i++) {
        jsonfor = (JSONObject) jsonArray.get(i);
        System.out.println(jsonfor.get("text"));
    }
} catch (IOException | ParseException e) {
    throw new RuntimeException(e);
}
```

#### Python 코드
```python
# Python 코드 사용예제
import requests

apiurl = "https://api.vworld.kr/req/address?"
params = {
    "service": "address",
    "request": "getaddress",
    "crs": "epsg:4326",
    "point": "127.101313354,37.402352535",
    "format": "json",
    "type": "road",
    "key": "[인증키]"
}

response = requests.get(apiurl, params=params)
if response.status_code == 200:
    print(response.json())
```

#### JavaScript (AJAX) 코드
```javascript
/* JS(AJAX) 코드 사용예제 */
$.ajax({
    url: "https://api.vworld.kr/req/address?",
    type: "GET",
    dataType: "jsonp",
    data: {
        service: "address",
        request: "getaddress",
        version: "2.0",
        crs: "EPSG:4326",
        type: "ROAD",
        point: "127.101313354,37.402352535",
        format: "json",
        errorformat: "json",
        key: "[인증키]"
    },
    success: function (result) {
        console.log(result);
    }
});
```

#### R 코드
```r
# R 코드 사용예제
library(httr)
library(RCurl)

url <- "https://api.vworld.kr/req/address"
params <- list(
    service = "address",
    request = "getAddress",
    version = "2.0",
    point = "127.025967892,37.487352931",
    simple = "false",
    format = "json",
    type = "both",
    key = "[인증키]"
)

full_url <- paste0(
    url, "?service=", params$service,
    "&request=", params$request,
    "&version=", params$version,
    "&point=", params$point,
    "&simple=", params$simple,
    "&format=", params$format,
    "&type=", params$type,
    "&key=", params$key
)

response <- GET(full_url)
content <- content(response, "text")
print(content)
```

### 8.5 응답 결과 구조

#### 응답 필드
| 항목명 | 타입 | 설명 |
|--------|------|------|
| **service** | - | 요청 서비스 정보 Root |
| ㄴ name | 문자 | 요청 서비스명 |
| ㄴ version | 숫자 | 요청 서비스 버전 |
| ㄴ operation | 문자 | 요청 서비스 오퍼레이션 이름 |
| ㄴ time | 숫자 | 응답결과 생성 시간 |
| **status** | 문자 | 처리 결과 상태 (OK, NOT_FOUND, ERROR) |
| **input** | - | 입력 정보 Root (simple=true일 때 생략) |
| ㄴ **point** | - | 주소 좌표 Root |
| ㄴ ㄴ x | 숫자 | x좌표 |
| ㄴ ㄴ y | 숫자 | y좌표 |
| ㄴ crs | 문자 | 입력에 적용되는 좌표계 |
| ㄴ type | 문자 | 요청한 주소 유형 (ROAD, PARCEL, BOTH) |
| **result** | - | 응답결과 Root (배열) |
| ㄴ **item** | - | 출력 주소 정보 Root (여러 개 가능) |
| ㄴ ㄴ zipcode | 숫자 | 우편번호 (zipcode=false일 때 생략) |
| ㄴ ㄴ type | 문자 | 주소 유형 (ROAD, PARCEL) - simple=true일 때 생략 |
| ㄴ ㄴ text | 문자 | 전체 주소 텍스트 |
| ㄴ ㄴ **structure** | - | 구조화된 주소 Root |
| ㄴ ㄴ ㄴ level0 | 문자 | 국가 |
| ㄴ ㄴ ㄴ level1 | 문자 | 시·도 |
| ㄴ ㄴ ㄴ level2 | 문자 | 시·군·구 |
| ㄴ ㄴ ㄴ level3 | 문자 | (일반구)구 |
| ㄴ ㄴ ㄴ level4L | 문자 | (도로)도로명, (지번)법정읍·면·동명 |
| ㄴ ㄴ ㄴ level4LC | 문자 | (도로)도로코드, (지번)법정읍·면·동코드 |
| ㄴ ㄴ ㄴ level4A | 문자 | (도로)행정읍·면·동명, (지번)지원안함 |
| ㄴ ㄴ ㄴ level4AC | 문자 | (도로)행정읍·면·동코드, (지번)지원안함 |
| ㄴ ㄴ ㄴ level5 | 문자 | (도로)길, (지번)번지 |
| ㄴ ㄴ ㄴ detail | 문자 | 상세주소 |

#### 응답 예제 (JSON, type=both)
```json
{
  "response": {
    "service": {
      "name": "address",
      "version": "2.0",
      "operation": "getaddress",
      "time": "85(ms)"
    },
    "status": "OK",
    "input": {
      "point": {
        "x": "127.101313354",
        "y": "37.402352535"
      },
      "crs": "EPSG:4326",
      "type": "BOTH"
    },
    "result": [
      {
        "zipcode": "13487",
        "type": "ROAD",
        "text": "경기도 성남시 분당구 삼평동 판교로 242",
        "structure": {
          "level0": "대한민국",
          "level1": "경기도",
          "level2": "성남시 분당구",
          "level4L": "판교로",
          "level4LC": "4113053",
          "level4A": "삼평동",
          "level4AC": "11350",
          "level5": "242"
        }
      },
      {
        "zipcode": "13487",
        "type": "PARCEL",
        "text": "경기도 성남시 분당구 삼평동 680",
        "structure": {
          "level0": "대한민국",
          "level1": "경기도",
          "level2": "성남시 분당구",
          "level4L": "삼평동",
          "level4LC": "1135010600",
          "level5": "680"
        }
      }
    ]
  }
}
```

**⚠️ 주의**: type=both인 경우 result는 배열로 반환되며, 도로명 주소와 지번 주소가 각각 item으로 포함됩니다.

---

## 9. API 사용량 및 제약사항 요약

### 9.1 일일 요청 제한

| API | 일일 제한 | 비고 |
|-----|----------|------|
| WMS/WFS API | API 키별 상이 | 인증키 발급 시 확인 |
| 검색 API | API 키별 상이 | 인증키 발급 시 확인 |
| Geocoder - 주소→좌표 | **40,000건** | 제한 있음 |
| Geocoder - 좌표→주소 | **무제한** | 제한 없음 |

### 9.2 공통 제약사항

- ⚠️ **실시간 사용만 가능**: API 응답을 별도 저장장치나 데이터베이스에 저장 불가
- HTTPS, Flex 등에서 사용 시 **domain 파라미터 필수**
- WMS/WFS 레이어명, 스타일명은 **소문자만 가능**
- WFS maxfeatures/count 최대값: **1,000**

### 9.3 좌표계 변환 주의사항

**BBOX 파라미터 순서**:
- 일반 좌표계: `(xmin, ymin, xmax, ymax)`
- EPSG:4326, 5185~5188: `(ymin, xmin, ymax, xmax)` ⚠️ **순서 주의!**

---

## 10. 참고 링크

- **오픈API 목록**: https://www.vworld.kr/dev/v4apiRefer.do
- **OGC WMS 표준**: https://www.ogc.org/standard/wms
- **OGC WFS 표준**: https://www.ogc.org/standard/wfs
- **OGC Filter 표준**: https://www.ogc.org/standard/filter
- **장소분류코드**: https://www.vworld.kr/contents/브이월드_장소분류코드_20240712.xlsx
- **WFS 컬럼정보**: https://www.vworld.kr/contents/브이월드_WFS_컬럼정보.xlsx