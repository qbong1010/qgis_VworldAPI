"""
레이어 생성 및 프로젝트 추가
파일명: core/parser/data_parser.py

QuickOSM의 osm_parser.py와 process.py 구조 참고
"""

import logging
from qgis.core import (
    QgsVectorLayer,
    QgsProject,
    QgsLayerMetadata,
    QgsWkbTypes,
    QgsField,
    QgsExpressionContextUtils
)
from qgis.PyQt.QtCore import QVariant, QObject, pyqtSignal

LOGGER = logging.getLogger('VworldPlugin')


class VworldLayerCreator(QObject):
    """
    Vworld 데이터로부터 QGIS 레이어 생성
    시그널을 통해 진행 상황 전달
    """
    
    # 시그널 정의
    signalPercentage = pyqtSignal(int, name='signalPercentage')
    signalText = pyqtSignal(str, name='signalText')

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
        super().__init__()
        self.data_file = data_file
        self.layer_name = layer_name
        self.output_format = output_format

    def create_layer(self) -> QgsVectorLayer:
        """
        벡터 레이어 생성
        
        :return: 생성된 레이어
        :raises Exception: 레이어 생성 실패 시
        """
        self.signalText.emit(f'레이어 생성 중: {self.layer_name}')
        self.signalPercentage.emit(10)
        
        LOGGER.info(f"Creating layer from: {self.data_file}")
        
        # OGR을 통한 레이어 로드
        # 포맷에 따라 URI 구성 달라질 수 있음
        if self.output_format.upper() == "GEOJSON":
            uri = self.data_file
        else:
            uri = f"{self.data_file}|layername={self.layer_name}"
        
        layer = QgsVectorLayer(
            uri,
            self.layer_name,
            "ogr"  # OGR provider
        )
        
        if not layer.isValid():
            raise Exception(f"Layer is not valid: {self.data_file}")
        
        self.signalPercentage.emit(50)
        
        # 인코딩 설정
        layer.setProviderEncoding('UTF-8')
        
        # 메타데이터 추가
        self.add_metadata(layer)
        
        self.signalPercentage.emit(80)
        
        # 필드 처리 (필요 시)
        self.process_fields(layer)
        
        self.signalPercentage.emit(100)
        self.signalText.emit('레이어 생성 완료')
        
        return layer

    def add_metadata(self, layer: QgsVectorLayer):
        """
        레이어에 메타데이터 추가
        
        :param layer: 대상 레이어
        """
        metadata = QgsLayerMetadata()
        metadata.setRights(['© Vworld Open API'])
        metadata.setLicenses(['Vworld Open API License'])
        metadata.setAbstract('Data downloaded from Vworld Open API')
        layer.setMetadata(metadata)
        
        LOGGER.info("Metadata added to layer")

    def process_fields(self, layer: QgsVectorLayer):
        """
        필드 처리 (필요한 경우 필드 추가/제거)
        
        :param layer: 대상 레이어
        """
        # 필요 시 필드 추가
        layer.startEditing()
        provider = layer.dataProvider()
        
        # 예: 데이터 소스 필드 추가
        if 'data_source' not in [field.name() for field in layer.fields()]:
            provider.addAttributes([
                QgsField('data_source', QVariant.String)
            ])
            layer.updateFields()
            
            # 모든 피처에 값 설정
            for feature in layer.getFeatures():
                feature.setAttribute('data_source', 'Vworld')
                layer.updateFeature(feature)
        
        layer.commitChanges()

    def add_to_project(self, layer: QgsVectorLayer, query: str = None):
        """
        프로젝트에 레이어 추가
        
        :param layer: 추가할 레이어
        :param query: 레이어 생성에 사용된 쿼리 (나중에 재로드 시 사용)
        """
        # 레이어 변수에 쿼리 정보 저장
        if query:
            QgsExpressionContextUtils.setLayerVariable(
                layer,
                'vworld_query',
                query
            )
        
        # 프로젝트에 추가
        QgsProject.instance().addMapLayer(layer)
        
        LOGGER.info(f"Layer added to project: {layer.name()}")


def create_and_load_layer(
    data_file: str,
    layer_name: str = "Vworld Data",
    add_to_project: bool = True,
    apply_style: bool = False,
    style_field: str = None
) -> QgsVectorLayer:
    """
    데이터 파일로부터 레이어 생성 및 로드
    
    :param data_file: 데이터 파일 경로
    :param layer_name: 레이어 이름
    :param add_to_project: 프로젝트에 추가 여부
    :param apply_style: 스타일 적용 여부
    :param style_field: 스타일 적용 시 사용할 필드
    :return: 생성된 레이어
    """
    creator = VworldLayerCreator(data_file, layer_name)
    layer = creator.create_layer()
    
    # 스타일 적용
    if apply_style and style_field:
        apply_categorized_style(layer, style_field)
    
    # 프로젝트에 추가
    if add_to_project:
        creator.add_to_project(layer)
    
    return layer


def apply_categorized_style(layer: QgsVectorLayer, field_name: str):
    """
    카테고리별 스타일 적용
    
    :param layer: 대상 레이어
    :param field_name: 카테고리 필드명
    """
    from qgis.core import (
        QgsSymbol,
        QgsCategorizedSymbolRenderer,
        QgsRendererCategory
    )
    from qgis.PyQt.QtGui import QColor
    
    # 필드 인덱스
    field_index = layer.fields().indexOf(field_name)
    if field_index == -1:
        LOGGER.warning(f"Field not found: {field_name}")
        return
    
    # 고유 값 가져오기
    unique_values = layer.uniqueValues(field_index)
    
    # 카테고리 생성
    categories = []
    colors = [
        '#e41a1c', '#377eb8', '#4daf4a', '#984ea3',
        '#ff7f00', '#ffff33', '#a65628', '#f781bf'
    ]
    
    for i, value in enumerate(unique_values):
        if value is None:
            continue
            
        # 심볼 생성
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        color = QColor(colors[i % len(colors)])
        symbol.setColor(color)
        
        # 카테고리 생성
        category = QgsRendererCategory(
            value,
            symbol,
            str(value)
        )
        categories.append(category)
    
    # 렌더러 적용
    renderer = QgsCategorizedSymbolRenderer(field_name, categories)
    layer.setRenderer(renderer)
    layer.triggerRepaint()
    
    LOGGER.info(f"Categorized style applied based on field: {field_name}")


# 사용 예제
if __name__ == '__main__':
    # 기본 사용
    layer = create_and_load_layer(
        '/tmp/vworld_data.geojson',
        'Buildings',
        add_to_project=True
    )
    
    # 스타일 적용
    layer_styled = create_and_load_layer(
        '/tmp/vworld_data.geojson',
        'Styled Buildings',
        add_to_project=True,
        apply_style=True,
        style_field='building_type'
    )

