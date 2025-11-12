"""
QGIS 플러그인 진입점 예제
파일명: __init__.py
"""

__copyright__ = 'Copyright 2025, Your Organization'
__license__ = 'GPL version 3'
__email__ = 'your@email.com'


def classFactory(iface):
    """
    QGIS가 플러그인을 로드할 때 호출하는 팩토리 함수
    
    :param iface: QGIS 인터페이스 객체
    :type iface: QgsInterface
    :return: 플러그인 인스턴스
    """
    from VworldPlugin.vworld_plugin import VworldPlugin
    return VworldPlugin(iface)

