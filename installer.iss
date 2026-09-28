; Inno Setup Script for SavannaCode
#define MyAppName "SavannaCode"
#define MyAppVersion "1.0"
#define MyAppPublisher "jeixix"
#define MyAppURL "https://github.com/jeixix/GiraffeCode"
#define MyAppExeName "GiraffeCode.exe"

[Setup]
AppId={{D8C96E25-0E78-4D2A-9496-512E7B1A2C39}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=installer_output
OutputBaseFilename=SavannaCode-Setup-v1.0
SetupIconFile=assets\icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Delete all runtime-generated files in the install folder
Type: files; Name: "{app}\settings.json"
Type: files; Name: "{app}\progress.json"
Type: files; Name: "{app}\custom_levels.json"
Type: files; Name: "{app}\crash.log"
Type: files; Name: "{app}\*.log"
Type: filesandordirs; Name: "{app}"

[Code]
// Complete purge of all game files and user data upon uninstallation
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Delete user AppData and LocalAppData folders if created
    DelTree(ExpandConstant('{userappdata}\SavannaCode'), True, True, True);
    DelTree(ExpandConstant('{localappdata}\SavannaCode'), True, True, True);
    // Delete any remaining files and the installation directory itself
    DelTree(ExpandConstant('{app}'), True, True, True);
  end;
end;
