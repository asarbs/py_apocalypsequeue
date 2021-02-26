@echo off

cmd /k " cd /d ..\venv\Scripts\ & activate & cd /d ../../apocalypsequeue & pyinstaller main.spec --noconfirm & pyinstaller map_editor.spec --noconfirm"