```PowerShell
pip install PyInstaller

pyinstaller --icon="icon/logo.ico" --add-data="icon;icon" Qiime2App.py

rm -r build
rm -r dist
rm Qiime2App.spec
```
