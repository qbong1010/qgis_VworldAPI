"""
예외 처리 클래스
파일명: core/exceptions.py

QuickOSM의 exceptions.py 구조 참고
"""

from qgis.core import Qgis


class VworldException(Exception):
    """
    Vworld 플러그인 기본 예외 클래스
    사용자에게 표시될 메시지와 레벨을 포함
    """

    def __init__(
        self,
        message: str,
        level: Qgis.MessageLevel = Qgis.Critical,
        duration: int = 5,
        more_details: str = None
    ):
        """
        생성자
        
        :param message: 에러 메시지
        :param level: QGIS 메시지 레벨
        :param duration: 메시지 표시 시간 (초)
        :param more_details: 상세 정보
        """
        super().__init__(message)
        self.message = message
        self.level = level
        self.duration = duration
        self.more_details = more_details


class VworldAPIException(VworldException):
    """
    Vworld API 관련 예외
    API 호출 실패, 인증 실패, 데이터 오류 등
    """

    def __init__(self, message: str = None, **kwargs):
        if message is None:
            message = "Vworld API error occurred"
        super().__init__(message, **kwargs)


class VworldAPIKeyException(VworldAPIException):
    """API 키 관련 예외"""

    def __init__(self, **kwargs):
        message = "Invalid or missing Vworld API key"
        super().__init__(message, level=Qgis.Critical, **kwargs)


class VworldAPILimitException(VworldAPIException):
    """API 사용량 제한 예외"""

    def __init__(self, **kwargs):
        message = "API usage limit exceeded"
        more_details = "You have exceeded your daily API quota. Please try again tomorrow."
        super().__init__(message, level=Qgis.Warning, more_details=more_details, **kwargs)


class VworldDataException(VworldException):
    """
    데이터 처리 관련 예외
    파싱 실패, 잘못된 형식 등
    """

    def __init__(self, message: str = None, **kwargs):
        if message is None:
            message = "Data processing error"
        super().__init__(message, **kwargs)


class VworldNetworkException(VworldException):
    """
    네트워크 관련 예외
    연결 실패, 타임아웃 등
    """

    def __init__(self, message: str = None, **kwargs):
        if message is None:
            message = "Network error occurred"
        super().__init__(message, level=Qgis.Critical, **kwargs)


class VworldLayerException(VworldException):
    """
    레이어 생성/처리 관련 예외
    """

    def __init__(self, message: str = None, **kwargs):
        if message is None:
            message = "Layer creation error"
        super().__init__(message, **kwargs)


# 예외 처리 헬퍼 함수
def handle_vworld_exception(exception: VworldException, iface):
    """
    Vworld 예외를 처리하고 사용자에게 표시
    
    :param exception: VworldException 인스턴스
    :param iface: QGIS 인터페이스
    """
    from qgis.PyQt.QtWidgets import QPushButton, QMessageBox
    
    # 메시지 바에 표시
    widget = iface.messageBar().createMessage(
        'Vworld Plugin',
        exception.message
    )
    
    # 상세 정보 버튼 추가
    if exception.more_details:
        button = QPushButton('자세히')
        widget.layout().addWidget(button)
        button.pressed.connect(
            lambda: QMessageBox.information(
                None,
                'Vworld Plugin - Details',
                exception.more_details
            )
        )
    
    iface.messageBar().pushWidget(
        widget,
        exception.level,
        exception.duration
    )


# 사용 예제
def example_usage():
    """예외 처리 사용 예제"""
    
    try:
        # API 호출
        api_key = get_api_key()
        if not api_key:
            raise VworldAPIKeyException()
        
        # 데이터 다운로드
        data = download_data(api_key)
        if not data:
            raise VworldDataException(
                "No data returned from API",
                more_details="The API returned an empty response. "
                            "This could be due to invalid parameters or no data "
                            "in the specified area."
            )
        
        # 레이어 생성
        layer = create_layer(data)
        
    except VworldAPIKeyException as e:
        # API 키 오류 - 설정 다이얼로그 표시
        handle_vworld_exception(e, iface)
        show_settings_dialog()
        
    except VworldAPILimitException as e:
        # 사용량 초과 - 경고만 표시
        handle_vworld_exception(e, iface)
        
    except VworldNetworkException as e:
        # 네트워크 오류 - 재시도 옵션
        handle_vworld_exception(e, iface)
        if show_retry_dialog():
            retry_download()
    
    except VworldException as e:
        # 기타 Vworld 예외
        handle_vworld_exception(e, iface)
        
    except Exception as e:
        # 예상치 못한 예외
        import logging
        logger = logging.getLogger('VworldPlugin')
        logger.exception("Unexpected error")
        
        iface.messageBar().pushCritical(
            'Vworld Plugin',
            f'Unexpected error: {str(e)}'
        )


# 데코레이터를 사용한 예외 처리
def handle_exceptions(func):
    """
    함수를 감싸서 예외를 자동으로 처리하는 데코레이터
    
    사용 예:
        @handle_exceptions
        def my_function():
            # ... code ...
    """
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except VworldException as e:
            # Vworld 예외는 메시지 표시
            from qgis.utils import iface
            handle_vworld_exception(e, iface)
        except Exception as e:
            # 기타 예외는 로그에 기록
            import logging
            logger = logging.getLogger('VworldPlugin')
            logger.exception(f"Error in {func.__name__}")
            
            from qgis.utils import iface
            iface.messageBar().pushCritical(
                'Vworld Plugin',
                f'Error: {str(e)}'
            )
    
    return wrapper

