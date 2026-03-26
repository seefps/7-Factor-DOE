# Building DOE Simulator as an Executable

This guide explains how to create a standalone .exe executable that can be installed and run on any Windows computer.

## Prerequisites

- Python 3.8 or higher installed
- All dependencies listed in `requirements.txt` installed

## Quick Build (Recommended)

1. Open Command Prompt or PowerShell in this project directory
2. Run:
   ```bash
   build.bat
   ```
3. The executable will be created at `dist\DOE_Simulator.exe`

## Manual Build

If the batch file doesn't work, you can build manually:

```bash
python -m pip install pyinstaller
pyinstaller doe_simulator.spec
```

## Running the Executable

After building, you can run the application in two ways:

### Option 1: Command Line
```bash
.\dist\DOE_Simulator.exe
```

### Option 2: Double-click
Simply double-click `dist\DOE_Simulator.exe` to run

A command window will appear with the Streamlit server running, and your default browser will open to the application.

## Creating an Installer (Optional)

To create a professional installer, you can use **Inno Setup**:

1. Download and install [Inno Setup](https://jrsoftware.org/isdl.php)
2. Create a file named `installer.iss` with the installer configuration (see example below)
3. Open `installer.iss` with Inno Setup and compile it
4. This creates a setup .exe that users can run to install your application

### Example Inno Setup Configuration (installer.iss)

```ini
[Setup]
AppName=DOE Simulator
AppVersion=1.0
DefaultDirName={pf}\DOE Simulator
DefaultGroupName=DOE Simulator
OutputDir=.\installers
OutputBaseFilename=DOE_Simulator_Setup
Compression=lz4
SolidCompression=yes
LicenseFile=LICENSE.txt

[Files]
Source: "dist\DOE_Simulator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\DOE Simulator"; Filename: "{app}\DOE_Simulator.exe"
Name: "{commondesktop}\DOE Simulator"; Filename: "{app}\DOE_Simulator.exe"

[Run]
Filename: "{app}\DOE_Simulator.exe"; Description: "Launch DOE Simulator"; Flags: nowait postinstall skipifsilent
```

## Troubleshooting

### The .exe won't run
- Make sure Python 3.8+ is installed
- Ensure all dependencies from `requirements.txt` are installed

### Streamlit won't start
- The executable bundles everything, so it should work standalone
- If issues persist, check that Python is properly installed

### The .exe is very large (400+ MB)
- This is normal! PyInstaller bundles Python and all dependencies into a single file
- You can reduce size by using `--onedir` instead of `--onefile` in the spec file

## Distribution

Once you have the `dist\DOE_Simulator.exe` file:

1. **For a single user**: just copy the .exe to their computer
2. **For multiple users**: create an installer (see above)
3. **For distribution**: zip the entire `dist` folder and share

## Notes

- The first run may take a few seconds as Streamlit initializes
- A command window will open alongside the Streamlit browser interface
- Users don't need Python installed to run the .exe

# Building DOE Simulator as an Executable

This guide explains how to create a standalone .exe executable that can be installed and run on any Windows computer.

## Prerequisites

- Python 3.8 or higher installed
- All dependencies listed in `requirements.txt` installed

## Quick Build (Recommended)

1. Open Command Prompt or PowerShell in this project directory
2. Run:
   ```bash
   build.bat
   ```
3. The executable will be created at `dist\DOE_Simulator.exe`

## Manual Build

If the batch file doesn't work, you can build manually:

```bash
python -m pip install pyinstaller
pyinstaller doe_simulator.spec
```

## Running the Executable

After building, you can run the application in two ways:

### Option 1: Command Line
```bash
.\dist\DOE_Simulator.exe
```

### Option 2: Double-click
Simply double-click `dist\DOE_Simulator.exe` to run

A command window will appear with the Streamlit server running, and your default browser will open to the application.

## Creating an Installer (Optional)

To create a professional installer, you can use **Inno Setup**:

1. Download and install [Inno Setup](https://jrsoftware.org/isdl.php)
2. Create a file named `installer.iss` with the installer configuration (see example below)
3. Open `installer.iss` with Inno Setup and compile it
4. This creates a setup .exe that users can run to install your application

### Example Inno Setup Configuration (installer.iss)

```ini
[Setup]
AppName=DOE Simulator
AppVersion=1.0
DefaultDirName={pf}\DOE Simulator
DefaultGroupName=DOE Simulator
OutputDir=.\installers
OutputBaseFilename=DOE_Simulator_Setup
Compression=lz4
SolidCompression=yes
LicenseFile=LICENSE.txt

[Files]
Source: "dist\DOE_Simulator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\DOE Simulator"; Filename: "{app}\DOE_Simulator.exe"
Name: "{commondesktop}\DOE Simulator"; Filename: "{app}\DOE_Simulator.exe"

[Run]
Filename: "{app}\DOE_Simulator.exe"; Description: "Launch DOE Simulator"; Flags: nowait postinstall skipifsilent
```

## Troubleshooting

### The .exe won't run
- Make sure Python 3.8+ is installed
- Ensure all dependencies from `requirements.txt` are installed

### Streamlit won't start
- The executable bundles everything, so it should work standalone
- If issues persist, check that Python is properly installed

### The .exe is very large (400+ MB)
- This is normal! PyInstaller bundles Python and all dependencies into a single file
- You can reduce size by using `--onedir` instead of `--onefile` in the spec file

## Distribution

Once you have the `dist\DOE_Simulator.exe` file:

1. **For a single user**: just copy the .exe to their computer
2. **For multiple users**: create an installer (see above)
3. **For distribution**: zip the entire `dist` folder and share

## Notes

- The first run may take a few seconds as Streamlit initializes
- A command window will open alongside the Streamlit browser interface
- Users don't need Python installed to run the .exe
