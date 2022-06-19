[Files]
Source: dist\wxmsw28h_html_vc.dll; DestDir: {app}
Source: dist\bz2.pyd; DestDir: {app}
Source: dist\library.zip; DestDir: {app}; Flags: ignoreversion
Source: dist\patiotiler.exe; DestDir: {app}
Source: dist\python26.dll; DestDir: {app}
Source: dist\select.pyd; DestDir: {app}
Source: dist\unicodedata.pyd; DestDir: {app}
Source: dist\w9xpopen.exe; DestDir: {app}
Source: dist\wx._controls_.pyd; DestDir: {app}
Source: dist\wx._core_.pyd; DestDir: {app}
Source: dist\wx._gdi_.pyd; DestDir: {app}
Source: dist\wx._grid.pyd; DestDir: {app}
Source: dist\wx._misc_.pyd; DestDir: {app}
Source: dist\wx._windows_.pyd; DestDir: {app}
Source: dist\wxbase28h_net_vc.dll; DestDir: {app}
Source: dist\wxbase28h_vc.dll; DestDir: {app}
Source: dist\wxmsw28h_adv_vc.dll; DestDir: {app}
Source: dist\wxmsw28h_core_vc.dll; DestDir: {app}
Source: dist\Microsoft.VC90.CRT\msvcr90.dll; DestDir: {app}\Microsoft.VC90.CRT
Source: dist\Microsoft.VC90.CRT\Microsoft.VC90.CRT.manifest; DestDir: {app}\Microsoft.VC90.CRT
Source: dist\Microsoft.VC90.CRT\msvcm90.dll; DestDir: {app}\Microsoft.VC90.CRT
Source: dist\Microsoft.VC90.CRT\msvcp90.dll; DestDir: {app}\Microsoft.VC90.CRT
Source: tileomatic.ico; DestDir: {app}
[Dirs]
Name: {app}\Microsoft.VC90.CRT
[Setup]
AppCopyright=©Joe Marshall 2011
AppName=Patio Tile-o-matic
AppVerName=Patio Tile-o-matic 1.0
DefaultDirName={pf}\PatioTileomatic
DefaultGroupName=Patio Tile-o-matic
ShowLanguageDialog=no
SetupIconFile=C:\projects\patiotiler\tileomatic.ico
WizardImageFile=C:\projects\patiotiler\tileomatic-installer.bmp
WizardSmallImageFile=C:\projects\patiotiler\tileomatic-installer-small.bmp
WizardImageStretch=true
OutputBaseFilename=patiotileomatic
[Icons]
Name: {group}\Patio Tile-o-matic; Filename: {app}\patiotiler.exe; IconFilename: {app}\tileomatic.ico; IconIndex: 0
[Run]
Filename: {app}\patiotiler.exe; Description: Run Patio Tile-o-matic now; Flags: postinstall
