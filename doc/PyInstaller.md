Install PyInstaller

```PowerShell
pip install PyInstaller
```

Package as a .exe file

```PowerShell
$VERSION = "v0.0.0"
pyinstaller --clean --onefile --icon="icon/logo.ico" --add-data="icon;icon" Qiime2App.py
Move-Item -Path "dist\Qiime2App.exe" -Destination "Qiime2App-win-$VERSION.exe"
rm -r build ; rm -r dist ; rm Qiime2App.spec
```

Package as a folder

```PowerShell
$VERSION = "v0.0.0"
pyinstaller --clean --icon="icon/logo.ico" --add-data="icon;icon" Qiime2App.py
Move-Item -Path "dist\Qiime2App.exe" -Destination "Qiime2App.exe"
Compress-Archive -Path "Qiime2App" -DestinationPath "Qiime2App-win-$VERSION.zip"
rm -r build ; rm -r dist ; rm -r Qiime2App ; rm Qiime2App.spec
```
