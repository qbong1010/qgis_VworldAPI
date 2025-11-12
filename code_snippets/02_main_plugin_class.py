"""
메인 플러그인 클래스 예제
파일명: vworld_plugin.py

QuickOSM의 quick_osm.py를 참고한 구조
"""

import logging
import os
from qgis.core import Qgis, QgsApplication
from qgis.PyQt.QtCore import QCoreApplication, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu

LOGGER = logging.getLogger('VworldPlugin')


class VworldPlugin:
    """Vworld 플러그인 메인 클래스"""

    def __init__(self, iface):
        """
        생성자
        
        :param iface: QGIS 인터페이스 인스턴스
        :type iface: QgsInterface
        """
        # QGIS 인터페이스 저장
        self.iface = iface
        
        # 번역 설정
        self.setup_translation()
        
        # Processing Provider (나중에 초기화)
        self.provider = None
        
        # UI 요소들
        self.toolbar = None
        self.menu = None
        self.main_action = None
        
        LOGGER.info("Vworld Plugin initialized")

    def setup_translation(self):
        """다국어 번역 설정"""
        # 사용자 로케일 가져오기
        from qgis.PyQt.QtCore import QSettings
        locale = QSettings().value('locale/userLocale')[0:2]
        
        # 번역 파일 경로
        locale_path = os.path.join(
            os.path.dirname(__file__),
            'i18n',
            f'vworld_{locale}.qm'
        )
        
        # 번역 파일이 존재하면 로드
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)
            LOGGER.info(f"Translation loaded: {locale}")

    def initProcessing(self):
        """Processing Provider 초기화"""
        from VworldPlugin.processing.provider import VworldProvider
        
        self.provider = VworldProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)
        LOGGER.info("Processing provider registered")

    def initGui(self):
        """
        사용자 인터페이스 초기화
        QGIS가 플러그인 로드 시 자동으로 호출
        """
        # Processing 먼저 초기화
        self.initProcessing()
        
        # 아이콘 경로
        icon_path = os.path.join(
            os.path.dirname(__file__),
            'resources/icons/vworld_icon.svg'
        )
        icon = QIcon(icon_path)
        
        # 툴바 추가
        self.toolbar = self.iface.addToolBar('Vworld')
        self.toolbar.setObjectName('Vworld')
        
        # 메뉴 생성
        self.menu = QMenu('Vworld')
        self.menu.setIcon(icon)
        
        # Vector 메뉴에 추가
        self.iface.vectorMenu().addMenu(self.menu)
        
        # 메인 액션 생성
        self.main_action = QAction(
            icon,
            'Vworld Data Download…',
            self.iface.mainWindow()
        )
        
        # 액션 트리거 연결
        self.main_action.triggered.connect(self.open_dialog)
        
        # 툴바와 메뉴에 액션 추가
        self.toolbar.addAction(self.main_action)
        self.menu.addAction(self.main_action)
        
        LOGGER.info("Vworld Plugin GUI initialized")

    def unload(self):
        """
        플러그인 언로드
        QGIS가 플러그인 제거 시 자동으로 호출
        """
        # 메뉴에서 제거
        self.iface.removePluginVectorMenu('&Vworld', self.main_action)
        
        # 툴바 아이콘 제거
        self.iface.removeToolBarIcon(self.main_action)
        
        # 툴바 제거
        if self.toolbar:
            del self.toolbar
        
        # Processing Provider 제거
        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)
        
        LOGGER.info("Vworld Plugin unloaded")

    def open_dialog(self):
        """메인 다이얼로그 열기"""
        from VworldPlugin.ui.dialog import VworldDialog
        
        dialog = VworldDialog(self.iface)
        result = dialog.exec()
        
        if result:
            LOGGER.info("Dialog closed with success")

