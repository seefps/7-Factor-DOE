; Inno Setup installer configuration for DOE Simulator
; This file defines the installer behavior and appearance
; To use: Download Inno Setup from https://jrsoftware.org/isdl.php
; Open this file with Inno Setup Compiler and click "Compile"

[Setup]
AppName=DOE Simulator
AppVersion=1.0.0
AppPublisher=DOE Simulator Team
AppPublisherURL=https://example.com
AppSupportURL=https://example.com
AppUpdatesURL=https://example.com
DefaultDirName={pf}\DOE Simulator
DefaultGroupName=DOE Simulator
OutputDir=.\installers
OutputBaseFilename=DOE_Simulator_Setup
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
LicenseFile=LICENSE.txt
UninstallDisplayIcon={app}\DOE_Simulator.exe
CloseApplications=yes
RestartApplications=yes
WizardStyle=modern
WizardResizable=yes
AllowNoIcons=yes
AllowUNCPath=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1,10.0

[Files]
Source: "dist\DOE_Simulator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DOE Simulator"; Filename: "{app}\DOE_Simulator.exe"
Name: "{group}\Uninstall DOE Simulator"; Filename: "{uninstallexe}"
Name: "{commondesktop}\DOE Simulator"; Filename: "{app}\DOE_Simulator.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\DOE Simulator"; Filename: "{app}\DOE_Simulator.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\DOE_Simulator.exe"; Description: "{cm:LaunchProgram,DOE Simulator}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: dirifempty; Name: "{app}"

; Inno Setup installer configuration for DOE Simulator
; This file defines the installer behavior and appearance
; To use: Download Inno Setup from https://jrsoftware.org/isdl.php
; Open this file with Inno Setup Compiler and click "Compile"

[Setup]
AppName=DOE Simulator
AppVersion=1.0.0
AppPublisher=DOE Simulator Team
AppPublisherURL=https://example.com
AppSupportURL=https://example.com
AppUpdatesURL=https://example.com
DefaultDirName={pf}\DOE Simulator
DefaultGroupName=DOE Simulator
OutputDir=.\installers
OutputBaseFilename=DOE_Simulator_Setup
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
LicenseFile=LICENSE.txt
UninstallDisplayIcon={app}\DOE_Simulator.exe
CloseApplications=yes
RestartApplications=yes
WizardStyle=modern
WizardResizable=yes
AllowNoIcons=yes
AllowUNCPath=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1,10.0

[Files]
Source: "dist\DOE_Simulator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DOE Simulator"; Filename: "{app}\DOE_Simulator.exe"
Name: "{group}\Uninstall DOE Simulator"; Filename: "{uninstallexe}"
Name: "{commondesktop}\DOE Simulator"; Filename: "{app}\DOE_Simulator.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\DOE Simulator"; Filename: "{app}\DOE_Simulator.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\DOE_Simulator.exe"; Description: "{cm:LaunchProgram,DOE Simulator}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: dirifempty; Name: "{app}"
