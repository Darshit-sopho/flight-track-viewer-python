# Deployment & Distribution Guide

## Building the Application

### Prerequisites for Building

1. **Node.js** (v16+) with npm
2. **Python** (3.8+)
3. **Platform-specific tools:**
   - Windows: Windows SDK, Visual Studio Build Tools
   - macOS: Xcode Command Line Tools
   - Linux: Standard build tools (gcc, make)

### Build Process

#### 1. Prepare the Project

```bash
# Install all dependencies
npm install

# Install Python dependencies
cd backend
pip install -r requirements.txt
cd ..
```

#### 2. Build for Your Platform

```bash
# Build for current platform
npm run build

# Output will be in dist/ folder
```

#### 3. Platform-Specific Builds

**Windows (.exe installer):**
```bash
npm run build -- --win
```
Output: `dist/Flight-Track-Viewer-Setup-1.0.0.exe`

**macOS (.dmg):**
```bash
npm run build -- --mac
```
Output: `dist/Flight-Track-Viewer-1.0.0.dmg`

**Linux (AppImage):**
```bash
npm run build -- --linux
```
Output: `dist/Flight-Track-Viewer-1.0.0.AppImage`

### Multi-Platform Builds

To build for all platforms (requires appropriate OS):

```bash
npm run build -- --win --mac --linux
```

## Distribution

### Windows Distribution

**Installer (.exe):**
- Users double-click to install
- Installs to Program Files
- Creates desktop shortcut
- Adds to Start Menu

**Portable (.zip):**
- No installation required
- Extract and run
- Good for USB drives

### macOS Distribution

**DMG File:**
- Users drag to Applications folder
- Standard macOS installation
- Code signing recommended for Gatekeeper

**App Bundle:**
- Standalone .app file
- Can be distributed directly
- Requires notarization for macOS 10.15+

### Linux Distribution

**AppImage:**
- Single executable file
- Works on most distributions
- No installation needed
- Make executable: `chmod +x Flight-Track-Viewer.AppImage`

**Snap/Flatpak:**
- Can be packaged for snap/flatpak stores
- Requires additional configuration

## Code Signing (Recommended)

### Windows Code Signing

```bash
# In package.json, add:
"build": {
  "win": {
    "certificateFile": "path/to/cert.pfx",
    "certificatePassword": "password"
  }
}
```

### macOS Code Signing

```bash
# In package.json, add:
"build": {
  "mac": {
    "identity": "Developer ID Application: Your Name",
    "hardenedRuntime": true,
    "gatekeeperAssess": false,
    "entitlements": "entitlements.mac.plist"
  }
}
```

### Notarization (macOS)

After building:
```bash
xcrun altool --notarize-app \
  --primary-bundle-id "com.flighttrack.viewer" \
  --username "your@email.com" \
  --password "app-specific-password" \
  --file "dist/Flight-Track-Viewer-1.0.0.dmg"
```

## Auto-Updates (Optional)

### Using electron-updater

1. Install dependency:
```bash
npm install electron-updater
```

2. Configure in main.js:
```javascript
const { autoUpdater } = require('electron-updater');

app.on('ready', () => {
  autoUpdater.checkForUpdatesAndNotify();
});
```

3. Host updates on:
   - GitHub Releases
   - Amazon S3
   - Custom server

## Python Backend Packaging

The Python backend needs to be included in the distribution:

### Option 1: Include Python (Recommended)
- Bundle Python interpreter with app
- Use PyInstaller to create standalone executable
- Increases app size but ensures compatibility

### Option 2: System Python
- Rely on user's installed Python
- Smaller app size
- May have compatibility issues

### Creating Python Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
cd backend
pyinstaller --onefile --name flight-backend main.py

# Executable will be in dist/flight-backend
```

Then modify `main.js` to use the bundled executable:

```javascript
const pythonExe = path.join(
  __dirname,
  'resources',
  'flight-backend' + (process.platform === 'win32' ? '.exe' : '')
);

pythonProcess = spawn(pythonExe);
```

## File Structure for Distribution

```
Flight-Track-Viewer/
├── Flight-Track-Viewer.exe (or .app, .AppImage)
├── resources/
│   ├── app.asar                  # Packaged Electron app
│   ├── flight-backend.exe        # Python backend (optional)
│   └── assets/
│       └── icon.png
└── (platform-specific files)
```

## Testing the Build

### Pre-Distribution Checklist

- [ ] Test installation on clean system
- [ ] Verify Python backend starts correctly
- [ ] Check all features work
- [ ] Test file upload/download
- [ ] Verify charts render properly
- [ ] Test animation controls
- [ ] Check for console errors
- [ ] Verify app icon displays
- [ ] Test on different screen sizes
- [ ] Check memory usage
- [ ] Verify proper shutdown

### Automated Testing

Create test script:

```javascript
// test.js
const { app } = require('electron');
const assert = require('assert');

// Test 1: Backend starts
async function testBackendStart() {
  // Wait for backend
  await new Promise(r => setTimeout(r, 3000));
  
  const response = await fetch('http://127.0.0.1:8000/health');
  const data = await response.json();
  assert.strictEqual(data.status, 'healthy');
}

// Run tests
testBackendStart()
  .then(() => console.log('✓ All tests passed'))
  .catch(err => console.error('✗ Tests failed:', err));
```

## Distribution Channels

### Direct Distribution
- Host on your website
- Provide download links
- Include SHA256 checksums

### GitHub Releases
- Automatic version management
- Built-in download hosting
- Update notifications

### App Stores

**Microsoft Store (Windows):**
- Requires developer account ($19/year)
- Desktop Bridge for Win32 apps
- Better user trust

**Mac App Store:**
- Requires Apple Developer account ($99/year)
- Strict sandboxing requirements
- May require app modifications

**Snap Store (Linux):**
- Free distribution
- Wide Linux compatibility
- Automatic updates

## Version Management

### Semantic Versioning

Follow semver: `MAJOR.MINOR.PATCH`

```json
// package.json
{
  "version": "1.0.0"
}
```

### Changelog

Maintain CHANGELOG.md:

```markdown
# Changelog

## [1.0.0] - 2026-02-05
### Added
- Initial release
- Flight path visualization
- Altitude/Speed charts
- Animation controls

## [1.0.1] - 2026-02-15
### Fixed
- Map rendering on high-DPI displays
- CSV parsing edge cases
```

## Analytics (Optional)

### Usage Tracking

```javascript
// In renderer.js
const { ipcRenderer } = require('electron');

function trackEvent(category, action) {
  ipcRenderer.send('track-event', { category, action });
}

// Example usage
trackEvent('file', 'upload');
trackEvent('animation', 'play');
```

### Privacy Considerations
- Only track anonymous usage
- No personal data
- Make it opt-in
- Comply with GDPR/privacy laws

## Support & Updates

### Documentation
- README.md - Getting started
- QUICKSTART.md - Quick reference
- PROJECT_STRUCTURE.md - Technical details
- This file - Deployment

### Issue Tracking
- GitHub Issues for bug reports
- Feature request template
- Bug report template

### Update Strategy
1. **Patch releases** (1.0.x) - Bug fixes, weekly
2. **Minor releases** (1.x.0) - New features, monthly
3. **Major releases** (x.0.0) - Breaking changes, yearly

## Troubleshooting Distribution

### Common Issues

**"Application can't be opened" (macOS)**
- Solution: Code sign and notarize

**"Windows protected your PC"**
- Solution: Code sign with EV certificate

**AppImage won't run (Linux)**
- Solution: `chmod +x` and check FUSE

**Backend doesn't start**
- Solution: Bundle Python or check system Python

**Large file size**
- Solution: Use asar archives, exclude devDependencies

### Size Optimization

```json
// package.json
{
  "build": {
    "asar": true,
    "compression": "maximum",
    "files": [
      "!**/*.map",
      "!**/.git*",
      "!**/test/**"
    ]
  }
}
```

## License Compliance

Ensure compliance with:
- Electron (MIT)
- Leaflet (BSD-2-Clause)
- Chart.js (MIT)
- FastAPI (MIT)
- Python libraries (various)

Include LICENSE file with all attributions.

---

**Ready to distribute?** Follow this checklist:
1. ✅ All tests pass
2. ✅ Documentation complete
3. ✅ Version number updated
4. ✅ Changelog updated
5. ✅ Code signed (if applicable)
6. ✅ Tested on clean system
7. ✅ Release notes prepared
8. 🚀 **Ship it!**
