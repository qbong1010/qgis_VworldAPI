"""
전체 워크플로우 통합 예제
파일명: core/process.py

QuickOSM의 process.py 구조 참고
"""

import logging
from typing import Optional
from qgis.core import QgsFeedback, QgsRectangle
from qgis.PyQt.QtWidgets import QDialog, QApplication

LOGGER = logging.getLogger('VworldPlugin')


def download_vworld_data(
    api_key: str,
    layer_type: str,
    bbox: Optional[QgsRectangle] = None,
    layer_name: str = "Vworld Data",
    dialog: Optional[QDialog] = None,
    feedback: Optional[QgsFeedback] = None,
    apply_style: bool = True
) -> int:
    """
    Vworld 데이터 다운로드 및 레이어 생성 전체 프로세스
    
    :param api_key: Vworld API 키
    :param layer_type: 레이어 타입 (예: 'lt_c_aisresc')
    :param bbox: 바운딩 박스 (QgsRectangle)
    :param layer_name: 레이어 이름
    :param dialog: 다이얼로그 (진행상황 표시용)
    :param feedback: 피드백 객체
    :param apply_style: 스타일 적용 여부
    :return: 생성된 레이어 수
    """
    
    # 진행 상황 표시
    if dialog:
        dialog.set_progress_text('Vworld API 연결 준비 중...')
        dialog.set_progress_percentage(0)
    
    if feedback:
        feedback.pushInfo('Starting Vworld data download...')
    
    # Step 1: URL 생성
    if dialog:
        dialog.set_progress_text('API URL 생성 중...')
        dialog.set_progress_percentage(10)
    
    from VworldPlugin.core.api.vworld_api import build_vworld_url
    
    # BBOX 문자열 생성
    bbox_string = None
    if bbox:
        bbox_string = (
            f"{bbox.xMinimum()},{bbox.yMinimum()},"
            f"{bbox.xMaximum()},{bbox.yMaximum()}"
        )
        LOGGER.info(f"Using BBOX: {bbox_string}")
    
    api_url = build_vworld_url(
        service='wfs',
        request='GetFeature',
        api_key=api_key,
        typename=layer_type,
        bbox=bbox_string if bbox_string else '',
        srsname='EPSG:4326',
        output='json',
        maxFeatures=1000
    )
    
    LOGGER.info(f"API URL: {api_url}")
    
    # 취소 확인
    if feedback and feedback.isCanceled():
        LOGGER.info("Process canceled by user")
        return 0
    
    # Step 2: 데이터 다운로드
    if dialog:
        dialog.set_progress_text('데이터 다운로드 중...')
        dialog.set_progress_percentage(30)
    
    QApplication.processEvents()  # UI 업데이트
    
    from VworldPlugin.core.api.vworld_api import VworldAPI
    from VworldPlugin.core.exceptions import VworldAPIException
    
    try:
        client = VworldAPI(api_url, api_key)
        data_file = client.fetch_data()
        LOGGER.info(f"Data downloaded to: {data_file}")
    except VworldAPIException as e:
        LOGGER.error(f"API error: {e}")
        if dialog:
            dialog.set_progress_text(f'다운로드 실패: {e}')
        raise
    except Exception as e:
        LOGGER.exception("Unexpected error during download")
        raise
    
    # 취소 확인
    if feedback and feedback.isCanceled():
        LOGGER.info("Process canceled after download")
        return 0
    
    # Step 3: 레이어 생성
    if dialog:
        dialog.set_progress_text('레이어 생성 중...')
        dialog.set_progress_percentage(60)
    
    QApplication.processEvents()
    
    from VworldPlugin.core.parser.data_parser import (
        VworldLayerCreator,
        apply_categorized_style
    )
    
    creator = VworldLayerCreator(data_file, layer_name)
    
    # 시그널 연결 (다이얼로그가 있는 경우)
    if dialog:
        creator.signalText.connect(dialog.set_progress_text)
        creator.signalPercentage.connect(
            lambda p: dialog.set_progress_percentage(60 + p * 0.3)
        )
    
    try:
        layer = creator.create_layer()
        LOGGER.info(f"Layer created: {layer.name()}")
    except Exception as e:
        LOGGER.exception("Failed to create layer")
        if dialog:
            dialog.set_progress_text(f'레이어 생성 실패: {e}')
        raise
    
    # 취소 확인
    if feedback and feedback.isCanceled():
        LOGGER.info("Process canceled after layer creation")
        return 0
    
    # Step 4: 스타일 적용 (선택적)
    if apply_style:
        if dialog:
            dialog.set_progress_text('스타일 적용 중...')
            dialog.set_progress_percentage(90)
        
        QApplication.processEvents()
        
        # 타입에 따른 스타일 필드 선택
        style_field_map = {
            'lt_c_aisresc': 'buld_se_nm',  # 건물 구분
            'lt_c_ademd_info': 'emd_kor_nm',  # 읍면동명
        }
        
        style_field = style_field_map.get(layer_type)
        if style_field and style_field in [f.name() for f in layer.fields()]:
            try:
                apply_categorized_style(layer, style_field)
                LOGGER.info(f"Style applied using field: {style_field}")
            except Exception as e:
                LOGGER.warning(f"Failed to apply style: {e}")
    
    # Step 5: 프로젝트에 추가
    if dialog:
        dialog.set_progress_text('프로젝트에 레이어 추가 중...')
        dialog.set_progress_percentage(95)
    
    QApplication.processEvents()
    
    # 쿼리 정보 저장 (나중에 재로드 가능)
    query_info = {
        'api_key': api_key,
        'layer_type': layer_type,
        'bbox': bbox_string
    }
    
    creator.add_to_project(layer, str(query_info))
    
    # 완료
    if dialog:
        dialog.set_progress_text('완료!')
        dialog.set_progress_percentage(100)
    
    if feedback:
        feedback.pushInfo('Process completed successfully')
    
    LOGGER.info(f"Successfully created and added layer: {layer.name()}")
    
    return 1  # 생성된 레이어 수


def reload_vworld_layer(layer_name: str, dialog: Optional[QDialog] = None):
    """
    기존 레이어를 다시 로드
    
    :param layer_name: 레이어 이름
    :param dialog: 다이얼로그
    """
    from qgis.core import QgsProject, QgsExpressionContextUtils
    
    # 레이어 찾기
    layers = QgsProject.instance().mapLayersByName(layer_name)
    if not layers:
        raise Exception(f"Layer not found: {layer_name}")
    
    layer = layers[0]
    
    # 저장된 쿼리 정보 가져오기
    query_info = QgsExpressionContextUtils.layerScope(layer).variable('vworld_query')
    
    if not query_info:
        raise Exception("No query information found for this layer")
    
    # 쿼리 정보 파싱
    import ast
    query_dict = ast.literal_eval(query_info)
    
    # 새 레이어 이름
    new_layer_name = f"{layer_name}_reloaded"
    
    # 다운로드 재실행
    return download_vworld_data(
        api_key=query_dict['api_key'],
        layer_type=query_dict['layer_type'],
        bbox=query_dict.get('bbox'),
        layer_name=new_layer_name,
        dialog=dialog
    )


# 사용 예제
if __name__ == '__main__':
    # 기본 사용
    num_layers = download_vworld_data(
        api_key='YOUR_API_KEY',
        layer_type='lt_c_aisresc',
        layer_name='Seoul Buildings'
    )
    
    print(f"Created {num_layers} layer(s)")
    
    # BBOX 지정
    from qgis.core import QgsRectangle
    
    bbox = QgsRectangle(126.9, 37.5, 127.0, 37.6)
    
    num_layers = download_vworld_data(
        api_key='YOUR_API_KEY',
        layer_type='lt_c_ademd_info',
        bbox=bbox,
        layer_name='Administrative Dong'
    )

