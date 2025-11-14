"""
VWorld Layer Definitions

This module contains definitions for VWorld WFS layers,
focusing on urban planning related layers.
"""

# VWorld API Base URL
VWORLD_WFS_URL = "https://api.vworld.kr/req/wfs"

# API Key (from documentation)
DEFAULT_API_KEY = "82E0F346-3308-3E16-AD90-3E36EB0A6895"

# Urban Planning Layers
# Source: VWORLD_API_DOCUMENT.md - 도시계획 카테고리 (12종)
URBAN_PLANNING_LAYERS = {
    'lt_c_upisuq153': {
        'name': '도시계획시설(공간시설)',
        'name_en': 'Urban Planning Facility (Space Facility)',
        'category': 'urban_planning',
        'description': '도시계획시설 중 공간시설 레이어',
        'geometry_type': 'Polygon'
    },
    'lt_c_lhblpn': {
        'name': '토지이용계획도',
        'name_en': 'Land Use Plan',
        'category': 'urban_planning',
        'description': '토지이용계획도 레이어',
        'geometry_type': 'Polygon'
    },
    'lt_c_upisuq161': {
        'name': '지구단위계획',
        'name_en': 'District Unit Plan',
        'category': 'urban_planning',
        'description': '지구단위계획 레이어',
        'geometry_type': 'Polygon'
    },
    'lt_c_upisuq151': {
        'name': '도시계획시설(도로)',
        'name_en': 'Urban Planning Facility (Road)',
        'category': 'urban_planning',
        'description': '도시계획시설 중 도로시설',
        'geometry_type': 'Polygon'
    },
    'lt_c_upisuq152': {
        'name': '도시계획시설(교통시설)',
        'name_en': 'Urban Planning Facility (Transportation)',
        'category': 'urban_planning',
        'description': '도시계획시설 중 교통시설',
        'geometry_type': 'Polygon'
    },
}

# Additional useful layers from documentation
ADDITIONAL_LAYERS = {
    'lt_c_aisresc': {
        'name': '건물',
        'name_en': 'Buildings',
        'category': 'administration',
        'description': '건축물대장 정보',
        'geometry_type': 'Polygon'
    },
    'lt_c_ademd_info': {
        'name': '행정동',
        'name_en': 'Administrative Dong',
        'category': 'boundary',
        'description': '행정구역 읍면동',
        'geometry_type': 'Polygon'
    },
    'lt_c_adsigg_info': {
        'name': '시군구',
        'name_en': 'Si/Gun/Gu',
        'category': 'boundary',
        'description': '행정구역 시군구',
        'geometry_type': 'Polygon'
    },
    'lp_pa_cbnd_bubun': {
        'name': '연속지적도',
        'name_en': 'Continuous Cadastral Map',
        'category': 'land',
        'description': '연속지적도(부분) 레이어',
        'geometry_type': 'Polygon'
    },
}

# WFS request parameters
WFS_VERSION = '1.1.0'
WFS_SERVICE = 'WFS'
WFS_REQUEST = 'GetFeature'

# Coordinate systems
CRS_WGS84 = 'EPSG:4326'
CRS_GOOGLE_MERCATOR = 'EPSG:3857'
CRS_KOREA_2000_CENTRAL = 'EPSG:5186'

# Output formats
OUTPUT_FORMAT_JSON = 'application/json'
OUTPUT_FORMAT_GML2 = 'GML2'
OUTPUT_FORMAT_GML3 = 'GML3'

# API limits
MAX_FEATURES = 1000
DEFAULT_MAX_FEATURES = 1000


def get_layer_info(typename):
    """
    Get layer information by typename.
    
    :param typename: Layer typename (e.g., 'lt_c_upisuq153')
    :return: Layer information dict or None
    """
    if typename in URBAN_PLANNING_LAYERS:
        return URBAN_PLANNING_LAYERS[typename]
    elif typename in ADDITIONAL_LAYERS:
        return ADDITIONAL_LAYERS[typename]
    return None


def get_all_layers():
    """
    Get all available layers.
    
    :return: Combined dict of all layers
    """
    all_layers = {}
    all_layers.update(URBAN_PLANNING_LAYERS)
    all_layers.update(ADDITIONAL_LAYERS)
    return all_layers


def get_layers_by_category(category):
    """
    Get layers filtered by category.
    
    :param category: Category name (e.g., 'urban_planning')
    :return: Dict of layers in the category
    """
    all_layers = get_all_layers()
    return {
        typename: info 
        for typename, info in all_layers.items() 
        if info.get('category') == category
    }

