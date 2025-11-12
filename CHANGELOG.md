# Changelog

All notable changes to Quick Vworld Plugin will be documented in this file.

## [1.0.0] - 2025-11-12

### Added
- Initial release
- Canvas extent selection for data download
- Layer extent selection for data download
- Selected features support
- Urban planning facility layer (lt_c_upisuq153) support
- VWorld WFS API integration
- Automatic coordinate transformation (any CRS to EPSG:4326)
- Progress bar and status messages
- Error handling with user-friendly messages
- VWorld API license agreement dialog (first run only)
- Help menu integration
- Version logging
- Settings persistence using QSettings

### Features
- **Extent Selection**:
  - Canvas extent: Download data for current map view
  - Layer extent: Use selected layer's boundary
  - Selected features: Use only selected features' extent

- **UI Components**:
  - Intuitive dialog interface
  - Dynamic control enable/disable based on selection
  - Real-time selected feature count display
  - Progress bar with status messages

- **Data Processing**:
  - Automatic coordinate system transformation
  - GeoJSON format support
  - Metadata addition (license, rights, keywords)
  - Layer styling (default QGIS styling)

- **Legal Compliance**:
  - VWorld API license notification on first run
  - Terms of use display with link to official documentation
  - User agreement tracking (shows only once)

### Technical Details
- QGIS minimum version: 3.22
- Python 3.x compatible
- Uses QgsFileDownloader for synchronous HTTP requests
- Implements QgsCoordinateTransform for CRS handling
- QSettings for persistent configuration

### Documentation
- README.md: User guide
- TESTING.md: Testing guide
- IMPLEMENTATION_SUMMARY.md: Implementation details
- CHANGELOG.md: This file

---

## Future Enhancements (Planned)

### Version 1.1.0
- [ ] Additional urban planning layers support
- [ ] Custom API key configuration
- [ ] Export options (GeoPackage, Shapefile)
- [ ] Batch download for multiple layers

### Version 1.2.0
- [ ] QGIS Processing algorithm integration
- [ ] Advanced filtering options
- [ ] Style templates for different layer types
- [ ] Multi-language support (English, Korean)

### Version 2.0.0
- [ ] WMS service support
- [ ] Search API integration
- [ ] Geocoding features
- [ ] Project templates

---

## Contributing

Please report bugs or suggest features through GitHub issues.

## License

GPL version 3

VWorld data: © Ministry of Land, Infrastructure and Transport, Republic of Korea

