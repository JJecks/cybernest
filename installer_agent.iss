[Setup]
AppName=CyberNest Agent
AppVersion=1.0
AppPublisher=JJecks
DefaultDirName={autopf}\CyberNest Agent
DefaultGroupName=CyberNest
OutputDir=installers
OutputBaseFilename=CyberNest_Agent_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"
Name: "startupicon"; Description: "Start agent automatically when Windows starts"; GroupDescription: "Startup:"; Flags: checkedonce

[Files]
Source: "dist\CyberNest_Agent.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CyberNest Agent"; Filename: "{app}\CyberNest_Agent.exe"
Name: "{group}\Uninstall CyberNest Agent"; Filename: "{uninstallexe}"
Name: "{commondesktop}\CyberNest Agent"; Filename: "{app}\CyberNest_Agent.exe"; Tasks: desktopicon
Name: "{userstartup}\CyberNest Agent"; Filename: "{app}\CyberNest_Agent.exe"; Tasks: startupicon

[Run]
Filename: "{app}\CyberNest_Agent.exe"; Description: "Launch CyberNest Agent now"; Flags: nowait postinstall skipifsilent runascurrentuser