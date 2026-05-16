[Setup]
AppName=CyberNest Server
AppVersion=1.0
AppPublisher=JJecks
DefaultDirName={autopf}\CyberNest Server
DefaultGroupName=CyberNest
OutputDir=installers
OutputBaseFilename=CyberNest_Server_Setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"
Name: "startupicon"; Description: "Start CyberNest Server when Windows starts"; GroupDescription: "Startup:"

[Files]
Source: "dist\CyberNest_Server.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\staticfiles\*"; DestDir: "{app}\staticfiles"; Flags: ignoreversion recursesubdirs
Source: "dist\db.sqlite3"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CyberNest Server"; Filename: "{app}\CyberNest_Server.exe"
Name: "{group}\Uninstall CyberNest Server"; Filename: "{uninstallexe}"
Name: "{commondesktop}\CyberNest Server"; Filename: "{app}\CyberNest_Server.exe"; Tasks: desktopicon
Name: "{userstartup}\CyberNest Server"; Filename: "{app}\CyberNest_Server.exe"; Tasks: startupicon

[Run]
Filename: "{app}\CyberNest_Server.exe"; Description: "Launch CyberNest Server now"; Flags: nowait postinstall skipifsilent