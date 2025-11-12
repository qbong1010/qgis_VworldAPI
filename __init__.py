"""
Quick Vworld Plugin
"""

__copyright__ = 'Copyright 2025, Quick Vworld'
__license__ = 'GPL version 3'
__email__ = 'quickvworld@example.com'
__revision__ = '$Format:%H$'


def classFactory(iface):
    """Load QuickVworld class from file quick_vworld.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .quick_vworld import QuickVworld
    return QuickVworld(iface)

