# Changelog

All notable changes to the Flight Track Viewer project will be documented in this file.

## [1.0.1] - 2026-02-05

### Fixed
- **UI/UX Improvements:**
  - Moved "Process Flight Data" button to header (no longer floating)
  - Button is now grayed out until CSV file is selected
  - Button stays in place and doesn't move when file is selected
  
- **CSV Parsing:**
  - Added auto-detection for comma-separated and tab-separated CSV files
  - Fixed parsing of quoted Position values (e.g., "42.187,-71.176")
  - Now handles both FlightRadar24 export formats correctly
  
- **Image Export:**
  - Implemented proper map saving using html2canvas library
  - Removed error popup when saving charts (errors now logged silently)
  - Added visual feedback (green checkmark) when images save successfully
  - Map images now save at 2x resolution for better quality

### Added
- html2canvas dependency for high-quality map screenshots
- Better user feedback during save operations (loading states, success indicators)
- Support for both comma and tab-separated CSV formats

### Changed
- Process button moved from floating to header for better UX
- Save operations now show temporary success states
- Error handling improved to not interrupt user workflow

## [1.0.0] - 2026-02-05

### Added
- Initial release
- Interactive flight path visualization on OpenStreetMap
- Real-time animation with speed controls (0.25x to 10x)
- Three interactive charts (Altitude, Speed, Distance from start)
- Python FastAPI backend for flight calculations
- Electron desktop application
- CSV file import from FlightRadar24
- Image export for maps and charts
- Flight statistics dashboard
- Dark modern UI design

### Features
- Automatic heading calculations using bearing formula
- Distance calculations using Haversine formula
- Rotating airplane marker based on flight heading
- Progress slider for scrubbing through flight
- Zoom and pan controls on map
- Responsive layout

---

## Version Guidelines

- **MAJOR**: Breaking changes to CSV format or API
- **MINOR**: New features, significant enhancements
- **PATCH**: Bug fixes, UI improvements, minor updates
