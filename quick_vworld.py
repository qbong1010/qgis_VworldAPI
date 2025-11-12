"""
Quick Vworld Plugin - Main Entry Point
"""

import logging
import os
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QUrl
from qgis.PyQt.QtGui import QIcon, QDesktopServices
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QPushButton
from qgis.core import Qgis, QgsMessageLog

from .ui.main_dialog import QuickVworldDialog
from .core.utilities import get_setting, set_setting, get_version

LOGGER = logging.getLogger('QuickVworld')


class QuickVworld:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        
        # Initialize locale
        locale = QSettings().value('locale/userLocale', 'en')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'QuickVworld_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr('&Quick Vworld')
        self.toolbar = None
        self.help_action = None

        LOGGER.info('Quick Vworld Plugin initialized')
        QgsMessageLog.logMessage('Quick Vworld Plugin initialized', 'QuickVworld', Qgis.Info)

    def tr(self, message):
        """Get the translation for a string using Qt translation API."""
        return QCoreApplication.translate('QuickVworld', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar."""

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        icon = QIcon(icon_path)
        
        # Add help menu action
        self.help_action = QAction(icon, 'Quick Vworld Help', self.iface.mainWindow())
        self.iface.pluginHelpMenu().addAction(self.help_action)
        self.help_action.triggered.connect(self.show_help)
        
        # Create toolbar
        self.toolbar = self.iface.addToolBar('Quick Vworld')
        self.toolbar.setObjectName('QuickVworld')

        self.add_action(
            icon_path,
            text=self.tr('Download Vworld Data'),
            callback=self.run,
            parent=self.iface.mainWindow(),
            status_tip=self.tr('Download spatial data from Vworld WFS API'),
            whats_this=self.tr('Download spatial data from Vworld WFS API'))

        # Log version info
        version = get_version()
        LOGGER.info(f'Quick Vworld Plugin loaded with version: {version}')
        QgsMessageLog.logMessage(f'Quick Vworld GUI initialized (v{version})', 'QuickVworld', Qgis.Info)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr('&Quick Vworld'),
                action)
            self.iface.removeToolBarIcon(action)
        
        # Remove help menu action
        if self.help_action:
            self.iface.pluginHelpMenu().removeAction(self.help_action)
            del self.help_action
        
        # Remove the toolbar
        if self.toolbar:
            del self.toolbar

        LOGGER.info('Quick Vworld plugin unloaded')

    @staticmethod
    def show_help():
        """Open the help documentation."""
        # Open README.md in the plugin directory or online documentation
        help_url = "https://github.com/quickvworld/qgis-plugin"  # Update with actual URL
        QDesktopServices.openUrl(QUrl(help_url))
        LOGGER.info('Opening help documentation')

    def open_vworld_license_message(self, dialog):
        """
        Display VWorld API license and terms of use message.
        Shows only on first run.
        """
        def read_license():
            """Open VWorld API terms page."""
            QDesktopServices.openUrl(QUrl('https://www.vworld.kr/v4po_prcint_a006.do'))
            set_setting("license_agreed", "true")

        def accept_license():
            """Accept license without reading."""
            set_setting("license_agreed", "true")

        # Check if user has already agreed
        if not get_setting("license_agreed"):
            message = QMessageBox(dialog)
            message.setWindowTitle('VWorld API 사용 약관')
            
            text = self.tr(
                'VWorld Open API는 대한민국 국토교통부에서 제공하는 공간정보 오픈플랫폼입니다.'
            ) + '\n\n'
            text += self.tr('API 사용 시 다음 사항을 준수해야 합니다:') + '\n'
            text += '• ' + self.tr('일일 API 요청 제한 준수') + '\n'
            text += '• ' + self.tr('상업적 이용 시 별도 협의 필요') + '\n\n'
            text += self.tr('자세한 내용은 VWorld 웹사이트를 참조하세요.')
            
            message.setText(text)
            message.setIcon(QMessageBox.Icon.Information)
            
            # Buttons
            accept_button = QPushButton(self.tr('약관에 동의하고 플러그인 사용'), message)
            read_button = QPushButton(self.tr('약관 전문 읽기'), message)
            
            message.addButton(accept_button, QMessageBox.ButtonRole.AcceptRole)
            message.addButton(read_button, QMessageBox.ButtonRole.HelpRole)
            
            read_button.clicked.connect(read_license)
            accept_button.clicked.connect(accept_license)
            
            message.exec()

    def run(self):
        """Run method that performs all the real work"""
        
        # Create the dialog with elements (after translation) and keep reference
        dlg = QuickVworldDialog(self.iface)
        
        # Show license agreement on first run
        self.open_vworld_license_message(dlg)
        
        # Show the dialog
        dlg.show()
        result = dlg.exec_()
        
        if result:
            # User clicked OK
            LOGGER.info('Dialog accepted')

