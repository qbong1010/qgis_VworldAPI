"""
Data Processor for Quick Vworld Plugin

This module handles data processing, coordinate transformation,
and layer creation from downloaded WFS data.
"""

import logging
from qgis.core import (
    QgsVectorLayer,
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsRectangle,
    QgsLayerMetadata,
    QgsMessageLog,
    Qgis
)

from ..definitions.layers import CRS_WGS84, get_layer_info

LOGGER = logging.getLogger('QuickVworld')


class ExtentType:
    """Extent selection types."""
    CANVAS = 'canvas'
    LAYER = 'layer'
    LAYER_SELECTED = 'layer_selected'


class VworldDataProcessor:
    """
    Processor for VWorld WFS data.
    
    Handles coordinate transformation, extent calculation,
    and layer creation.
    """

    def __init__(self, iface):
        """
        Constructor.
        
        :param iface: QGIS interface
        :type iface: QgsInterface
        """
        self.iface = iface

    def get_canvas_extent(self):
        """
        Get the current map canvas extent.
        
        :return: Canvas extent in WGS84 (EPSG:4326)
        :rtype: QgsRectangle
        """
        canvas = self.iface.mapCanvas()
        extent = canvas.extent()
        
        # Get canvas CRS
        canvas_crs = canvas.mapSettings().destinationCrs()
        
        # Transform to WGS84 if needed
        if canvas_crs.authid() != CRS_WGS84:
            wgs84_crs = QgsCoordinateReferenceSystem(CRS_WGS84)
            transform = QgsCoordinateTransform(
                canvas_crs,
                wgs84_crs,
                QgsProject.instance()
            )
            extent = transform.transformBoundingBox(extent)
        
        LOGGER.info(f"Canvas extent (WGS84): {extent.toString()}")
        return extent

    def get_layer_extent(self, layer, selected_only=False):
        """
        Get the extent of a layer or its selected features.
        
        :param layer: Vector layer
        :type layer: QgsVectorLayer
        :param selected_only: Use only selected features
        :type selected_only: bool
        :return: Layer extent in WGS84 (EPSG:4326)
        :rtype: QgsRectangle
        """
        if not layer or not layer.isValid():
            LOGGER.error("Invalid layer provided")
            return None

        # Get extent
        if selected_only and layer.selectedFeatureCount() > 0:
            extent = layer.boundingBoxOfSelected()
            LOGGER.info(f"Using extent of {layer.selectedFeatureCount()} selected features")
        else:
            extent = layer.extent()
            LOGGER.info(f"Using full layer extent")

        # Get layer CRS
        layer_crs = layer.crs()
        
        # Transform to WGS84 if needed
        if layer_crs.authid() != CRS_WGS84:
            wgs84_crs = QgsCoordinateReferenceSystem(CRS_WGS84)
            transform = QgsCoordinateTransform(
                layer_crs,
                wgs84_crs,
                QgsProject.instance()
            )
            extent = transform.transformBoundingBox(extent)
        
        LOGGER.info(f"Layer extent (WGS84): {extent.toString()}")
        return extent

    def create_layer(self, data_file, layer_name, typename):
        """
        Create a vector layer from a data file.
        
        :param data_file: Path to data file (GeoJSON)
        :type data_file: str
        :param layer_name: Name for the new layer
        :type layer_name: str
        :param typename: VWorld layer typename
        :type typename: str
        :return: Created vector layer
        :rtype: QgsVectorLayer
        """
        LOGGER.info(f"Creating layer from file: {data_file}")
        
        # Create vector layer
        layer = QgsVectorLayer(data_file, layer_name, "ogr")
        
        if not layer.isValid():
            LOGGER.error(f"Failed to create valid layer from: {data_file}")
            return None

        # Set encoding
        layer.setProviderEncoding('UTF-8')
        
        # Add metadata
        self._add_metadata(layer, typename)
        
        LOGGER.info(f"Layer created successfully: {layer_name}")
        LOGGER.info(f"Feature count: {layer.featureCount()}")
        LOGGER.info(f"Geometry type: {layer.geometryType()}")
        
        return layer

    def _add_metadata(self, layer, typename):
        """
        Add metadata to the layer.
        
        :param layer: Vector layer
        :type layer: QgsVectorLayer
        :param typename: VWorld layer typename
        :type typename: str
        """
        metadata = QgsLayerMetadata()
        
        # Get layer info
        layer_info = get_layer_info(typename)
        
        if layer_info:
            abstract = f"{layer_info.get('name', '')} - {layer_info.get('description', '')}"
            metadata.setAbstract(abstract)
            metadata.setTitle(layer_info.get('name', typename))
        
        # Add rights and license
        metadata.setRights(['© VWorld Open API'])
        metadata.setLicenses(['VWorld Open API License'])
        
        # Add keywords
        keywords = ['VWorld', 'WFS', 'Korea', typename]
        if layer_info:
            category = layer_info.get('category', '')
            if category:
                keywords.append(category)
        metadata.setKeywords({'keywords': keywords})
        
        layer.setMetadata(metadata)

    def add_layer_to_project(self, layer, add_to_legend=True):
        """
        Add layer to the QGIS project.
        
        :param layer: Vector layer to add
        :type layer: QgsVectorLayer
        :param add_to_legend: Add to legend (default: True)
        :type add_to_legend: bool
        :return: True if successful
        :rtype: bool
        """
        if not layer or not layer.isValid():
            LOGGER.error("Cannot add invalid layer to project")
            return False

        # Add to project
        QgsProject.instance().addMapLayer(layer, add_to_legend)
        
        LOGGER.info(f"Layer added to project: {layer.name()}")
        
        # Show message in QGIS message bar
        self.iface.messageBar().pushMessage(
            "Quick Vworld",
            f"레이어가 추가되었습니다: {layer.name()} ({layer.featureCount()} features)",
            level=Qgis.Success,
            duration=5
        )
        
        return True

    def process_and_load(self, data_file, layer_name, typename):
        """
        Complete workflow: create layer and add to project.
        
        :param data_file: Path to data file
        :type data_file: str
        :param layer_name: Name for the layer
        :type layer_name: str
        :param typename: VWorld layer typename
        :type typename: str
        :return: Created layer if successful, None otherwise
        :rtype: QgsVectorLayer or None
        """
        try:
            # Create layer
            layer = self.create_layer(data_file, layer_name, typename)
            
            if not layer:
                return None
            
            # Add to project
            success = self.add_layer_to_project(layer)
            
            if not success:
                return None
            
            return layer
            
        except Exception as e:
            LOGGER.exception(f"Error processing and loading data: {e}")
            
            # Show error message
            self.iface.messageBar().pushMessage(
                "Quick Vworld",
                f"레이어 생성 중 오류 발생: {str(e)}",
                level=Qgis.Critical,
                duration=10
            )
            
            return None


def get_extent_for_download(iface, extent_type, layer=None, selected_only=False):
    """
    Helper function to get extent based on extent type.
    
    :param iface: QGIS interface
    :type iface: QgsInterface
    :param extent_type: Type of extent (canvas, layer, layer_selected)
    :type extent_type: str
    :param layer: Layer (required if extent_type is layer-based)
    :type layer: QgsVectorLayer
    :param selected_only: Use selected features only
    :type selected_only: bool
    :return: Extent in WGS84
    :rtype: QgsRectangle or None
    """
    processor = VworldDataProcessor(iface)
    
    if extent_type == ExtentType.CANVAS:
        return processor.get_canvas_extent()
    
    elif extent_type in [ExtentType.LAYER, ExtentType.LAYER_SELECTED]:
        if not layer:
            LOGGER.error("Layer is required for layer extent type")
            return None
        return processor.get_layer_extent(layer, selected_only)
    
    else:
        LOGGER.error(f"Unknown extent type: {extent_type}")
        return None

