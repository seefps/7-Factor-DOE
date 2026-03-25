# Creating a Professional Installer

Your DOE Simulator can now be packaged as a professional installer (.exe setup wizard).

## Steps to Create the Installer:

### 1. Download Inno Setup
- Visit: https://jrsoftware.org/isdl.php
- Download and install Inno Setup (free)

### 2. Compile the Installer
- Open Inno Setup Compiler
- Go to File → Open and select `installer.iss` from your project folder
- Click the blue "Compile" button (or press Ctrl+F9)
- Wait for compilation to complete

### 3. Locate Your Installer
The setup file will be created at: `installers\DOE_Simulator_Setup.exe`

## Distributing Your Installer

Users can now:
1. Download `DOE_Simulator_Setup.exe`
2. Double-click to run the installer
3. Choose installation location
4. Click "Install"
5. Application launches automatically

## Customizing the Installer

Edit `installer.iss` to customize:

- **AppVersion**: Update version number (currently 1.0.0)
- **AppPublisher**: Change company/author name
- **AppPublisherURL**: Your website
- **DefaultDirName**: Default installation directory
- **SetupIconFile**: Add custom icon (path to your .ico file)

### Example Changes:

```ini
AppVersion=2.0.0
AppPublisher=Your Company Name
AppPublisherURL=https://yourcompany.com
DefaultDirName={pf}\My Company\DOE Simulator
SetupIconFile=icon.ico
```

## What Gets Installed

- DOE_Simulator.exe (the main application)
- All required libraries (bundled in the exe)
- Shortcuts in Start Menu and (optionally) Desktop
- Uninstall option via Control Panel

## System Requirements

- Windows 10 or later (64-bit)
- ~500MB disk space
- No other dependencies required

## Updating the Installer

After you rebuild the .exe (with `build.bat`):
1. Open `installer.iss` in Inno Setup again
2. Update the AppVersion number
3. Click Compile
4. New installer will be created in `installers\`

## Advanced: Code Signing

For production distribution, you may want to code-sign your installer:
- This prevents Windows SmartScreen warnings
- Requires an SSL certificate
- Add to installer.iss: `SignTool=...` (see Inno Setup documentation)

## Support

- Inno Setup Documentation: https://jrsoftware.org/ishelp/
- Inno Setup Forums: https://jrsoftware.org/forums/
