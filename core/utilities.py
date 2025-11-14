"""
Utility functions for Quick Vworld Plugin
"""

import logging
from qgis.PyQt.QtCore import QSettings

LOGGER = logging.getLogger('QuickVworld')


def get_setting(key, default=None):
    """
    Get a plugin setting value.
    
    :param key: Setting key
    :type key: str
    :param default: Default value if key doesn't exist
    :return: Setting value
    """
    settings = QSettings()
    return settings.value(f'quick_vworld/{key}', default)


def set_setting(key, value):
    """
    Set a plugin setting value.
    
    :param key: Setting key
    :type key: str
    :param value: Setting value
    """
    settings = QSettings()
    settings.setValue(f'quick_vworld/{key}', value)


def get_version():
    """
    Get plugin version from metadata.txt
    
    :return: Version string
    :rtype: str
    """
    import os
    import configparser
    
    metadata_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'metadata.txt')
    
    try:
        config = configparser.ConfigParser()
        config.read(metadata_path, encoding='utf-8')
        return config.get('general', 'version', fallback='unknown')
    except Exception as e:
        LOGGER.error(f"Failed to read version: {e}")
        return 'unknown'

