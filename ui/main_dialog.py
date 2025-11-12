"""
Main Dialog for Quick Vworld Plugin

This dialog allows users to:
- Select extent type (canvas or layer)
- Select layer (if layer extent is chosen)
- Choose to use selected features only
- Download VWorld WFS data
"""

import logging
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QCheckBox,
    QPushButton,
    QProgressBar,
    QGroupBox,
    QMessageBox,
    QSizePolicy
)
from qgis.core import QgsProject, QgsVectorLayer, QgsMessageLog, Qgis

from ..core.api.vworld_client import VworldWFSClient
from ..core.processor import VworldDataProcessor, ExtentType
from ..definitions.layers import URBAN_PLANNING_LAYERS, get_layer_info
from .legend_dialog import show_legend_dialog

LOGGER = logging.getLogger('QuickVworld')


class QuickVworldDialog(QDialog):
    """Main dialog for Quick Vworld plugin."""

    def __init__(self, iface, parent=None):
        """
        Constructor.
        
        :param iface: QGIS interface
        :type iface: QgsInterface
        :param parent: Parent widget
        :type parent: QWidget
        """
        super().__init__(parent)
        
        self.iface = iface
        self.processor = VworldDataProcessor(iface)
        
        # Initialize UI
        self.setup_ui()
        
        # Populate dropdowns
        self.populate_layer_combo()
        
        # Connect signals
        self.connect_signals()
        
        # Initial state
        self.update_layer_controls_state()

    def setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("Quick Vworld - WFS 데이터 다운로드")
        self.setMinimumWidth(500)
        self.setMinimumHeight(350)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # === Extent Selection Group ===
        extent_group = QGroupBox("범위 선택")
        extent_layout = QVBoxLayout()
        
        # Extent type label and combo
        extent_type_label = QLabel("다운로드 범위:")
        self.extent_type_combo = QComboBox()
        self.extent_type_combo.addItem("캔버스 범위", ExtentType.CANVAS)
        self.extent_type_combo.addItem("레이어 범위", ExtentType.LAYER)
        
        extent_layout.addWidget(extent_type_label)
        extent_layout.addWidget(self.extent_type_combo)
        
        # Layer selection label and combo
        self.layer_label = QLabel("레이어 선택:")
        self.layer_combo = QComboBox()
        
        extent_layout.addWidget(self.layer_label)
        extent_layout.addWidget(self.layer_combo)
        
        # Selected features checkbox
        self.selected_features_checkbox = QCheckBox("선택한 피처만 사용")
        extent_layout.addWidget(self.selected_features_checkbox)
        
        extent_group.setLayout(extent_layout)
        layout.addWidget(extent_group)
        
        # === Layer Type Selection Group ===
        layer_type_group = QGroupBox("레이어 타입")
        layer_type_layout = QVBoxLayout()
        
        layer_type_label = QLabel("다운로드할 레이어:")
        self.layer_type_combo = QComboBox()
        
        # Add urban planning layers
        for typename, info in URBAN_PLANNING_LAYERS.items():
            display_name = f"{info['name']} ({typename})"
            self.layer_type_combo.addItem(display_name, typename)
        
        layer_type_layout.addWidget(layer_type_label)
        layer_type_layout.addWidget(self.layer_type_combo)
        
        # Legend button
        self.legend_button = QPushButton("범례 보기")
        self.legend_button.setToolTip("선택한 레이어의 범례를 표시합니다")
        layer_type_layout.addWidget(self.legend_button)
        
        # Layer info display
        self.layer_info_label = QLabel()
        self.layer_info_label.setWordWrap(True)
        self.layer_info_label.setStyleSheet("color: #666; font-size: 10px;")
        layer_type_layout.addWidget(self.layer_info_label)
        
        layer_type_group.setLayout(layer_type_layout)
        layout.addWidget(layer_type_group)
        
        # === Progress Group ===
        progress_group = QGroupBox("진행 상황")
        progress_layout = QVBoxLayout()
        
        self.status_label = QLabel("대기 중...")
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        
        progress_layout.addWidget(self.status_label)
        progress_layout.addWidget(self.progress_bar)
        
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        # === Buttons ===
        button_layout = QHBoxLayout()
        
        self.download_button = QPushButton("다운로드")
        self.download_button.setDefault(True)
        self.download_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        self.close_button = QPushButton("닫기")
        self.close_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        
        # Set main layout
        self.setLayout(layout)
        
        # Update layer info
        self.update_layer_info()

    def connect_signals(self):
        """Connect UI signals to slots."""
        self.extent_type_combo.currentIndexChanged.connect(self.update_layer_controls_state)
        self.layer_combo.currentIndexChanged.connect(self.update_selected_features_state)
        self.layer_type_combo.currentIndexChanged.connect(self.update_layer_info)
        self.legend_button.clicked.connect(self.show_legend)
        self.download_button.clicked.connect(self.download_data)
        self.close_button.clicked.connect(self.reject)

    def populate_layer_combo(self):
        """Populate the layer combo box with available vector layers."""
        self.layer_combo.clear()
        
        # Get all vector layers
        layers = QgsProject.instance().mapLayers().values()
        vector_layers = [layer for layer in layers if isinstance(layer, QgsVectorLayer)]
        
        if not vector_layers:
            self.layer_combo.addItem("(벡터 레이어 없음)", None)
            return
        
        # Add layers to combo
        for layer in vector_layers:
            self.layer_combo.addItem(layer.name(), layer.id())

    def update_layer_controls_state(self):
        """Update enabled state of layer-related controls."""
        extent_type = self.extent_type_combo.currentData()
        
        is_layer_extent = (extent_type == ExtentType.LAYER)
        
        self.layer_label.setEnabled(is_layer_extent)
        self.layer_combo.setEnabled(is_layer_extent)
        self.selected_features_checkbox.setEnabled(is_layer_extent)
        
        if is_layer_extent:
            self.update_selected_features_state()

    def update_selected_features_state(self):
        """Update state of selected features checkbox."""
        layer = self.get_selected_layer()
        
        if layer and layer.selectedFeatureCount() > 0:
            self.selected_features_checkbox.setEnabled(True)
            self.selected_features_checkbox.setText(
                f"선택한 피처만 사용 ({layer.selectedFeatureCount()}개)"
            )
        else:
            self.selected_features_checkbox.setEnabled(False)
            self.selected_features_checkbox.setText("선택한 피처만 사용 (선택된 피처 없음)")
            self.selected_features_checkbox.setChecked(False)

    def update_layer_info(self):
        """Update layer information display."""
        typename = self.layer_type_combo.currentData()
        
        if typename:
            layer_info = get_layer_info(typename)
            if layer_info:
                info_text = f"설명: {layer_info.get('description', 'N/A')}"
                self.layer_info_label.setText(info_text)
            else:
                self.layer_info_label.setText("")
        else:
            self.layer_info_label.setText("")

    def get_selected_layer(self):
        """
        Get the currently selected layer.
        
        :return: Selected layer or None
        :rtype: QgsVectorLayer or None
        """
        layer_id = self.layer_combo.currentData()
        
        if not layer_id:
            return None
        
        return QgsProject.instance().mapLayer(layer_id)

    def show_legend(self):
        """Show legend dialog for the selected layer type."""
        typename = self.layer_type_combo.currentData()
        
        if not typename:
            QMessageBox.warning(
                self,
                "경고",
                "레이어 타입을 선택해주세요."
            )
            return
        
        layer_info = get_layer_info(typename)
        layer_name = layer_info['name'] if layer_info else typename
        
        try:
            # Show legend dialog
            show_legend_dialog(typename, layer_name, self)
            
        except Exception as e:
            LOGGER.exception(f"Error showing legend: {e}")
            QMessageBox.critical(
                self,
                "오류",
                f"범례를 표시하는 중 오류가 발생했습니다:\n{str(e)}"
            )

    def download_data(self):
        """Execute the download process."""
        try:
            # Disable controls during download
            self.download_button.setEnabled(False)
            self.progress_bar.setValue(0)
            self.status_label.setText("다운로드 준비 중...")
            
            # Get extent
            extent_type = self.extent_type_combo.currentData()
            extent = None
            
            if extent_type == ExtentType.CANVAS:
                self.status_label.setText("캔버스 범위 계산 중...")
                extent = self.processor.get_canvas_extent()
                
            elif extent_type == ExtentType.LAYER:
                layer = self.get_selected_layer()
                
                if not layer:
                    QMessageBox.warning(
                        self,
                        "경고",
                        "레이어를 선택해주세요."
                    )
                    return
                
                selected_only = self.selected_features_checkbox.isChecked()
                
                if selected_only and layer.selectedFeatureCount() == 0:
                    QMessageBox.warning(
                        self,
                        "경고",
                        "선택된 피처가 없습니다."
                    )
                    return
                
                self.status_label.setText("레이어 범위 계산 중...")
                extent = self.processor.get_layer_extent(layer, selected_only)
            
            if not extent or extent.isEmpty():
                QMessageBox.critical(
                    self,
                    "오류",
                    "유효한 범위를 가져올 수 없습니다."
                )
                return
            
            self.progress_bar.setValue(20)
            
            # Get layer type
            typename = self.layer_type_combo.currentData()
            layer_info = get_layer_info(typename)
            layer_name = layer_info['name'] if layer_info else typename
            
            # Download data
            self.status_label.setText("VWorld WFS API에서 데이터 다운로드 중...")
            self.progress_bar.setValue(40)
            
            client = VworldWFSClient()
            data_file = client.fetch_data(typename, extent)
            
            if not data_file:
                errors = client.get_errors()
                error_msg = "\n".join(errors) if errors else "알 수 없는 오류"
                
                QMessageBox.critical(
                    self,
                    "다운로드 실패",
                    f"데이터 다운로드에 실패했습니다:\n{error_msg}"
                )
                return
            
            self.progress_bar.setValue(70)
            
            # Create and load layer
            self.status_label.setText("레이어 생성 중...")
            
            layer = self.processor.process_and_load(data_file, layer_name, typename)
            
            if not layer:
                QMessageBox.critical(
                    self,
                    "레이어 생성 실패",
                    "레이어를 생성할 수 없습니다."
                )
                return
            
            self.progress_bar.setValue(100)
            self.status_label.setText(f"완료! {layer.featureCount()}개의 피처를 다운로드했습니다.")
            
            # Show success message
            QMessageBox.information(
                self,
                "성공",
                f"데이터가 성공적으로 다운로드되었습니다!\n\n"
                f"레이어: {layer_name}\n"
                f"피처 수: {layer.featureCount()}"
            )
            
            LOGGER.info(f"Download completed successfully: {layer_name}")
            
        except Exception as e:
            LOGGER.exception(f"Error during download: {e}")
            
            QMessageBox.critical(
                self,
                "오류",
                f"다운로드 중 오류가 발생했습니다:\n{str(e)}"
            )
            
            self.status_label.setText("오류 발생!")
            
        finally:
            # Re-enable controls
            self.download_button.setEnabled(True)

