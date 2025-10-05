
[Setup]
AppId={{9EC7B49D-2A06-4DA7-86B4-2B7133F2C285}} 
AppName=Millionaire
AppVersion=1.0
DefaultDirName={userdocs}\Millionaire
DisableDirPage=no 
DefaultGroupName=Millionaire
OutputDir=.
OutputBaseFilename=Millionaire_Installer
Compression=lzma
SolidCompression=yes

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; EXE único
Source: ".\dist\Millionaire.exe"; DestDir: "{app}"; Flags: ignoreversion
; Recursos externos
Source: ".\data\*";   DestDir: "{app}\data";   Flags: recursesubdirs createallsubdirs ignoreversion
Source: ".\\assets\img\icon.ico";   DestDir: "{app}\assets\img";   Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\Millionaire"; Filename: "{app}\Millionaire.exe"; IconFilename: "{app}\assets\img\icon.ico"
Name: "{userdesktop}\Millionaire"; Filename: "{app}\Millionaire.exe"; Tasks: desktopicon; IconFilename: "{app}\assets\img\icon.ico"
Name: "{group}\Desinstalar Millionaire"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\Millionaire.exe"; Description: "Iniciar Millionaire ahora"; Flags: nowait postinstall skipifsilent
