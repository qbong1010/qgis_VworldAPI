"""
Processing 알고리즘 예제
파일명: processing/algorithms/download_data.py

QuickOSM의 quickosm_process.py 구조 참고
"""

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterString,
    QgsProcessingParameterEnum,
    QgsProcessingParameterExtent,
    QgsProcessingOutputVectorLayer,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessing
)
from qgis.PyQt.QtGui import QIcon


class DownloadVworldData(QgsProcessingAlgorithm):
    """Vworld 데이터 다운로드 Processing 알고리즘"""

    # 파라미터 이름 상수
    API_KEY = 'API_KEY'
    LAYER_TYPE = 'LAYER_TYPE'
    EXTENT = 'EXTENT'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        """생성자"""
        super().__init__()

    def name(self):
        """알고리즘 ID (소문자, 공백 없음)"""
        return 'downloadvworlddata'

    def displayName(self):
        """알고리즘 표시 이름"""
        return 'Download Vworld Data'

    def group(self):
        """알고리즘 그룹"""
        return 'Download'

    def groupId(self):
        """그룹 ID"""
        return 'download'

    def shortHelpString(self):
        """도움말 텍스트"""
        return """
        Vworld Open API를 사용하여 공간 데이터를 다운로드합니다.
        
        파라미터:
        - API Key: Vworld API 키 (필수)
        - Layer Type: 다운로드할 레이어 종류
        - Extent: 다운로드 영역 (BBOX)
        
        출력:
        - Vector Layer: 다운로드된 벡터 레이어
        """

    def icon(self):
        """알고리즘 아이콘"""
        import os
        icon_path = os.path.join(
            os.path.dirname(__file__),
            '../../resources/icons/vworld_icon.svg'
        )
        return QIcon(icon_path)

    def createInstance(self):
        """알고리즘 인스턴스 생성"""
        return DownloadVworldData()

    def initAlgorithm(self, config=None):
        """
        알고리즘 파라미터 및 출력 정의
        
        :param config: 설정 (사용 안함)
        """
        # API Key 파라미터
        self.addParameter(
            QgsProcessingParameterString(
                self.API_KEY,
                'Vworld API Key',
                defaultValue='',
                optional=False
            )
        )
        
        # Layer Type 선택 파라미터
        layer_types = [
            'Building (lt_c_aisresc)',
            'Administrative Dong (lt_c_ademd_info)',
            'Road (lt_c_uq151)',
            'Land Use (lp_pa_cbnd_bonbun)'
        ]
        
        self.addParameter(
            QgsProcessingParameterEnum(
                self.LAYER_TYPE,
                'Layer Type',
                options=layer_types,
                defaultValue=0,
                optional=False
            )
        )
        
        # 영역(Extent) 파라미터
        self.addParameter(
            QgsProcessingParameterExtent(
                self.EXTENT,
                'Download Extent',
                optional=True
            )
        )
        
        # 출력 레이어
        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT,
                'Output Layer',
                QgsProcessing.TypeVectorAnyGeometry
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        알고리즘 실행
        
        :param parameters: 입력 파라미터
        :param context: Processing 컨텍스트
        :param feedback: 피드백 객체
        :return: 출력 딕셔너리
        """
        # 멀티스텝 피드백 (진행률 표시)
        multi_feedback = QgsProcessingMultiStepFeedback(3, feedback)
        
        # Step 1: 파라미터 가져오기
        multi_feedback.setCurrentStep(0)
        multi_feedback.pushInfo('파라미터 확인 중...')
        
        api_key = self.parameterAsString(parameters, self.API_KEY, context)
        layer_type_idx = self.parameterAsEnum(parameters, self.LAYER_TYPE, context)
        extent = self.parameterAsExtent(parameters, self.EXTENT, context)
        
        # 레이어 타입 매핑
        layer_type_map = {
            0: 'lt_c_aisresc',  # Building
            1: 'lt_c_ademd_info',  # Administrative Dong
            2: 'lt_c_uq151',  # Road
            3: 'lp_pa_cbnd_bonbun'  # Land Use
        }
        layer_type = layer_type_map[layer_type_idx]
        
        # 검증
        if not api_key:
            raise QgsProcessingException('API Key is required')
        
        multi_feedback.pushInfo(f'Layer Type: {layer_type}')
        
        # Step 2: 데이터 다운로드
        multi_feedback.setCurrentStep(1)
        multi_feedback.pushInfo('Vworld API에서 데이터 다운로드 중...')
        
        if feedback.isCanceled():
            return {}
        
        # BBOX 문자열 생성
        bbox_string = None
        if not extent.isNull():
            bbox_string = (
                f"{extent.xMinimum()},{extent.yMinimum()},"
                f"{extent.xMaximum()},{extent.yMaximum()}"
            )
            multi_feedback.pushInfo(f'BBOX: {bbox_string}')
        
        # API 호출
        from VworldPlugin.core.api.vworld_api import build_vworld_url, VworldAPI
        
        url = build_vworld_url(
            service='wfs',
            request='GetFeature',
            api_key=api_key,
            typename=layer_type,
            bbox=bbox_string if bbox_string else '',
            srsname='EPSG:4326',
            output='json',
            maxFeatures=1000
        )
        
        client = VworldAPI(url, api_key)
        
        try:
            data_file = client.fetch_data()
            multi_feedback.pushInfo(f'Downloaded to: {data_file}')
        except Exception as e:
            raise QgsProcessingException(f'Download failed: {str(e)}')
        
        if feedback.isCanceled():
            return {}
        
        # Step 3: 레이어 생성
        multi_feedback.setCurrentStep(2)
        multi_feedback.pushInfo('레이어 생성 중...')
        
        from VworldPlugin.core.parser.data_parser import create_and_load_layer
        
        layer_name = f'Vworld_{layer_type}'
        
        try:
            layer = create_and_load_layer(
                data_file,
                layer_name,
                add_to_project=False  # Processing에서는 자동 추가됨
            )
        except Exception as e:
            raise QgsProcessingException(f'Layer creation failed: {str(e)}')
        
        # 레이어를 context에 추가
        context.temporaryLayerStore().addMapLayer(layer)
        
        multi_feedback.pushInfo('완료!')
        
        # 결과 반환
        return {self.OUTPUT: layer.id()}


# Processing Provider 클래스
from qgis.core import QgsProcessingProvider


class VworldProvider(QgsProcessingProvider):
    """Vworld Processing Provider"""

    def id(self):
        """Provider ID"""
        return 'vworld'

    def name(self):
        """Provider 이름"""
        return 'Vworld'

    def icon(self):
        """Provider 아이콘"""
        import os
        icon_path = os.path.join(
            os.path.dirname(__file__),
            '../resources/icons/vworld_icon.svg'
        )
        return QIcon(icon_path)

    def loadAlgorithms(self):
        """알고리즘 로드"""
        # 다운로드 알고리즘 추가
        self.addAlgorithm(DownloadVworldData())
        
        # 추가 알고리즘이 있으면 여기에 등록
        # self.addAlgorithm(AnotherAlgorithm())

