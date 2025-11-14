"""
VWorld Legend API Client

이 모듈은 VWorld Image API의 GetLegendGraphic 요청을 처리하여
레이어의 범례 이미지를 다운로드합니다.
"""

import logging
import os
from qgis.PyQt.QtCore import QDir, QTemporaryFile, QUrlQuery, QUrl
from qgis.PyQt.QtGui import QPixmap

from .downloader import Downloader
from ...definitions.layers import DEFAULT_API_KEY

LOGGER = logging.getLogger('QuickVworld')

# Legend API 기본 URL
LEGEND_API_URL = "https://api.vworld.kr/req/image"


class VworldLegendClient(Downloader):
    """
    VWorld Legend API Client.
    
    이 클라이언트는 GetLegendGraphic 요청을 처리하여
    레이어의 범례 이미지를 다운로드합니다.
    """

    def __init__(self, api_key=None):
        """
        Constructor.
        
        :param api_key: VWorld API key (uses default if not provided)
        :type api_key: str
        """
        super().__init__()
        
        self.api_key = api_key or DEFAULT_API_KEY
        self._layer = None
        self._style = None
        self._type = 'ALL'  # ALL, POINT, LINE, POLYGON
        self._format = 'png'
        
        # Create temporary file for result
        self._create_temp_file()

    def _create_temp_file(self):
        """Create a temporary file for storing downloaded legend image."""
        temp_file = QTemporaryFile(
            os.path.join(QDir.tempPath(), 'quickvworld-legend-XXXXXX.png')
        )
        temp_file.setAutoRemove(False)  # Don't auto-remove, we'll manage it
        temp_file.open()
        self.result_path = temp_file.fileName()
        temp_file.close()
        
        LOGGER.debug(f"Created temporary legend file: {self.result_path}")

    def set_layer(self, layer):
        """
        Set the layer name.
        
        :param layer: Layer name (e.g., 'lt_c_upisuq153')
        :type layer: str
        """
        self._layer = layer

    def set_style(self, style):
        """
        Set the style name.
        
        :param style: Style name (usually same as layer name)
        :type style: str
        """
        self._style = style

    def set_type(self, legend_type):
        """
        Set the legend type.
        
        :param legend_type: Legend type (ALL, POINT, LINE, POLYGON)
        :type legend_type: str
        """
        if legend_type.upper() in ['ALL', 'POINT', 'LINE', 'POLYGON']:
            self._type = legend_type.upper()
        else:
            LOGGER.warning(f"Invalid legend type: {legend_type}, using ALL")
            self._type = 'ALL'

    def build_url(self):
        """
        Build the GetLegendGraphic URL with parameters.
        
        :return: Complete URL with query parameters
        :rtype: str
        """
        if not self._layer:
            raise ValueError("Layer must be set before building URL")
        
        # Style defaults to layer name if not set
        style = self._style or self._layer

        # Build query parameters
        query = QUrlQuery()
        query.addQueryItem('service', 'image')
        query.addQueryItem('request', 'GetLegendGraphic')
        query.addQueryItem('format', self._format)
        query.addQueryItem('layer', self._layer)
        query.addQueryItem('style', style)
        query.addQueryItem('type', self._type)
        query.addQueryItem('key', self.api_key)

        # Build full URL
        url = QUrl(LEGEND_API_URL)
        url.setQuery(query)
        
        return url.toString()

    def fetch_legend(self, layer, style=None, legend_type='ALL'):
        """
        Fetch legend image from VWorld API.
        
        :param layer: Layer name (e.g., 'lt_c_upisuq153')
        :type layer: str
        :param style: Style name (defaults to layer name)
        :type style: str
        :param legend_type: Legend type (ALL, POINT, LINE, POLYGON)
        :type legend_type: str
        :return: Path to downloaded file if successful, None otherwise
        :rtype: str or None
        """
        # Set parameters
        self.set_layer(layer)
        
        if style:
            self.set_style(style)
        
        self.set_type(legend_type)

        # Build URL
        try:
            url = self.build_url()
            self.set_url(url)
            
            LOGGER.info(f"Fetching legend from VWorld API")
            LOGGER.info(f"Layer: {layer}")
            LOGGER.info(f"Style: {style or layer}")
            LOGGER.info(f"Type: {legend_type}")
            LOGGER.debug(f"URL: {url}")
            
        except Exception as e:
            LOGGER.error(f"Error building legend URL: {e}")
            return None

        # Download legend
        success = self.download_sync()
        
        if not success:
            LOGGER.error(f"Failed to download legend: {self.get_errors()}")
            return None

        # Verify file exists and has content
        if not os.path.exists(self.result_path):
            LOGGER.error(f"Downloaded legend file does not exist: {self.result_path}")
            return None
            
        if os.path.getsize(self.result_path) == 0:
            LOGGER.error(f"Downloaded legend file is empty: {self.result_path}")
            return None
            
        LOGGER.info(f"Successfully downloaded legend to: {self.result_path} "
                   f"({os.path.getsize(self.result_path)} bytes)")
        return self.result_path

    def fetch_legend_as_pixmap(self, layer, style=None, legend_type='ALL'):
        """
        Fetch legend image and return as QPixmap.
        
        :param layer: Layer name
        :type layer: str
        :param style: Style name
        :type style: str
        :param legend_type: Legend type
        :type legend_type: str
        :return: QPixmap with legend image, or None if failed
        :rtype: QPixmap or None
        """
        file_path = self.fetch_legend(layer, style, legend_type)
        
        if not file_path:
            return None
        
        pixmap = QPixmap(file_path)
        
        if pixmap.isNull():
            LOGGER.error(f"Failed to load legend image as pixmap: {file_path}")
            return None
        
        return pixmap


def get_legend_url(layer, style=None, legend_type='ALL', api_key=None):
    """
    Helper function to build a VWorld GetLegendGraphic URL.
    
    :param layer: Layer name
    :type layer: str
    :param style: Style name (defaults to layer name)
    :type style: str
    :param legend_type: Legend type (ALL, POINT, LINE, POLYGON)
    :type legend_type: str
    :param api_key: API key (uses default if not provided)
    :type api_key: str
    :return: Complete legend URL
    :rtype: str
    """
    client = VworldLegendClient(api_key)
    client.set_layer(layer)
    
    if style:
        client.set_style(style)
    
    client.set_type(legend_type)
    
    return client.build_url()


def download_legend(layer, style=None, legend_type='ALL', api_key=None):
    """
    Helper function to download a legend image.
    
    :param layer: Layer name
    :type layer: str
    :param style: Style name
    :type style: str
    :param legend_type: Legend type
    :type legend_type: str
    :param api_key: API key
    :type api_key: str
    :return: Path to downloaded file, or None if failed
    :rtype: str or None
    """
    client = VworldLegendClient(api_key)
    return client.fetch_legend(layer, style, legend_type)


def download_legend_pixmap(layer, style=None, legend_type='ALL', api_key=None):
    """
    Helper function to download a legend image as QPixmap.
    
    :param layer: Layer name
    :type layer: str
    :param style: Style name
    :type style: str
    :param legend_type: Legend type
    :type legend_type: str
    :param api_key: API key
    :type api_key: str
    :return: QPixmap or None if failed
    :rtype: QPixmap or None
    """
    client = VworldLegendClient(api_key)
    return client.fetch_legend_as_pixmap(layer, style, legend_type)

