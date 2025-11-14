"""
VWorld WFS API Client

This module provides a client for accessing VWorld WFS API
to download spatial data.
"""

import logging
import os
from qgis.PyQt.QtCore import QDir, QFileInfo, QTemporaryFile, QUrlQuery
from qgis.core import QgsRectangle

from .downloader import Downloader
from ...definitions.layers import (
    VWORLD_WFS_URL,
    DEFAULT_API_KEY,
    WFS_VERSION,
    WFS_SERVICE,
    WFS_REQUEST,
    CRS_WGS84,
    OUTPUT_FORMAT_JSON,
    DEFAULT_MAX_FEATURES
)

LOGGER = logging.getLogger('QuickVworld')


class VworldWFSClient(Downloader):
    """
    VWorld WFS API Client.
    
    This client handles WFS GetFeature requests to VWorld API
    and downloads the result to a temporary GeoJSON file.
    """

    def __init__(self, api_key=None):
        """
        Constructor.
        
        :param api_key: VWorld API key (uses default if not provided)
        :type api_key: str
        """
        super().__init__()
        
        self.api_key = api_key or DEFAULT_API_KEY
        self._typename = None
        self._bbox = None
        self._srsname = CRS_WGS84
        self._max_features = DEFAULT_MAX_FEATURES
        self._last_request_url = None  # Store last request URL
        
        # Create temporary file for result
        self._create_temp_file()

    def _create_temp_file(self):
        """Create a temporary file for storing downloaded data."""
        temp_file = QTemporaryFile(
            os.path.join(QDir.tempPath(), 'quickvworld-XXXXXX.geojson')
        )
        temp_file.setAutoRemove(False)  # Don't auto-remove, we'll manage it
        temp_file.open()
        self.result_path = temp_file.fileName()
        temp_file.close()
        
        LOGGER.info(f"Created temporary file: {self.result_path}")

    def set_typename(self, typename):
        """
        Set the WFS typename (layer name).
        
        :param typename: Layer typename (e.g., 'lt_c_upisuq153')
        :type typename: str
        """
        self._typename = typename

    def set_bbox(self, bbox):
        """
        Set the bounding box for the request.
        
        Note: VWorld WFS API with EPSG:4326 expects BBOX in format:
        ymin,xmin,ymax,xmax (lat/lon order, not lon/lat!)
        
        :param bbox: Bounding box (QgsRectangle or string)
        :type bbox: QgsRectangle or str
        """
        if isinstance(bbox, QgsRectangle):
            # Convert QgsRectangle to string
            # VWorld API expects: ymin,xmin,ymax,xmax for EPSG:4326
            self._bbox = f"{bbox.yMinimum()},{bbox.xMinimum()},{bbox.yMaximum()},{bbox.xMaximum()}"
        else:
            self._bbox = str(bbox)

    def set_srsname(self, srsname):
        """
        Set the spatial reference system.
        
        :param srsname: SRS name (e.g., 'EPSG:4326')
        :type srsname: str
        """
        self._srsname = srsname

    def set_max_features(self, max_features):
        """
        Set maximum number of features to retrieve.
        
        :param max_features: Maximum features (max 1000)
        :type max_features: int
        """
        self._max_features = min(max_features, 1000)

    def get_last_request_url(self):
        """
        Get the last request URL that was used.
        
        :return: Last request URL or None
        :rtype: str or None
        """
        return self._last_request_url

    def build_url(self):
        """
        Build the WFS GetFeature URL with parameters.
        
        :return: Complete URL with query parameters
        :rtype: str
        """
        if not self._typename:
            raise ValueError("Typename must be set before building URL")

        # Build query parameters
        query = QUrlQuery()
        query.addQueryItem('SERVICE', WFS_SERVICE)
        query.addQueryItem('VERSION', WFS_VERSION)
        query.addQueryItem('REQUEST', WFS_REQUEST)
        query.addQueryItem('TYPENAME', self._typename)
        query.addQueryItem('SRSNAME', self._srsname)
        query.addQueryItem('OUTPUT', OUTPUT_FORMAT_JSON)
        query.addQueryItem('KEY', self.api_key)
        
        # Add optional parameters
        if self._bbox:
            query.addQueryItem('BBOX', self._bbox)
        
        if self._max_features:
            query.addQueryItem('MAXFEATURES', str(self._max_features))

        # Build full URL
        from qgis.PyQt.QtCore import QUrl
        url = QUrl(VWORLD_WFS_URL)
        url.setQuery(query)
        
        return url.toString()

    def fetch_data(self, typename, bbox=None, srsname=CRS_WGS84, max_features=None):
        """
        Fetch data from VWorld WFS API.
        
        :param typename: Layer typename (e.g., 'lt_c_upisuq153')
        :type typename: str
        :param bbox: Bounding box (QgsRectangle or string)
        :type bbox: QgsRectangle or str
        :param srsname: Spatial reference system (default: EPSG:4326)
        :type srsname: str
        :param max_features: Maximum features to retrieve
        :type max_features: int
        :return: Path to downloaded file if successful, None otherwise
        :rtype: str or None
        """
        # Set parameters
        self.set_typename(typename)
        
        if bbox:
            self.set_bbox(bbox)
        
        self.set_srsname(srsname)
        
        if max_features:
            self.set_max_features(max_features)

        # Build URL
        try:
            url = self.build_url()
            self._last_request_url = url  # Store the request URL
            self.set_url(url)
            
            LOGGER.info(f"Fetching data from VWorld WFS API")
            LOGGER.info(f"Typename: {typename}")
            LOGGER.info(f"BBOX: {self._bbox}")
            LOGGER.info(f"URL: {url}")
            
        except Exception as e:
            LOGGER.error(f"Error building URL: {e}")
            return None

        # Download data
        success = self.download_sync()
        
        if not success:
            LOGGER.error(f"Failed to download data: {self.get_errors()}")
            return None

        # Verify file exists and has content
        file_info = QFileInfo(self.result_path)
        if not file_info.exists():
            LOGGER.error(f"Downloaded file does not exist: {self.result_path}")
            return None
            
        if file_info.size() == 0:
            LOGGER.error(f"Downloaded file is empty: {self.result_path}")
            return None
            
        LOGGER.info(f"Successfully downloaded data to: {self.result_path} ({file_info.size()} bytes)")
        return self.result_path


def build_wfs_url(typename, bbox=None, api_key=None, srsname=CRS_WGS84, max_features=None):
    """
    Helper function to build a VWorld WFS GetFeature URL.
    
    :param typename: Layer typename
    :type typename: str
    :param bbox: Bounding box (QgsRectangle or string)
    :type bbox: QgsRectangle or str
    :param api_key: API key (uses default if not provided)
    :type api_key: str
    :param srsname: Spatial reference system
    :type srsname: str
    :param max_features: Maximum features to retrieve
    :type max_features: int
    :return: Complete WFS URL
    :rtype: str
    """
    client = VworldWFSClient(api_key)
    client.set_typename(typename)
    
    if bbox:
        client.set_bbox(bbox)
    
    client.set_srsname(srsname)
    
    if max_features:
        client.set_max_features(max_features)
    
    return client.build_url()

