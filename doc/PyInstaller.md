```PowerShell
pip install PyInstaller

pyinstaller --clean --onefile --icon="icon/logo.ico" --add-data="icon;icon" Qiime2App.py

rm -r build
rm Qiime2App.spec
```
