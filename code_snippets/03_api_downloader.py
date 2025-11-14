"""
API 다운로더 클래스
파일명: core/api/downloader.py

QuickOSM의 downloader.py 참고
"""

import logging
from qgis.core import Qgis, QgsFileDownloader
from qgis.PyQt.QtCore import QByteArray, QEventLoop, QUrl, QUrlQuery

LOGGER = logging.getLogger('VworldPlugin')


class Downloader:
    """
    HTTP 다운로더 베이스 클래스
    QgsFileDownloader를 사용하여 동기식 다운로드 구현
    """

    def __init__(self, url: str = None):
        """
        생성자
        
        :param url: 다운로드할 URL
        """
        self._url = QUrl(url) if url else None
        self.result_path = None  # 저장될 파일 경로
        self.errors = []  # 에러 메시지 리스트

    def error(self, messages: str):
        """
        에러 메시지 저장
        
        :param messages: 에러 메시지
        """
        self.errors = messages
        LOGGER.error(f"Download error: {messages}")

    @staticmethod
    def canceled():
        """다운로드 취소 시 호출"""
        LOGGER.info('Request canceled')

    @staticmethod
    def completed():
        """다운로드 완료 시 호출"""
        LOGGER.info('Request completed')

    def download(self, use_post=False, post_data=None):
        """
        데이터 다운로드 실행
        
        :param use_post: POST 방식 사용 여부
        :param post_data: POST 데이터 (딕셔너리)
        """
        if use_post and post_data:
            # POST 요청
            # URL에서 쿼리 파라미터 제거하고 POST body로 전송
            url_query = QUrlQuery(self._url)
            
            # POST 데이터 구성
            data_string = "&".join([f"{k}={v}" for k, v in post_data.items()])
            
            downloader = QgsFileDownloader(
                self._url,
                self.result_path,
                delayStart=True,
                httpMethod=Qgis.HttpMethod.Post,
                data=QByteArray(str.encode(data_string))
            )
        else:
            # GET 요청
            downloader = QgsFileDownloader(
                self._url,
                self.result_path,
                delayStart=True
            )
        
        # 이벤트 루프로 동기식 처리
        loop = QEventLoop()
        downloader.downloadExited.connect(loop.quit)
        downloader.downloadError.connect(self.error)
        downloader.downloadCanceled.connect(self.canceled)
        downloader.downloadCompleted.connect(self.completed)
        
        # 다운로드 시작
        downloader.startDownload()
        
        # 완료될 때까지 대기
        loop.exec()


# 사용 예제
if __name__ == '__main__':
    # GET 요청 예제
    downloader = Downloader("https://api.example.com/data")
    downloader.result_path = "/tmp/output.json"
    downloader.download()
    
    # POST 요청 예제
    downloader2 = Downloader("https://api.example.com/query")
    downloader2.result_path = "/tmp/output2.json"
    downloader2.download(
        use_post=True,
        post_data={'key': 'value', 'param': 'test'}
    )

