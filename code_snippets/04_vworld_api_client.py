"""
Vworld API 클라이언트
파일명: core/api/vworld_api.py

QuickOSM의 connexion_oapi.py 구조 참고
"""

import logging
import os
from qgis.PyQt.QtCore import QDir, QFileInfo, QTemporaryFile, QUrlQuery
from VworldPlugin.core.api.downloader import Downloader
from VworldPlugin.core.exceptions import VworldAPIException

LOGGER = logging.getLogger('VworldPlugin')


class VworldAPI(Downloader):
    """Vworld Open API 클라이언트"""

    def __init__(self, url: str, api_key: str, output_format: str = 'json'):
        """
        생성자
        
        :param url: API 엔드포인트 URL
        :param api_key: Vworld API 키
        :param output_format: 출력 포맷 (json, xml 등)
        """
        super().__init__(url)
        self.api_key = api_key
        self.output_format = output_format
        
        # 임시 파일 생성
        extension = '.geojson' if output_format == 'json' else f'.{output_format}'
        temporary = QTemporaryFile(
            os.path.join(QDir.tempPath(), f'vworld-XXXXXX{extension}')
        )
        temporary.open()
        self.result_path = temporary.fileName()
        temporary.close()
        
        LOGGER.info(f"VworldAPI initialized with temp file: {self.result_path}")

    def fetch_data(self, additional_params: dict = None) -> str:
        """
        데이터 가져오기
        
        :param additional_params: 추가 파라미터
        :return: 결과 파일 경로
        :raises VworldAPIException: API 에러 발생 시
        """
        # URL에 API 키와 추가 파라미터 추가
        query = QUrlQuery(self._url)
        query.addQueryItem('key', self.api_key)
        
        if additional_params:
            for key, value in additional_params.items():
                query.addQueryItem(key, str(value))
        
        self._url.setQuery(query)
        
        LOGGER.info(f"Fetching data from: {self._url.toString()}")
        
        # 다운로드 실행
        self.download()
        
        # 에러 체크
        if self.errors:
            error_msg = ', '.join(self.errors) if isinstance(self.errors, list) else self.errors
            raise VworldAPIException(f"API Error: {error_msg}")
        
        # 파일 존재 확인
        file_info = QFileInfo(self.result_path)
        if not file_info.exists() or not file_info.isFile():
            raise FileNotFoundError(
                f"Downloaded file not found: {self.result_path}"
            )
        
        # 파일 내용 검증
        self.check_response_file(self.result_path)
        
        LOGGER.info(f"Data successfully downloaded to: {self.result_path}")
        return self.result_path

    @staticmethod
    def check_response_file(file_path: str):
        """
        응답 파일 검증
        에러 응답이 포함되어 있는지 확인
        
        :param file_path: 검증할 파일 경로
        :raises VworldAPIException: 에러 응답인 경우
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Vworld API 에러 응답 체크
                if 'error' in content.lower():
                    import json
                    try:
                        data = json.loads(content)
                        if 'error' in data:
                            raise VworldAPIException(
                                f"API returned error: {data['error']}"
                            )
                    except json.JSONDecodeError:
                        pass
                
                # 빈 응답 체크
                if len(content.strip()) == 0:
                    raise VworldAPIException("API returned empty response")
                    
        except Exception as e:
            LOGGER.warning(f"Response validation warning: {e}")


def build_vworld_url(
    service: str,
    request: str,
    api_key: str,
    **kwargs
) -> str:
    """
    Vworld API URL 생성 헬퍼 함수
    
    :param service: 서비스 종류 (wfs, wms, search 등)
    :param request: 요청 종류 (GetFeature, GetCapabilities 등)
    :param api_key: API 키
    :param kwargs: 추가 파라미터
    :return: 완성된 URL
    
    예제:
        url = build_vworld_url(
            service='wfs',
            request='GetFeature',
            api_key='YOUR_KEY',
            typename='lt_c_aisresc',
            bbox='126.9,37.5,127.0,37.6'
        )
    """
    # Vworld API 베이스 URL
    base_url = f"https://api.vworld.kr/req/{service}"
    
    # 기본 파라미터
    params = {
        'service': service.upper(),
        'request': request,
        'key': api_key,
        'format': kwargs.pop('format', 'json'),
        'version': kwargs.pop('version', '2.0.0')
    }
    
    # 추가 파라미터 병합
    params.update(kwargs)
    
    # URL 구성
    query_parts = []
    for key, value in params.items():
        if value is not None and value != '':
            query_parts.append(f"{key}={value}")
    
    query_string = '&'.join(query_parts)
    full_url = f"{base_url}?{query_string}"
    
    LOGGER.debug(f"Built URL: {full_url}")
    return full_url


# 사용 예제
if __name__ == '__main__':
    # WFS GetFeature 요청
    url = build_vworld_url(
        service='wfs',
        request='GetFeature',
        api_key='YOUR_API_KEY',
        typename='lt_c_aisresc',  # 건물 레이어
        bbox='126.9,37.5,127.0,37.6',  # 서울 일부 지역
        srsname='EPSG:4326',
        output='json',
        maxFeatures=100
    )
    
    client = VworldAPI(url, 'YOUR_API_KEY')
    result_file = client.fetch_data()
    print(f"Downloaded to: {result_file}")

