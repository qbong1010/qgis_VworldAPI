"""
Legend Dialog

레이어 범례를 표시하는 다이얼로그
"""

import logging
from qgis.PyQt.QtCore import Qt, QSize
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QWidget, QDialogButtonBox,
    QMessageBox
)
from qgis.PyQt.QtGui import QPixmap

from ..core.api.legend_client import VworldLegendClient

LOGGER = logging.getLogger('QuickVworld')


class LegendDialog(QDialog):
    """
    범례를 표시하는 다이얼로그.
    
    VWorld API에서 범례 이미지를 다운로드하여 표시합니다.
    """

    def __init__(self, layer_name, layer_label=None, parent=None):
        """
        Constructor.
        
        :param layer_name: 레이어 이름 (예: 'lt_c_upisuq153')
        :type layer_name: str
        :param layer_label: 레이어 한글 이름 (예: '도시계획시설(공간시설)')
        :type layer_label: str
        :param parent: 부모 위젯
        :type parent: QWidget
        """
        super().__init__(parent)
        
        self.layer_name = layer_name
        self.layer_label = layer_label or layer_name
        self.legend_pixmap = None
        
        self._setup_ui()
        self._load_legend()

    def _setup_ui(self):
        """UI 구성"""
        self.setWindowTitle(f"{self.layer_label} - 범례")
        self.setMinimumSize(400, 300)
        
        # 메인 레이아웃
        layout = QVBoxLayout()
        
        # 제목 레이블
        title_label = QLabel(f"<h3>{self.layer_label}</h3>")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 스크롤 영역 (범례 이미지용)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 범례 이미지 레이블
        self.legend_label = QLabel()
        self.legend_label.setAlignment(Qt.AlignCenter)
        self.legend_label.setScaledContents(False)
        self.legend_label.setText("범례를 불러오는 중...")
        
        scroll_area.setWidget(self.legend_label)
        layout.addWidget(scroll_area)
        
        # 버튼
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)

    def _load_legend(self):
        """범례 이미지를 다운로드하여 표시"""
        try:
            # 범례 다운로드
            client = VworldLegendClient()
            pixmap = client.fetch_legend_as_pixmap(
                layer=self.layer_name,
                style=self.layer_name,
                legend_type='ALL'
            )
            
            if pixmap and not pixmap.isNull():
                self.legend_pixmap = pixmap
                self.legend_label.setPixmap(pixmap)
                LOGGER.info(f"Legend loaded successfully: {self.layer_name}")
            else:
                self.legend_label.setText(
                    f"범례를 불러올 수 없습니다.\n\n"
                    f"레이어: {self.layer_name}\n\n"
                    f"VWorld API에서 해당 레이어의 범례를\n"
                    f"제공하지 않거나 네트워크 오류가 발생했습니다."
                )
                LOGGER.warning(f"Failed to load legend: {self.layer_name}")
                
        except Exception as e:
            error_msg = f"범례 로드 중 오류 발생: {str(e)}"
            self.legend_label.setText(error_msg)
            LOGGER.error(error_msg)

    def get_pixmap(self):
        """
        범례 이미지 Pixmap 반환.
        
        :return: 범례 이미지 Pixmap
        :rtype: QPixmap or None
        """
        return self.legend_pixmap


def show_legend_dialog(layer_name, layer_label=None, parent=None):
    """
    범례 다이얼로그를 표시하는 헬퍼 함수.
    
    :param layer_name: 레이어 이름
    :type layer_name: str
    :param layer_label: 레이어 한글 이름
    :type layer_label: str
    :param parent: 부모 위젯
    :type parent: QWidget
    :return: 다이얼로그 결과
    :rtype: int
    """
    dialog = LegendDialog(layer_name, layer_label, parent)
    return dialog.exec_()

